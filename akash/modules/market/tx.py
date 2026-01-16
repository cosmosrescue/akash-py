import logging
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from akash.tx import BroadcastResult

logger = logging.getLogger(__name__)


class MarketTx:
    """Mixin for market transaction operations."""

    def create_bid(
        self,
        wallet,
        owner: str,
        dseq: int,
        gseq: int = 1,
        oseq: int = 1,
        price: str = "100",
        deposit: str = "5000000",
        denom: str = "uakt",
        memo: str = "",
        fee_amount: Optional[str] = None,
        gas_limit: Optional[int] = None,
        gas_adjustment: float = 1.2,
        use_simulation: bool = True,
    ) -> "BroadcastResult":
        try:
            from ...tx import broadcast_transaction_rpc, BroadcastResult

            logger.info(f"Creating bid for deployment {dseq}")

            msg_create_bid = {
                "@type": "/akash.market.v1beta5.MsgCreateBid",
                "order": {
                    "owner": owner,
                    "dseq": str(dseq),
                    "gseq": gseq,
                    "oseq": oseq,
                },
                "provider": wallet.address,
                "price": {"denom": denom, "amount": price},
                "deposit": {"denom": denom, "amount": deposit},
            }
            return broadcast_transaction_rpc(
                client=self.akash_client,
                wallet=wallet,
                messages=[msg_create_bid],
                memo=memo,
                fee_amount=fee_amount,
                gas_limit=gas_limit,
                gas_adjustment=gas_adjustment,
                use_simulation=use_simulation,
            )

        except Exception as e:
            logger.error(f"Failed to create bid: {e}")
            from ...tx import BroadcastResult

            return BroadcastResult("", 1, f"Bid creation failed: {e}", False)

    def close_bid(
        self,
        wallet,
        owner: str,
        dseq: int,
        gseq: int = 1,
        oseq: int = 1,
        provider: Optional[str] = None,
        memo: str = "",
        fee_amount: Optional[str] = None,
        gas_limit: Optional[int] = None,
        gas_adjustment: float = 1.2,
        use_simulation: bool = True,
    ) -> "BroadcastResult":
        """
        Close existing bid using unified broadcasting pattern.

        Args:
            wallet: AkashWallet instance (must be provider)
            provider: Provider address
            deployment_owner: Deployment owner address
            deployment_dseq: Deployment sequence number
            group_seq: Group sequence number
            order_seq: Order sequence number
            memo: Transaction memo
            fee_amount: Transaction fee amount (default: auto-calculated)
            gas_limit: Gas limit (default: 200000)
            gas_adjustment: Multiplier for gas estimation (default 1.2)
            use_simulation: Enable gas simulation (default: True)

        Returns:
            BroadcastResult with transaction details
        """
        try:
            from ...tx import broadcast_transaction_rpc, BroadcastResult

            final_provider = provider or wallet.address

            logger.info(f"Closing bid for deployment {dseq}")

            msg_close_bid = {
                "@type": "/akash.market.v1beta5.MsgCloseBid",
                "id": {
                    "owner": owner,
                    "dseq": str(dseq),
                    "gseq": gseq,
                    "oseq": oseq,
                    "provider": final_provider,
                },
            }
            return broadcast_transaction_rpc(
                client=self.akash_client,
                wallet=wallet,
                messages=[msg_close_bid],
                memo=memo,
                fee_amount=fee_amount,
                gas_limit=gas_limit,
                gas_adjustment=gas_adjustment,
                use_simulation=use_simulation,
            )

        except Exception as e:
            logger.error(f"Failed to close bid: {e}")
            from ...tx import BroadcastResult

            return BroadcastResult("", 1, f"Bid closure failed: {e}", False)

    def create_lease(
        self,
        wallet,
        owner: str,
        dseq: int,
        gseq: int = 1,
        oseq: int = 1,
        provider: Optional[str] = None,
        memo: str = "",
        fee_amount: Optional[str] = None,
        gas_limit: Optional[int] = None,
        gas_adjustment: float = 1.2,
        use_simulation: bool = True,
    ) -> "BroadcastResult":
        """
        Create lease from accepted bid using unified broadcasting pattern.

        Args:
            wallet: AkashWallet instance (must be deployment owner)
            provider: Provider address
            deployment_owner: Deployment owner address
            deployment_dseq: Deployment sequence number
            group_seq: Group sequence number
            order_seq: Order sequence number
            memo: Transaction memo
            fee_amount: Transaction fee amount (default: auto-calculated)
            gas_limit: Gas limit (default: 200000)
            gas_adjustment: Multiplier for gas estimation (default 1.2)
            use_simulation: Enable gas simulation (default: True)

        Returns:
            BroadcastResult with transaction details
        """
        try:
            from ...tx import broadcast_transaction_rpc, BroadcastResult

            logger.info(f"Creating lease for deployment {dseq}")

            msg_create_lease = {
                "@type": "/akash.market.v1beta5.MsgCreateLease",
                "owner": owner,
                "dseq": dseq,
                "gseq": gseq,
                "oseq": oseq,
                "provider": provider,
            }

            return broadcast_transaction_rpc(
                client=self.akash_client,
                wallet=wallet,
                messages=[msg_create_lease],
                memo=memo,
                fee_amount=fee_amount,
                gas_limit=gas_limit,
                gas_adjustment=gas_adjustment,
                use_simulation=use_simulation,
            )

        except Exception as e:
            logger.error(f"Failed to create lease: {e}")
            from ...tx import BroadcastResult

            return BroadcastResult("", 1, f"Lease creation failed: {e}", False)

    def close_lease(
        self,
        wallet,
        owner: str,
        dseq: int,
        gseq: int = 1,
        oseq: int = 1,
        provider: Optional[str] = None,
        memo: str = "",
        fee_amount: Optional[str] = None,
        gas_limit: Optional[int] = None,
        gas_adjustment: float = 1.2,
        use_simulation: bool = True,
    ) -> "BroadcastResult":
        """
        Close active lease using unified broadcasting pattern.

        Args:
            wallet: AkashWallet instance (owner or provider)
            provider: Provider address
            deployment_owner: Deployment owner address
            deployment_dseq: Deployment sequence number
            group_seq: Group sequence number
            order_seq: Order sequence number
            memo: Transaction memo
            fee_amount: Transaction fee amount (default: auto-calculated)
            gas_limit: Gas limit (default: 200000)
            gas_adjustment: Multiplier for gas estimation (default 1.2)
            use_simulation: Enable gas simulation (default: True)

        Returns:
            BroadcastResult with transaction details
        """
        try:
            from ...tx import broadcast_transaction_rpc, BroadcastResult

            logger.info(f"Closing lease for deployment {dseq}")

            msg_close_lease = {
                "@type": "/akash.market.v1beta5.MsgCloseLease",
                "id": {
                    "owner": owner,
                    "dseq": str(dseq),
                    "gseq": gseq,
                    "oseq": oseq,
                    "provider": provider,
                },
            }

            return broadcast_transaction_rpc(
                client=self.akash_client,
                wallet=wallet,
                messages=[msg_close_lease],
                memo=memo,
                fee_amount=fee_amount,
                gas_limit=gas_limit,
                gas_adjustment=gas_adjustment,
                use_simulation=use_simulation,
            )

        except Exception as e:
            logger.error(f"Failed to close lease: {e}")
            from ...tx import BroadcastResult

            return BroadcastResult("", 1, f"Lease closure failed: {e}", False)

    def withdraw_lease(
        self,
        wallet,
        owner: str,
        dseq: int,
        gseq: int = 1,
        oseq: int = 1,
        provider: Optional[str] = None,
        memo: str = "",
        fee_amount: Optional[str] = None,
        gas_limit: Optional[int] = None,
        gas_adjustment: float = 1.2,
        use_simulation: bool = True,
    ) -> "BroadcastResult":
        """
        Withdraw funds from closed lease escrow using unified broadcasting pattern.

        Args:
            wallet: AkashWallet instance (must be deployment owner)
            provider: Provider address
            deployment_owner: Deployment owner address
            deployment_dseq: Deployment sequence number
            group_seq: Group sequence number
            order_seq: Order sequence number
            memo: Transaction memo
            fee_amount: Transaction fee amount (default: auto-calculated)
            gas_limit: Gas limit (default: 200000)
            gas_adjustment: Multiplier for gas estimation (default 1.2)
            use_simulation: Enable gas simulation (default: True)

        Returns:
            BroadcastResult with transaction details
        """
        try:
            from ...tx import broadcast_transaction_rpc, BroadcastResult

            logger.info(f"Withdrawing from lease for deployment {dseq}")

            msg_withdraw_lease = {
                "@type": "/akash.market.v1beta5.MsgWithdrawLease",
                "id": {
                    "owner": owner,
                    "dseq": str(dseq),
                    "gseq": gseq,
                    "oseq": oseq,
                    "provider": provider,
                },
            }

            return broadcast_transaction_rpc(
                client=self.akash_client,
                wallet=wallet,
                messages=[msg_withdraw_lease],
                memo=memo,
                fee_amount=fee_amount,
                gas_limit=gas_limit,
                gas_adjustment=gas_adjustment,
                use_simulation=use_simulation,
            )

        except Exception as e:
            logger.error(f"Failed to withdraw from lease: {e}")
            from ...tx import BroadcastResult

            return BroadcastResult("", 1, f"Lease withdrawal failed: {e}", False)
