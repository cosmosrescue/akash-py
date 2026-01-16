import base64
import logging
import os
from typing import Dict, Optional, Any

from akash.proto.akash.cert.v1 import cert_pb2 as cert_pb2
from akash.proto.akash.cert.v1 import query_pb2 as cert_query_pb2
from akash.proto.akash.cert.v1 import filters_pb2  # v1: CertificateFilter moved to filters_pb2
from akash.proto.cosmos.base.query.v1beta1 import pagination_pb2 as pagination_pb2

logger = logging.getLogger(__name__)


class CertQuery:
    """
    Mixin for certificate query operations.
    """

    def get_certificates(
            self,
            owner: str = None,
            serial: str = None,
            state: str = None,
            limit: int = 100,
            offset: int = 0,
            count_total: bool = False,
            reverse: bool = False,
    ) -> Dict[str, Any]:
        """
        Get certificates with optional filters.

        Args:
            owner: Filter by certificate owner address
            serial: Filter by certificate serial number
            state: Filter by certificate state ('valid', 'revoked', 'invalid')
            limit: Maximum number of certificates to return (default: 100)
            offset: Number of certificates to skip (default: 0)
            count_total: Whether to count total number of certificates (default: False)
            reverse: Whether to return results in reverse order (default: False)

        Returns:
            Dict[str, Any]: Dictionary containing certificates list and pagination info
        """
        try:
            logger.info(
                f"Querying certificates with filters: owner={owner}, serial={serial}, state={state}"
            )

            request = cert_query_pb2.QueryCertificatesRequest()

            # v1: CertificateFilter moved to filters_pb2
            cert_filter = filters_pb2.CertificateFilter()
            if owner:
                cert_filter.owner = owner
            if serial:
                cert_filter.serial = serial
            if state:
                state_map = {"invalid": 0, "valid": 1, "revoked": 2}
                if state in state_map:
                    cert_filter.state = state
            request.filter.CopyFrom(cert_filter)

            page_request = pagination_pb2.PageRequest()
            page_request.limit = limit
            page_request.offset = offset
            page_request.count_total = count_total
            page_request.reverse = reverse
            request.pagination.CopyFrom(page_request)

            path = "/akash.cert.v1.Query/Certificates"
            result = self.akash_client.rpc_query(
                "abci_query",
                [path, request.SerializeToString().hex().upper(), "0", False],
            )

            if not result or "response" not in result:
                error_msg = f"Query failed: No response from {path}"
                logger.error(error_msg)
                raise Exception(error_msg)

            response = result["response"]
            response_code = response.get("code", -1)

            if response_code != 0:
                error_msg = f"Query failed with code {response_code}: {response.get('log', 'Unknown error')}"
                logger.error(error_msg)
                raise Exception(error_msg)

            if "value" not in response or not response["value"]:
                logger.info(
                    "Query succeeded but returned no certificates (empty result)"
                )
                return {
                    "certificates": [],
                    "pagination": {
                        "next_key": None,
                        "total": 0 if count_total else None,
                    },
                }

            try:
                response_bytes = base64.b64decode(response["value"])
                query_response = cert_query_pb2.QueryCertificatesResponse()
                query_response.ParseFromString(response_bytes)

                certificates = []
                for cert_response in query_response.certificates:
                    cert_info = {
                        "serial": cert_response.serial,
                        "certificate": {
                            "state": self._get_state_name(
                                cert_response.certificate.state
                            ),
                            "cert": base64.b64encode(
                                cert_response.certificate.cert
                            ).decode(),
                            "pubkey": base64.b64encode(
                                cert_response.certificate.pubkey
                            ).decode(),
                        },
                    }
                    certificates.append(cert_info)

                next_key = None
                if query_response.pagination.next_key:
                    try:
                        next_key = query_response.pagination.next_key.decode("utf-8")
                    except UnicodeDecodeError:
                        next_key = base64.b64encode(
                            query_response.pagination.next_key
                        ).decode()

                pagination_info = {
                    "next_key": next_key,
                    "total": query_response.pagination.total if count_total else None,
                }

                logger.info(f"Found {len(certificates)} certificates")
                return {"certificates": certificates, "pagination": pagination_info}

            except Exception as parse_error:
                error_msg = f"Failed to parse certificates response: {parse_error}"
                logger.error(error_msg)
                raise Exception(error_msg)

        except Exception as e:
            logger.error(f"Failed to get certificates: {e}")
            raise

    def get_certificate(self, owner: str, serial: str) -> Optional[Dict]:
        """
        Get a specific certificate by owner and serial number.

        Args:
            owner: Certificate owner address
            serial: Certificate serial number

        Returns:
            Optional[Dict]: Certificate data with keys: 'serial', 'certificate'
                           containing 'state', 'cert' (base64), 'pubkey' (base64),
                           or None if not found
        """
        try:
            logger.info(f"Querying certificate for owner {owner} and serial {serial}")
            result = self.get_certificates(owner=owner, serial=serial, limit=1)
            certificates = result.get("certificates", [])
            if certificates:
                return certificates[0]
            logger.info(f"No certificate found for owner {owner} and serial {serial}")
            return None
        except Exception as e:
            logger.error(f"Failed to get certificate by owner and serial: {e}")
            raise

    def _get_state_name(self, state_value: int) -> str:
        """
        Convert certificate state enum value to string name.

        Args:
            state_value: State enum value

        Returns:
            str: State name
        """
        state_map = {0: "invalid", 1: "valid", 2: "revoked"}
        return state_map.get(state_value, "unknown")

    def get_mtls_credentials(self, owner: str, serial: str = None) -> Dict[str, Any]:
        """
        Get certificate data for mTLS from blockchain and save to files.

        Args:
            owner: Certificate owner's Akash address
            serial: Certificate serial (optional, gets latest if empty)

        Returns:
            Dict with certificate paths for gRPC
        """
        try:
            if serial:
                cert_result = self.get_certificate(owner, serial)
            else:
                certs = self.get_certificates(owner=owner, limit=1)
                cert_result = certs.get('certificates', [None])[0] if certs else None
            if not cert_result:
                return {
                    "status": "error",
                    "error": f"No certificate found for {owner}",
                    "recommendation": "Create certificate first using create_certificate_for_mtls()",
                }

            cert_data = cert_result["certificate"]

            try:
                cert_pem = base64.b64decode(cert_data["cert"]).decode()
                pubkey_pem = base64.b64decode(cert_data["pubkey"]).decode()
            except Exception as e:
                logger.error(f"Failed to decode certificate data: {e}")
                return {"status": "error", "error": "Invalid certificate encoding"}

            logger.warning(
                "Certificate retrieved from blockchain, but private key must be loaded from local storage"
            )

            ca_pem = cert_pem

            cert_dir = "certs"
            os.makedirs(cert_dir, exist_ok=True)

            cert_paths = {
                "client_cert": f"{cert_dir}/client.pem",
                "client_key": f"{cert_dir}/client-key.pem",
                "ca_cert": f"{cert_dir}/ca.pem",
            }

            with open(cert_paths["client_cert"], "w") as f:
                f.write(cert_pem)

            if not os.path.exists(cert_paths["client_key"]):
                logger.error(f"Private key not found at {cert_paths['client_key']}")
                return {
                    "status": "error",
                    "error": "Private key not found locally. Private keys are never stored on blockchain.",
                    "recommendation": "Use create_certificate_for_mtls() to generate both cert and key locally",
                }

            with open(cert_paths["ca_cert"], "w") as f:
                f.write(ca_pem)

            logger.info(f"Certificate credentials prepared for {owner}")
            return {
                "status": "success",
                "file_paths": cert_paths,
                "cert_data": {
                    "cert": cert_pem,
                    "pubkey": pubkey_pem,
                    "ca_cert": ca_pem,
                    "serial": cert_data.get("serial", "unknown"),
                },
                "note": "Private key must be loaded from local storage",
            }

        except Exception as e:
            logger.error(f"Failed to get mTLS credentials: {e}")
            return {"status": "error", "error": str(e)}
