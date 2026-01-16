from typing import Any, Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class MarketUtils:
    """
    Mixin for market utilities.
    """

    def create_lease_from_bid(
        self,
        wallet,
        bid: Dict,
        fee_amount: str = "100000",
        gas_adjustment: float = 1.4
    ) -> Dict[str, Any]:
        """
        Create lease from a bid.
        Simplifies lease creation process.

        Args:
            wallet: AkashWallet instance
            bid: Bid dictionary
            fee_amount: Transaction fee
            gas_adjustment: Gas adjustment multiplier

        Returns:
            Dict with lease creation result
        """
        try:
            if 'bid' in bid:
                bid_id = bid['bid']['bid_id']
            else:
                bid_id = bid['bid_id']

            if hasattr(self, 'akash_client'):
                result = self.akash_client.market.create_lease(
                    wallet=wallet,
                    owner=bid_id['owner'],
                    dseq=bid_id['dseq'],
                    gseq=bid_id['gseq'],
                    oseq=bid_id['oseq'],
                    provider=bid_id['provider'],
                    fee_amount=fee_amount,
                    gas_adjustment=gas_adjustment
                )

                if result.success:
                    provider_info = self.akash_client.provider.get_provider(bid_id['provider'])
                    provider_endpoint = provider_info.get('host_uri', '')

                    return {
                        "success": True,
                        "lease_id": bid_id,
                        "provider": bid_id['provider'],
                        "provider_endpoint": provider_endpoint,
                        "tx_hash": result.tx_hash
                    }
                else:
                    return {
                        "success": False,
                        "error": result.raw_log
                    }
            else:
                raise ValueError("This method requires an initialized AkashClient")

        except Exception as e:
            logger.error(f"Lease creation failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def _create_bid_msg(
        self,
        provider: str,
        deployment_owner: str,
        deployment_dseq: str,
        group_seq: str,
        order_seq: str,
        price: str,
    ) -> Dict[str, Any]:
        """Create bid message for testing."""
        return {
            "@type": "/akash.market.v1beta5.MsgCreateBid",
            "id": {
                "owner": deployment_owner,
                "dseq": deployment_dseq,
                "gseq": group_seq,
                "oseq": order_seq,
                "provider": provider,
            },
            "price": {"amount": price.replace("uakt", ""), "denom": "uakt"},
            "deposit": {"amount": price.replace("uakt", ""), "denom": "uakt"},
        }

    def _create_close_bid_msg(
        self,
        provider: str,
        deployment_owner: str,
        deployment_dseq: str,
        group_seq: str,
        order_seq: str,
    ) -> Dict[str, Any]:
        """Create close bid message for testing."""
        return {
            "@type": "/akash.market.v1beta5.MsgCloseBid",
            "id": {
                "owner": deployment_owner,
                "dseq": deployment_dseq,
                "gseq": group_seq,
                "oseq": order_seq,
                "provider": provider,
            },
        }

    def _create_lease_msg(
        self,
        provider: str,
        deployment_owner: str,
        deployment_dseq: str,
        group_seq: str,
        order_seq: str,
    ) -> Dict[str, Any]:
        """Create lease message for testing."""
        return {
            "@type": "/akash.market.v1beta5.MsgCreateLease",
            "id": {
                "owner": deployment_owner,
                "dseq": deployment_dseq,
                "gseq": group_seq,
                "oseq": order_seq,
                "provider": provider,
            },
        }

    def _create_close_lease_msg(
        self,
        provider: str,
        deployment_owner: str,
        deployment_dseq: str,
        group_seq: str,
        order_seq: str,
    ) -> Dict[str, Any]:
        """Create close lease message for testing."""
        return {
            "@type": "/akash.market.v1beta5.MsgCloseLease",
            "id": {
                "owner": deployment_owner,
                "dseq": deployment_dseq,
                "gseq": group_seq,
                "oseq": order_seq,
                "provider": provider,
            },
        }

    def _create_withdraw_lease_msg(
        self,
        provider: str,
        deployment_owner: str,
        deployment_dseq: str,
        group_seq: str,
        order_seq: str,
    ) -> Dict[str, Any]:
        """Create withdraw lease message for testing."""
        return {
            "@type": "/akash.market.v1beta5.MsgWithdrawLease",
            "id": {
                "owner": deployment_owner,
                "dseq": deployment_dseq,
                "gseq": group_seq,
                "oseq": order_seq,
                "provider": provider,
            },
        }
