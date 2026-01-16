import logging
from typing import Dict, List

from ...tx import BroadcastResult, broadcast_transaction_rpc

logger = logging.getLogger(__name__)


class AuditTx:
    """
    Mixin for audit transaction operations.
    """

    def create_provider_attributes(
        self,
        wallet,
        owner: str,
        attributes: List[Dict],
        memo: str = "",
        fee_amount: str = None,
        gas_limit: int = None,
        gas_adjustment: float = 1.2,
        use_simulation: bool = True,
    ) -> BroadcastResult:
        """
        Create/update provider attributes as an auditor.

        Args:
            wallet: AkashWallet instance (auditor wallet)
            owner: Provider owner address to sign attributes for
            attributes: List of attributes to sign [{'key': 'region', 'value': 'us-west'}]
            memo: Transaction memo
            fee_amount: Transaction fee amount in uakt
            gas_limit: Gas limit
            gas_adjustment: Multiplier for gas estimation (default 1.2)
            use_simulation: Enable gas simulation

        Returns:
            BroadcastResult: Transaction result
        """
        try:
            logger.info(
                f"Signing attributes for provider {owner} by auditor {wallet.address}"
            )

            msg = {
                "@type": "/akash.audit.v1.MsgSignProviderAttributes",
                "owner": owner,
                "auditor": wallet.address,
                "attributes": [
                    {"key": attr["key"], "value": attr["value"]} for attr in attributes
                ],
            }

            return broadcast_transaction_rpc(
                client=self.akash_client,
                wallet=wallet,
                messages=[msg],
                memo=memo,
                fee_amount=fee_amount or "20000",
                gas_limit=gas_limit,
                gas_adjustment=gas_adjustment,
                use_simulation=use_simulation,
                wait_for_confirmation=True,
                confirmation_timeout=30,
            )

        except Exception as e:
            logger.error(f"Failed to create provider attributes: {e}")
            return BroadcastResult(
                "", 1, f"Create provider attributes failed: {str(e)}", False
            )

    def delete_provider_attributes(
        self,
        wallet,
        owner: str,
        keys: List[str],
        memo: str = "",
        fee_amount: str = None,
        gas_limit: int = None,
        gas_adjustment: float = 1.2,
        use_simulation: bool = True,
    ) -> BroadcastResult:
        """
        Delete provider attributes as an auditor.

        Args:
            wallet: AkashWallet instance (auditor wallet)
            owner: Provider owner address
            keys: List of attribute keys to delete
            memo: Transaction memo
            fee_amount: Transaction fee amount in uakt
            gas_limit: Gas limit
            gas_adjustment: Multiplier for gas estimation (default 1.2)
            use_simulation: Enable gas simulation

        Returns:
            BroadcastResult: Transaction result
        """
        try:
            logger.info(
                f"Deleting attributes for provider {owner} by auditor {wallet.address}"
            )

            msg = {
                "@type": "/akash.audit.v1.MsgDeleteProviderAttributes",
                "owner": owner,
                "auditor": wallet.address,
                "keys": keys,
            }

            return broadcast_transaction_rpc(
                client=self.akash_client,
                wallet=wallet,
                messages=[msg],
                memo=memo,
                fee_amount=fee_amount or "20000",
                gas_limit=gas_limit,
                gas_adjustment=gas_adjustment,
                use_simulation=use_simulation,
                wait_for_confirmation=True,
                confirmation_timeout=30,
            )

        except Exception as e:
            logger.error(f"Failed to delete provider attributes: {e}")
            return BroadcastResult(
                "", 1, f"Delete provider attributes failed: {str(e)}", False
            )
