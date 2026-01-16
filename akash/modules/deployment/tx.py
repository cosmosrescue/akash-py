import logging
import time
from typing import Dict, List, Any

from ...tx import BroadcastResult, broadcast_transaction_rpc

logger = logging.getLogger(__name__)


class DeploymentTx:
    """
    Mixin for deployment transaction operations.
    """

    def create_deployment(
        self,
        wallet,
        sdl_yaml: str,
        deposit: str = "5000000",
        deposit_denom: str = "uakt",
        version: str = None,
        memo: str = "",
        fee_amount: str = None,
        gas_limit: int = None,
        gas_adjustment: float = 1.2,
        use_simulation: bool = True,
    ) -> BroadcastResult:
        """
        Create deployment from SDL YAML.

        Args:
            wallet: AkashWallet instance
            sdl_yaml: SDL YAML content as string (required)
            deposit: Deposit amount (default: "5000000")
            deposit_denom: Deposit token denomination (default: "uakt")
            version: Deployment hash (calculated from SDL if not provided) - renamed from 'version' in v1beta4
            memo: Transaction memo
            fee_amount: Fee amount in uakt
            gas_limit: Gas limit override
            gas_adjustment: Multiplier for simulated gas
            use_simulation: Enable/disable gas simulation

        Returns:
            BroadcastResult with transaction details
        """
        try:
            import hashlib
            import json
            import base64
            import yaml

            if not sdl_yaml:
                raise ValueError("sdl_yaml is required")

            sdl_data = yaml.safe_load(sdl_yaml)
            deployment_groups = self._create_groups_from_sdl(sdl_data)

            if version is None:
                parse_result = self.akash_client.manifest.parse_sdl(sdl_yaml)
                if parse_result.get('status') != 'success':
                    raise ValueError(f"SDL parsing failed: {parse_result.get('error')}")

                manifest_data = parse_result.get('manifest_data', [])
                legacy_manifest = self.akash_client.manifest._create_legacy_manifest(manifest_data)
                manifest_json = json.dumps(legacy_manifest, sort_keys=True, separators=(',', ':'))
                manifest_json = self.akash_client.manifest._escape_html(manifest_json)
                version_hash = hashlib.sha256(manifest_json.encode()).hexdigest()

            logger.info(f"Creating deployment with {len(deployment_groups)} deployment_groups")

            dseq = int(time.time())

            msg_dict = {
                "@type": "/akash.deployment.v1beta4.MsgCreateDeployment",
                "id": {"owner": wallet.address, "dseq": str(dseq)},
                "hash": version_hash,
                "groups": [
                    self._group_spec_to_dict(group_data) for group_data in deployment_groups
                ],
                "deposit": {
                    "amount": {"denom": deposit_denom, "amount": deposit},
                    "sources": ["1"]  # 1 = SourceBalance (from akash.base.deposit.v1.Source enum)
                },
            }

            result = broadcast_transaction_rpc(
                client=self.akash_client,
                wallet=wallet,
                messages=[msg_dict],
                memo=memo,
                fee_amount=fee_amount,
                gas_limit=gas_limit,
                gas_adjustment=gas_adjustment,
                use_simulation=use_simulation,
            )

            if result.success:
                result.dseq = dseq
                logger.info(f"Deployment created successfully with DSEQ: {dseq}")

            return result

        except Exception as e:
            logger.error(f"Failed to create deployment: {e}")
            return BroadcastResult("", 1, f"Deployment creation failed: {e}", False)

    def update_deployment(
        self,
        wallet,
        sdl_yaml: str,
        owner: str = None,
        dseq: int = None,
        memo: str = "",
        fee_amount: str = None,
        gas_limit: int = None,
        gas_adjustment: float = 1.2,
        use_simulation: bool = True,
    ) -> BroadcastResult:
        """
        Update deployment with SDL YAML content.

        Args:
            wallet: AkashWallet instance
            sdl_yaml: SDL YAML content as string (required)
            owner: Deployment owner address (defaults to wallet address)
            dseq: Deployment sequence number (required)
            memo: Transaction memo
            fee_amount: Fee amount in uakt
            gas_limit: Gas limit override
            gas_adjustment: Multiplier for simulated gas
            use_simulation: Enable/disable gas simulation

        Returns:
            BroadcastResult with transaction details
        """
        try:
            import hashlib
            import json
            import base64
            import yaml

            if not sdl_yaml:
                raise ValueError("sdl_yaml is required")

            if owner is None:
                owner = wallet.address

            if dseq is None:
                raise ValueError("dseq (deployment sequence number) is required")

            parse_result = self.akash_client.manifest.parse_sdl(sdl_yaml)
            if parse_result.get('status') != 'success':
                raise ValueError(f"SDL parsing failed: {parse_result.get('error')}")

            manifest_data = parse_result.get('manifest_data', [])
            legacy_manifest = self.akash_client.manifest._create_legacy_manifest(manifest_data)
            manifest_json = json.dumps(legacy_manifest, sort_keys=True, separators=(',', ':'))

            manifest_json = self.akash_client.manifest._escape_html(manifest_json)

            version_hash = hashlib.sha256(manifest_json.encode()).hexdigest()

            logger.info(
                f"Updating deployment {dseq} with manifest version: {version_hash}"
            )

            msg_dict = {
                "@type": "/akash.deployment.v1beta4.MsgUpdateDeployment",
                "id": {"owner": owner, "dseq": str(dseq)},
                "hash": version_hash
            }

            return broadcast_transaction_rpc(
                client=self.akash_client,
                wallet=wallet,
                messages=[msg_dict],
                memo=memo,
                fee_amount=fee_amount,
                gas_limit=gas_limit,
                gas_adjustment=gas_adjustment,
                use_simulation=use_simulation,
            )

        except Exception as e:
            logger.error(f"Failed to update deployment: {e}")
            return BroadcastResult("", 1, f"Deployment update failed: {e}", False)

    def close_deployment(
        self,
        wallet,
        owner: str,
        dseq: int,
        memo: str = "",
        fee_amount: str = None,
        gas_limit: int = None,
        gas_adjustment: float = 1.2,
        use_simulation: bool = True,
    ) -> BroadcastResult:
        """
        Close deployment.

        Args:
            wallet: AkashWallet instance
            owner: Deployment owner address
            dseq: Deployment sequence number
            memo: Transaction memo
            fee_amount: Fee amount in uakt
            gas_limit: Gas limit override
            gas_adjustment: Multiplier for simulated gas
            use_simulation: Enable/disable gas simulation

        Returns:
            BroadcastResult with transaction details
        """
        try:
            logger.info(f"Closing deployment {dseq}")

            msg_dict = self._close_deployment_msg(owner, dseq)

            return broadcast_transaction_rpc(
                client=self.akash_client,
                wallet=wallet,
                messages=[msg_dict],
                memo=memo,
                fee_amount=fee_amount,
                gas_limit=gas_limit,
                gas_adjustment=gas_adjustment,
                use_simulation=use_simulation,
            )

        except Exception as e:
            logger.error(f"Failed to close deployment: {e}")
            return BroadcastResult("", 1, f"Deployment closure failed: {e}", False)

    def deposit_deployment(
        self,
        wallet,
        owner: str,
        dseq: int,
        amount: str,
        denom: str = "uakt",
        memo: str = "",
        fee_amount: str = None,
        gas_limit: int = None,
        gas_adjustment: float = 1.2,
        use_simulation: bool = True,
    ) -> BroadcastResult:
        """
        Add funds to deployment deposit account.

        Args:
            wallet: Wallet for signing transactions
            owner: Deployment owner address
            dseq: Deployment sequence number
            amount: Amount to deposit
            denom: Token denomination (default: "uakt")
            memo: Transaction memo
            fee_amount: Fee amount in uakt
            gas_limit: Gas limit override
            gas_adjustment: Multiplier for simulated gas
            use_simulation: Enable/disable gas simulation

        Returns:
            BroadcastResult: Transaction result
        """
        try:
            logger.info(f"Depositing {amount} {denom} to deployment {dseq}")

            msg_dict = self._deposit_deployment_msg(
                owner, dseq, amount, denom, wallet.address
            )

            return broadcast_transaction_rpc(
                client=self.akash_client,
                wallet=wallet,
                messages=[msg_dict],
                memo=memo,
                fee_amount=fee_amount,
                gas_limit=gas_limit,
                gas_adjustment=gas_adjustment,
                use_simulation=use_simulation,
            )

        except Exception as e:
            logger.error(f"Error depositing to deployment: {e}")
            return BroadcastResult("", 1, f"Deployment deposit failed: {e}", False)

    def close_group(
        self,
        wallet,
        owner: str,
        dseq: int,
        gseq: int,
        memo: str = "",
        fee_amount: str = None,
        gas_limit: int = None,
        gas_adjustment: float = 1.2,
        use_simulation: bool = True,
    ) -> BroadcastResult:
        """
        Close a specific group within a deployment.

        Args:
            wallet: Wallet for signing transactions
            owner: Deployment owner address
            dseq: Deployment sequence number
            gseq: Group sequence number
            memo: Transaction memo
            fee_amount: Fee amount in uakt
            gas_limit: Gas limit override
            gas_adjustment: Multiplier for simulated gas
            use_simulation: Enable/disable gas simulation

        Returns:
            BroadcastResult: Transaction result
        """
        try:
            logger.info(f"Closing group {gseq} in deployment {dseq}")

            msg_dict = self._close_group_msg(owner, dseq, gseq)

            return broadcast_transaction_rpc(
                client=self.akash_client,
                wallet=wallet,
                messages=[msg_dict],
                memo=memo,
                fee_amount=fee_amount,
                gas_limit=gas_limit,
                gas_adjustment=gas_adjustment,
                use_simulation=use_simulation,
            )

        except Exception as e:
            logger.error(f"Error closing group: {e}")
            return BroadcastResult("", 1, f"Group closure failed: {e}", False)

    def pause_group(
        self,
        wallet,
        owner: str,
        dseq: int,
        gseq: int,
        memo: str = "",
        fee_amount: str = None,
        gas_limit: int = None,
        gas_adjustment: float = 1.2,
        use_simulation: bool = True,
    ) -> BroadcastResult:
        """
        Pause a specific group within a deployment.

        Args:
            wallet: Wallet for signing transactions
            owner: Deployment owner address
            dseq: Deployment sequence number
            gseq: Group sequence number
            memo: Transaction memo
            fee_amount: Fee amount in uakt
            gas_limit: Gas limit override
            gas_adjustment: Multiplier for simulated gas
            use_simulation: Enable/disable gas simulation

        Returns:
            BroadcastResult: Transaction result
        """
        try:
            logger.info(f"Pausing group {gseq} in deployment {dseq}")

            msg_dict = self._pause_group_msg(owner, dseq, gseq)

            return broadcast_transaction_rpc(
                client=self.akash_client,
                wallet=wallet,
                messages=[msg_dict],
                memo=memo,
                fee_amount=fee_amount,
                gas_limit=gas_limit,
                gas_adjustment=gas_adjustment,
                use_simulation=use_simulation,
            )

        except Exception as e:
            logger.error(f"Error pausing group: {e}")
            return BroadcastResult("", 1, f"Group pause failed: {e}", False)

    def start_group(
        self,
        wallet,
        owner: str,
        dseq: int,
        gseq: int,
        memo: str = "",
        fee_amount: str = None,
        gas_limit: int = None,
        gas_adjustment: float = 1.2,
        use_simulation: bool = True,
    ) -> BroadcastResult:
        """
        Start a specific group within a deployment.

        Args:
            wallet: Wallet for signing transactions
            owner: Deployment owner address
            dseq: Deployment sequence number
            gseq: Group sequence number
            memo: Transaction memo
            fee_amount: Fee amount in uakt
            gas_limit: Gas limit override
            gas_adjustment: Multiplier for simulated gas
            use_simulation: Enable/disable gas simulation

        Returns:
            BroadcastResult: Transaction result
        """
        try:
            logger.info(f"Starting group {gseq} in deployment {dseq}")

            msg_dict = self._start_group_msg(owner, dseq, gseq)

            return broadcast_transaction_rpc(
                client=self.akash_client,
                wallet=wallet,
                messages=[msg_dict],
                memo=memo,
                fee_amount=fee_amount,
                gas_limit=gas_limit,
                gas_adjustment=gas_adjustment,
                use_simulation=use_simulation,
            )

        except Exception as e:
            logger.error(f"Error starting group: {e}")
            return BroadcastResult("", 1, f"Group start failed: {e}", False)
