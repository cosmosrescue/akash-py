import base64
import datetime
import logging
import os
from cryptography import x509
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec
from typing import Dict, Any, Optional

from ...tx import BroadcastResult, broadcast_transaction_rpc

logger = logging.getLogger(__name__)


class CertTx:
    """
    Mixin for certificate transaction operations.
    """

    def publish_client_certificate(
            self,
            wallet,
            cert_data: bytes,
            public_key: bytes,
            memo: str = "",
            fee_amount: str = "20000",
            gas_limit: int = None,
            gas_adjustment: float = 1.2,
            use_simulation: bool = True,
    ) -> BroadcastResult:
        """
        Publish a client certificate to the blockchain.

        Args:
            wallet: AkashWallet instance
            cert_data: Certificate data in bytes
            public_key: Public key data in bytes
            memo: Transaction memo
            fee_amount: Transaction fee amount in uakt
            gas_limit: Gas limit override
            gas_adjustment: Multiplier for gas estimation (default 1.2)
            use_simulation: Enable gas simulation

        Returns:
            BroadcastResult: Transaction result
        """
        try:
            logger.info(f"Publishing client certificate for {wallet.address}")

            if not isinstance(cert_data, bytes):
                raise TypeError(f"cert_data must be bytes, got {type(cert_data)}")
            if not isinstance(public_key, bytes):
                raise TypeError(f"public_key must be bytes, got {type(public_key)}")

            msg = {
                "@type": "/akash.cert.v1.MsgCreateCertificate",
                "owner": wallet.address,
                "cert": base64.b64encode(cert_data).decode(),
                "pubkey": base64.b64encode(public_key).decode(),
            }

            return broadcast_transaction_rpc(
                client=self.akash_client,
                wallet=wallet,
                messages=[msg],
                memo=memo,
                fee_amount=fee_amount,
                gas_limit=gas_limit,
                gas_adjustment=gas_adjustment,
                use_simulation=use_simulation,
                wait_for_confirmation=True,
                confirmation_timeout=30,
            )

        except Exception as e:
            logger.error(f"Failed to publish client certificate: {e}")
            return BroadcastResult(
                "", 1, f"Error publishing client certificate: {str(e)}", False
            )

    def create_certificate(
            self,
            wallet,
            memo: str = "",
            fee_amount: str = "20000",
            gas_limit: int = None,
            use_simulation: bool = True,
    ) -> BroadcastResult:
        """
        Create and publish a client certificate for mTLS authentication.

        This method generates a complete certificate and private key pair,
        publishes the certificate to the blockchain, and returns the result.
        The private key is stored locally for mTLS authentication.

        Args:
            wallet: AkashWallet instance
            memo: Transaction memo
            fee_amount: Transaction fee amount in uakt
            gas_limit: Gas limit override
            use_simulation: Enable gas simulation

        Returns:
            BroadcastResult: Transaction result with certificate info
        """
        try:
            logger.info(f"Creating certificate for {wallet.address}")

            existing_certs = self.get_certificates(wallet.address)
            if existing_certs and len(existing_certs.get("certificates", [])) > 0:
                logger.info("Certificate already exists")
                return BroadcastResult(
                    "existing", 0, "Certificate already exists", True
                )

            import datetime
            from cryptography import x509
            from cryptography.hazmat.primitives import serialization, hashes
            from cryptography.hazmat.primitives.asymmetric import ec

            # Generate private key (using secp256r1/NIST P-256 curve)
            private_key = ec.generate_private_key(ec.SECP256R1())

            subject = issuer = x509.Name(
                [
                    x509.NameAttribute(x509.NameOID.COMMON_NAME, wallet.address),
                ]
            )

            cert = (
                x509.CertificateBuilder()
                .subject_name(subject)
                .issuer_name(issuer)
                .public_key(private_key.public_key())
                .serial_number(x509.random_serial_number())
                .not_valid_before(datetime.datetime.utcnow())
                .not_valid_after(
                    datetime.datetime.utcnow() + datetime.timedelta(days=365)
                )
                .add_extension(
                    x509.KeyUsage(
                        digital_signature=True,
                        key_encipherment=True,
                        key_agreement=False,
                        key_cert_sign=False,
                        crl_sign=False,
                        content_commitment=False,
                        data_encipherment=False,
                        encipher_only=False,
                        decipher_only=False,
                    ),
                    critical=True,
                )
                .add_extension(
                    x509.ExtendedKeyUsage([x509.oid.ExtendedKeyUsageOID.CLIENT_AUTH]),
                    critical=True,
                )
                .sign(private_key, hashes.SHA256())
            )

            # Serialize certificate
            cert_pem = cert.public_bytes(serialization.Encoding.PEM)

            # Create EC PUBLIC KEY format for blockchain
            public_key_der = private_key.public_key().public_bytes(
                encoding=serialization.Encoding.DER,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )

            # Convert DER to EC PUBLIC KEY PEM format
            import base64

            public_key_b64 = base64.b64encode(public_key_der[26:]).decode(
                "utf-8"
            )  # Skip DER header
            public_key_lines = [
                public_key_b64[i: i + 64] for i in range(0, len(public_key_b64), 64)
            ]
            public_key_pem = (
                    "-----BEGIN EC PUBLIC KEY-----\n"
                    + "\n".join(public_key_lines)
                    + "\n-----END EC PUBLIC KEY-----"
            )
            public_key_bytes = public_key_pem.encode("utf-8")

            # Store private key for mTLS
            private_key_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )

            # Store certificate details on the client for mTLS use
            if not hasattr(self.akash_client, "_certificate_store"):
                self.akash_client._certificate_store = {}

            self.akash_client._certificate_store[wallet.address] = {
                "certificate_pem": cert_pem.decode("utf-8"),
                "private_key_pem": private_key_pem.decode("utf-8"),
                "created_at": datetime.datetime.utcnow().isoformat(),
            }

            # Publish to blockchain
            result = self.publish_client_certificate(
                wallet=wallet,
                cert_data=cert_pem,
                public_key=public_key_bytes,
                memo=memo,
                fee_amount=fee_amount,
                gas_limit=gas_limit,
                use_simulation=use_simulation,
            )

            if result.success:
                logger.info(
                    f"Certificate created and published successfully! TX: {result.tx_hash}"
                )
                # Add certificate info to result
                result.certificate_pem = cert_pem.decode("utf-8")
                result.private_key_pem = private_key_pem.decode("utf-8")
            else:
                logger.error("Failed to publish certificate")

            return result

        except Exception as e:
            logger.error(f"Failed to create certificate: {e}")
            return BroadcastResult("", 1, f"Failed to create certificate: {e}", False)

    def publish_server_certificate(
            self,
            wallet,
            cert_data: bytes,
            public_key: bytes,
            memo: str = "",
            fee_amount: str = "20000",
            gas_limit: int = None,
            gas_adjustment: float = 1.2,
            use_simulation: bool = True,
    ) -> BroadcastResult:
        """
        Publish a server certificate to the blockchain.

        Args:
            wallet: AkashWallet instance
            cert_data: Certificate data in bytes
            public_key: Public key data in bytes
            memo: Transaction memo
            fee_amount: Transaction fee amount in uakt
            gas_limit: Gas limit override
            gas_adjustment: Multiplier for gas estimation (default 1.2)
            use_simulation: Enable gas simulation

        Returns:
            BroadcastResult: Transaction result
        """
        try:
            logger.info(f"Publishing server certificate for {wallet.address}")

            msg = {
                "@type": "/akash.cert.v1.MsgCreateCertificate",
                "owner": wallet.address,
                "cert": base64.b64encode(cert_data).decode(),
                "pubkey": base64.b64encode(public_key).decode(),
            }

            return broadcast_transaction_rpc(
                client=self.akash_client,
                wallet=wallet,
                messages=[msg],
                memo=memo,
                fee_amount=fee_amount,
                gas_limit=gas_limit,
                gas_adjustment=gas_adjustment,
                use_simulation=use_simulation,
                wait_for_confirmation=True,
                confirmation_timeout=30,
            )

        except Exception as e:
            logger.error(f"Failed to publish server certificate: {e}")
            return BroadcastResult(
                "", 1, f"Error publishing server certificate: {str(e)}", False
            )

    def revoke_client_certificate(
            self,
            wallet,
            serial: str,
            memo: str = "",
            fee_amount: str = "20000",
            gas_limit: int = None,
            gas_adjustment: float = 1.2,
            use_simulation: bool = True,
    ) -> BroadcastResult:
        """
        Revoke a client certificate.

        Args:
            wallet: AkashWallet instance (must be certificate owner)
            serial: Certificate serial number to revoke
            memo: Transaction memo
            fee_amount: Transaction fee amount in uakt
            gas_limit: Gas limit override
            gas_adjustment: Multiplier for gas estimation (default 1.2)
            use_simulation: Enable gas simulation

        Returns:
            BroadcastResult: Transaction result
        """
        try:
            logger.info(f"Revoking client certificate {serial} for {wallet.address}")

            msg = {
                "@type": "/akash.cert.v1.MsgRevokeCertificate",
                "id": {"owner": wallet.address, "serial": serial},
            }

            return broadcast_transaction_rpc(
                client=self.akash_client,
                wallet=wallet,
                messages=[msg],
                memo=memo,
                fee_amount=fee_amount,
                gas_limit=gas_limit,
                gas_adjustment=gas_adjustment,
                use_simulation=use_simulation,
                wait_for_confirmation=True,
                confirmation_timeout=30,
            )

        except Exception as e:
            logger.error(f"Failed to revoke client certificate: {e}")
            return BroadcastResult(
                "", 1, f"Error revoking client certificate: {str(e)}", False
            )

    def revoke_server_certificate(
            self,
            wallet,
            serial: str,
            memo: str = "",
            fee_amount: str = "20000",
            gas_limit: int = None,
            gas_adjustment: float = 1.2,
            use_simulation: bool = True,
    ) -> BroadcastResult:
        """
        Revoke a server certificate.

        Args:
            wallet: AkashWallet instance (must be certificate owner)
            serial: Certificate serial number to revoke
            memo: Transaction memo
            fee_amount: Transaction fee amount in uakt
            gas_limit: Gas limit override
            gas_adjustment: Multiplier for gas estimation (default 1.2)
            use_simulation: Enable gas simulation

        Returns:
            BroadcastResult: Transaction result
        """
        try:
            logger.info(f"Revoking server certificate {serial} for {wallet.address}")

            msg = {
                "@type": "/akash.cert.v1.MsgRevokeCertificate",
                "id": {"owner": wallet.address, "serial": serial},
            }

            return broadcast_transaction_rpc(
                client=self.akash_client,
                wallet=wallet,
                messages=[msg],
                memo=memo,
                fee_amount=fee_amount,
                gas_limit=gas_limit,
                gas_adjustment=gas_adjustment,
                use_simulation=use_simulation,
                wait_for_confirmation=True,
                confirmation_timeout=30,
            )

        except Exception as e:
            logger.error(f"Failed to revoke server certificate: {e}")
            return BroadcastResult(
                "", 1, f"Error revoking server certificate: {str(e)}", False
            )

    def create_certificate_for_mtls(
            self,
            wallet,
            ca_cert_path: Optional[str] = None,
            ca_key_path: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create and store a client certificate for mTLS, saving to local files.

        Args:
            wallet: Wallet for signing transaction.
            ca_cert_path: Optional path to CA certificate for signing (if None, creates self-signed).
            ca_key_path: Optional path to CA private key for signing (required if ca_cert_path is provided).

        Returns:
            Dict with certificate details and file paths.
        """
        try:
            private_key = ec.generate_private_key(ec.SECP256R1())
            public_key = private_key.public_key()

            subject = x509.Name(
                [x509.NameAttribute(x509.oid.NameOID.COMMON_NAME, wallet.address)]
            )

            if ca_cert_path and ca_key_path:
                with open(ca_cert_path, "rb") as f:
                    ca_cert = x509.load_pem_x509_certificate(f.read())
                with open(ca_key_path, "rb") as f:
                    ca_key = serialization.load_pem_private_key(f.read(), password=None)
                issuer = ca_cert.subject
                signing_key = ca_key
                logger.info(f"Using CA certificate from {ca_cert_path} for signing")
            else:
                issuer = subject
                signing_key = private_key
                logger.info("Creating self-signed certificate (no CA provided)")

            cert_builder = x509.CertificateBuilder()
            cert_builder = cert_builder.subject_name(subject)
            cert_builder = cert_builder.issuer_name(issuer)
            cert_builder = cert_builder.public_key(public_key)
            cert_builder = cert_builder.serial_number(x509.random_serial_number())
            cert_builder = cert_builder.not_valid_before(datetime.datetime.utcnow())
            cert_builder = cert_builder.not_valid_after(
                datetime.datetime.utcnow() + datetime.timedelta(days=365)
            )

            cert_builder = cert_builder.add_extension(
                x509.KeyUsage(
                    digital_signature=True,
                    key_encipherment=True,
                    content_commitment=False,
                    data_encipherment=False,
                    key_agreement=False,
                    key_cert_sign=False,
                    crl_sign=False,
                    encipher_only=False,
                    decipher_only=False
                ),
                critical=True
            )

            cert_builder = cert_builder.add_extension(
                x509.ExtendedKeyUsage([x509.oid.ExtendedKeyUsageOID.CLIENT_AUTH]),
                critical=True
            )

            cert = cert_builder.sign(signing_key, hashes.SHA256())

            cert_bytes = cert.public_bytes(serialization.Encoding.PEM)
            cert_pem = cert_bytes.decode().replace("\n", "\r\n")

            key_bytes = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )
            key_pem = key_bytes.decode().replace("\n", "\r\n")

            # (SubjectPublicKeyInfo DER wrapped with EC PUBLIC KEY headers)
            pubkey_der = public_key.public_bytes(
                encoding=serialization.Encoding.DER,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
            pubkey_b64 = base64.b64encode(pubkey_der).decode("ascii")
            pubkey_pem_lines = ["-----BEGIN EC PUBLIC KEY-----"]
            for i in range(0, len(pubkey_b64), 64):
                pubkey_pem_lines.append(pubkey_b64[i: i + 64])
            pubkey_pem_lines.append("-----END EC PUBLIC KEY-----")
            pubkey_pem = "\r\n".join(pubkey_pem_lines) + "\r\n"

            if ca_cert_path:
                with open(ca_cert_path, "r") as f:
                    ca_pem = f.read().replace("\n", "\r\n")
            else:
                ca_pem = cert_pem

            cert_data = cert_pem.encode()
            pubkey_data = pubkey_pem.encode()

            result = self.publish_client_certificate(wallet, cert_data, pubkey_data)

            if not result.success:
                error_msg = getattr(result, "error", None) or getattr(
                    result, "raw_log", "Unknown error"
                )
                return {
                    "status": "error",
                    "error": f"Certificate publish failed: {error_msg}",
                    "step": "blockchain_publish",
                }

            try:
                cert_dir = "certs"
                os.makedirs(cert_dir, exist_ok=True)

                cert_paths = {
                    "client_cert": f"{cert_dir}/client.pem",
                    "client_key": f"{cert_dir}/client-key.pem",
                    "ca_cert": f"{cert_dir}/ca.pem",
                }

                with open(cert_paths["client_cert"], "w") as f:
                    f.write(cert_pem)
                with open(cert_paths["client_key"], "w") as f:
                    f.write(key_pem)
                with open(cert_paths["ca_cert"], "w") as f:
                    f.write(ca_pem)

            except (IOError, OSError) as e:
                return {"status": "error", "error": str(e), "step": "file_save"}

            logger.info(f"Certificate created and saved for {wallet.address}")
            return {
                "status": "success",
                "tx_hash": result.tx_hash,
                "cert_data": {
                    "cert": cert_pem,
                    "key": key_pem,
                    "ca_cert": ca_pem,
                    "serial": str(cert.serial_number),
                },
                "file_paths": cert_paths,
            }

        except Exception as e:
            logger.error(f"Failed to create certificate: {e}")
            return {"status": "error", "error": str(e)}
