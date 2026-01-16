import logging
from typing import Dict, List, Any, Optional

from ...tx import BroadcastResult, broadcast_transaction_rpc

logger = logging.getLogger(__name__)


class ProviderTx:
    """
    Mixin for provider transaction operations.
    """

    def create_provider(
        self,
        wallet,
        host_uri: str,
        email: str = "",
        website: str = "",
        attributes: List[Dict[str, Any]] = None,
        memo: str = "",
        fee_amount: Optional[str] = None,
        gas_limit: Optional[int] = None,
        gas_adjustment: float = 1.2,
        use_simulation: bool = True,
    ) -> BroadcastResult:
        """
        Register a new provider on Akash Network.

        Args:
            wallet: AkashWallet instance of the provider operator
            host_uri: Provider host URI
            email: Provider email
            website: Provider website
            attributes: Provider attributes list
            memo: Transaction memo
            fee_amount: Transaction fee amount
            gas_limit: Gas limit
            gas_adjustment: Multiplier for gas estimation (default 1.2)
            use_simulation: Enable gas simulation

        Returns:
            BroadcastResult with transaction details
        """
        try:
            logger.info(f"Creating provider for {wallet.address}")

            msg_create_provider = {
                "@type": "/akash.provider.v1beta4.MsgCreateProvider",
                "owner": wallet.address,
                "host_uri": host_uri,
                "attributes": [
                    {"key": attr["key"], "value": attr["value"]}
                    for attr in (attributes or [])
                ],
                "info": {"email": email, "website": website},
            }

            return broadcast_transaction_rpc(
                client=self.akash_client,
                wallet=wallet,
                messages=[msg_create_provider],
                memo=memo,
                fee_amount=fee_amount or "5000",
                gas_limit=gas_limit,
                gas_adjustment=gas_adjustment,
                use_simulation=use_simulation,
                wait_for_confirmation=True,
                confirmation_timeout=30,
            )

        except Exception as e:
            logger.error(f"Failed to create provider: {e}")
            return BroadcastResult("", 1, f"Create provider failed: {e}", False)

    def update_provider(
        self,
        wallet,
        host_uri: str,
        email: str = "",
        website: str = "",
        attributes: List[Dict[str, Any]] = None,
        memo: str = "",
        fee_amount: Optional[str] = None,
        gas_limit: Optional[int] = None,
        gas_adjustment: float = 1.2,
        use_simulation: bool = True,
    ) -> BroadcastResult:
        """
        Update existing provider information.

        Args:
            wallet: AkashWallet instance of the provider operator
            host_uri: Provider host URI
            email: Provider email
            website: Provider website
            attributes: Provider attributes list
            memo: Transaction memo
            fee_amount: Transaction fee amount
            gas_limit: Gas limit
            gas_adjustment: Multiplier for gas estimation (default 1.2)
            use_simulation: Enable gas simulation

        Returns:
            BroadcastResult with transaction details
        """
        try:
            logger.info(f"Updating provider for {wallet.address}")

            msg_update_provider = {
                "@type": "/akash.provider.v1beta4.MsgUpdateProvider",
                "owner": wallet.address,
                "host_uri": host_uri,
                "attributes": [
                    {"key": attr["key"], "value": attr["value"]}
                    for attr in (attributes or [])
                ],
                "info": {"email": email, "website": website},
            }

            return broadcast_transaction_rpc(
                client=self.akash_client,
                wallet=wallet,
                messages=[msg_update_provider],
                memo=memo,
                fee_amount=fee_amount or "5000",
                gas_limit=gas_limit,
                gas_adjustment=gas_adjustment,
                use_simulation=use_simulation,
                wait_for_confirmation=True,
                confirmation_timeout=30,
            )

        except Exception as e:
            logger.error(f"Failed to update provider: {e}")
            return BroadcastResult("", 1, f"Update provider failed: {e}", False)
