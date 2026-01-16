import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class MarketQuery:
    """
    Mixin for market query operations.
    """

    def get_orders(
        self,
        owner: Optional[str] = None,
        state: Optional[str] = None,
        dseq: Optional[int] = None,
        gseq: Optional[int] = None,
        oseq: Optional[int] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        count_total: bool = False,
    ) -> List[Dict[str, Any]]:
        """
        Get deployment orders available for bidding using proper ABCI query.

        Args:
            owner: Filter by deployment owner
            state: Filter by order state ("open", "active", "closed")
            dseq: Filter by deployment sequence number
            gseq: Filter by group sequence number
            oseq: Filter by order sequence number
            limit: Maximum number of results to return (default: no limit)
            offset: Number of results to skip (default: 0)
            count_total: Include total count in response (default: False)

        Returns:
            List of order information with state as integer (1=open, 2=active, 3=closed)
        """
        try:
            from akash.proto.akash.market.v1beta5.query_pb2 import QueryOrdersRequest
            # v1beta5: OrderFilters moved to filters_pb2
            from akash.proto.akash.market.v1beta5.filters_pb2 import OrderFilters
            from akash.proto.cosmos.base.query.v1beta1.pagination_pb2 import PageRequest

            logger.info(
                f"Querying orders for owner: {owner or 'all'}, state: {state or 'all'}, dseq: {dseq or 'all'}, limit: {limit}"
            )

            query = QueryOrdersRequest()

            if owner or state or dseq or gseq or oseq:
                filters = OrderFilters()
                if owner:
                    filters.owner = owner
                if state:
                    filters.state = state
                if dseq:
                    filters.dseq = dseq
                if gseq:
                    filters.gseq = gseq
                if oseq:
                    filters.oseq = oseq
                query.filters.CopyFrom(filters)

            if limit is not None or offset is not None or count_total:
                pagination = PageRequest()
                if limit is not None:
                    pagination.limit = limit
                if offset is not None:
                    pagination.offset = offset
                pagination.count_total = count_total
                query.pagination.CopyFrom(pagination)

            query_path = "/akash.market.v1beta5.Query/Orders"
            query_data = query.SerializeToString()

            result = self.akash_client.abci_query(
                path=query_path, data=query_data.hex() if query_data else ""
            )

            if not result or "response" not in result:
                error_msg = f"Query failed: No response from {query_path}"
                logger.error(error_msg)
                raise Exception(error_msg)

            response = result["response"]
            response_code = response.get("code", -1)

            if response_code != 0:
                error_msg = f"Query failed: {query_path} returned code {response_code}: {response.get('log', 'Unknown error')}"
                logger.error(error_msg)
                raise Exception(error_msg)

            if "value" not in response or not response["value"]:
                logger.info("Query succeeded but returned no orders (empty result)")
                return []

            from akash.proto.akash.market.v1beta5.query_pb2 import QueryOrdersResponse
            import base64

            try:
                response_bytes = base64.b64decode(response["value"])
                orders_response = QueryOrdersResponse()
                orders_response.ParseFromString(response_bytes)

                orders = []
                for order in orders_response.orders:
                    order_dict = {
                        "order_id": {
                            "owner": order.order_id.owner,
                            "dseq": order.order_id.dseq,
                            "gseq": order.order_id.gseq,
                            "oseq": order.order_id.oseq,
                        },
                        "state": order.state,
                        "spec": {
                            "name": (
                                order.spec.name if hasattr(order.spec, "name") else ""
                            ),
                            "requirements": (
                                order.spec.requirements
                                if hasattr(order.spec, "requirements")
                                else {}
                            ),
                        },
                        "created_at": (
                            order.created_at if hasattr(order, "created_at") else 0
                        ),
                    }
                    orders.append(order_dict)

                logger.info(f"Found {len(orders)} orders")
                return orders

            except Exception as parse_error:
                error_msg = f"Failed to parse orders response: {parse_error}"
                logger.error(error_msg)
                raise Exception(error_msg)

        except ImportError as e:
            logger.error(f"Failed to import market protobuf: {e}")
            raise ImportError(f"Protobuf import failed - cannot get orders: {e}")
        except Exception as e:
            logger.error(f"Order query failed: {e}")
            raise

    def get_bids(
        self,
        provider: Optional[str] = None,
        owner: Optional[str] = None,
        state: Optional[str] = None,
        dseq: Optional[int] = None,
        gseq: Optional[int] = None,
        oseq: Optional[int] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        count_total: bool = False,
    ) -> List[Dict[str, Any]]:
        """
        Get bids submitted by providers using proper ABCI query.

        Args:
            provider: Filter by provider address
            owner: Filter by deployment owner
            state: Filter by bid state ("open", "active", "lost", "closed")
            dseq: Filter by deployment sequence number
            gseq: Filter by group sequence number
            oseq: Filter by order sequence number
            limit: Maximum number of results to return (default: no limit)
            offset: Number of results to skip (default: 0)
            count_total: Include total count in response (default: False)

        Returns:
            List of bid information
        """
        try:
            from akash.proto.akash.market.v1beta5.query_pb2 import QueryBidsRequest
            # v1beta5: BidFilters moved to filters_pb2
            from akash.proto.akash.market.v1beta5.filters_pb2 import BidFilters
            from akash.proto.cosmos.base.query.v1beta1.pagination_pb2 import PageRequest

            logger.info(
                f"Querying bids for provider: {provider or 'all'}, owner: {owner or 'all'}, dseq: {dseq or 'all'}, limit: {limit}"
            )

            query = QueryBidsRequest()

            if provider or owner or state or dseq or gseq or oseq:
                filters = BidFilters()
                if provider:
                    filters.provider = provider
                if owner:
                    filters.owner = owner
                if state:
                    filters.state = state
                if dseq:
                    filters.dseq = dseq
                if gseq:
                    filters.gseq = gseq
                if oseq:
                    filters.oseq = oseq
                query.filters.CopyFrom(filters)

            if limit is not None or offset is not None or count_total:
                pagination = PageRequest()
                if limit is not None:
                    pagination.limit = limit
                if offset is not None:
                    pagination.offset = offset
                pagination.count_total = count_total
                query.pagination.CopyFrom(pagination)

            query_path = "/akash.market.v1beta5.Query/Bids"
            query_data = query.SerializeToString()

            result = self.akash_client.abci_query(
                path=query_path, data=query_data.hex() if query_data else ""
            )

            if not result or "response" not in result:
                error_msg = f"Query failed: No response from {query_path}"
                logger.error(error_msg)
                raise Exception(error_msg)

            response = result["response"]
            response_code = response.get("code", -1)

            if response_code != 0:
                error_msg = f"Query failed: {query_path} returned code {response_code}: {response.get('log', 'Unknown error')}"
                logger.error(error_msg)
                raise Exception(error_msg)

            if "value" not in response or not response["value"]:
                logger.info("Query succeeded but returned no bids (empty result)")
                return []

            from akash.proto.akash.market.v1beta5.query_pb2 import QueryBidsResponse
            import base64

            try:
                response_bytes = base64.b64decode(response["value"])
                bids_response = QueryBidsResponse()
                bids_response.ParseFromString(response_bytes)

                bids = []
                for bid in bids_response.bids:
                    bid_dict = {
                        "bid_id": {
                            "owner": bid.bid.bid_id.owner,
                            "dseq": bid.bid.bid_id.dseq,
                            "gseq": bid.bid.bid_id.gseq,
                            "oseq": bid.bid.bid_id.oseq,
                            "provider": bid.bid.bid_id.provider,
                        },
                        "state": bid.bid.state,
                        "price": {
                            "denom": (
                                bid.bid.price.denom
                                if hasattr(bid.bid.price, "denom")
                                else "uakt"
                            ),
                            "amount_raw": (
                                bid.bid.price.amount
                                if hasattr(bid.bid.price, "amount")
                                else "0"
                            ),
                            "amount": self._convert_price_amount(
                                bid.bid.price.amount
                                if hasattr(bid.bid.price, "amount")
                                else "0"
                            ),
                        },
                        "created_at": (
                            bid.bid.created_at if hasattr(bid.bid, "created_at") else 0
                        ),
                        "escrow_account": (
                            {
                                "balance": (
                                    bid.escrow_account.balance.amount
                                    if bid.escrow_account and bid.escrow_account.balance
                                    else "0"
                                ),
                                "state": (
                                    bid.escrow_account.state
                                    if bid.escrow_account
                                    else 0
                                ),
                            }
                            if hasattr(bid, "escrow_account")
                            else None
                        ),
                    }
                    bids.append(bid_dict)

                logger.info(f"Found {len(bids)} bids")
                return bids

            except Exception as parse_error:
                error_msg = f"Failed to parse bids response: {parse_error}"
                logger.error(error_msg)
                raise Exception(error_msg)

        except ImportError as e:
            logger.error(f"Failed to import market protobuf: {e}")
            raise ImportError(f"Protobuf import failed - cannot get orders: {e}")
        except Exception as e:
            logger.error(f"Bid query failed: {e}")
            raise

    def _convert_price_amount(self, raw_amount: str) -> str:
        """
        Convert raw bid price amount to standard uakt units.

        - Mainnet (akashnet-2): 18 decimal precision
        - Testnet: Raw amount (6 decimal precision)
        
        Args:
            raw_amount: Raw price amount from blockchain
            
        Returns:
            Converted amount as string in standard uakt units
        """
        try:
            from decimal import Decimal
            
            if not raw_amount or raw_amount == "0":
                return "0"
            
            raw_decimal = Decimal(raw_amount)
            chain_id = getattr(self.akash_client, 'chain_id', '')
            
            if chain_id == "akashnet-2":
                converted = raw_decimal / Decimal("1000000000000000000")
            else:
                converted = raw_decimal
                
            return str(converted)
            
        except (ValueError, TypeError, AttributeError):
            logger.warning(f"Failed to convert price amount: {raw_amount}")
            return raw_amount

    def get_leases(
        self,
        provider: Optional[str] = None,
        owner: Optional[str] = None,
        state: Optional[str] = None,
        dseq: Optional[int] = None,
        gseq: Optional[int] = None,
        oseq: Optional[int] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        count_total: bool = False,
    ) -> List[Dict[str, Any]]:
        """
        Get leases using proper ABCI query.

        Args:
            provider: Filter by provider address
            owner: Filter by deployment owner
            state: Filter by lease state ("active", "insufficient_funds", "closed")
            dseq: Filter by deployment sequence number
            gseq: Filter by group sequence number
            oseq: Filter by order sequence number
            limit: Maximum number of results to return (default: no limit)
            offset: Number of results to skip (default: 0)
            count_total: Include total count in response (default: False)

        Returns:
            List of lease information with state converted to string
        """
        try:
            from akash.proto.akash.market.v1beta5.query_pb2 import QueryLeasesRequest
            # v1beta5: QueryLeasesRequest uses v1.LeaseFilters (not v1beta5)
            from akash.proto.akash.market.v1.filters_pb2 import LeaseFilters
            from akash.proto.cosmos.base.query.v1beta1.pagination_pb2 import PageRequest

            logger.info(
                f"Querying leases for provider: {provider or 'all'}, owner: {owner or 'all'}, dseq: {dseq or 'all'}, limit: {limit}"
            )

            query = QueryLeasesRequest()

            if provider or owner or state or dseq or gseq or oseq:
                filters = LeaseFilters()
                if provider:
                    filters.provider = provider
                if owner:
                    filters.owner = owner
                if state:
                    filters.state = state
                if dseq:
                    filters.dseq = dseq
                if gseq:
                    filters.gseq = gseq
                if oseq:
                    filters.oseq = oseq
                query.filters.CopyFrom(filters)

            if limit is not None or offset is not None or count_total:
                pagination = PageRequest()
                if limit is not None:
                    pagination.limit = limit
                if offset is not None:
                    pagination.offset = offset
                pagination.count_total = count_total
                query.pagination.CopyFrom(pagination)

            query_path = "/akash.market.v1beta5.Query/Leases"
            query_data = query.SerializeToString()

            result = self.akash_client.abci_query(
                path=query_path, data=query_data.hex() if query_data else ""
            )

            if not result or "response" not in result:
                error_msg = f"Query failed: No response from {query_path}"
                logger.error(error_msg)
                raise Exception(error_msg)

            response = result["response"]
            response_code = response.get("code", -1)

            if response_code != 0:
                error_msg = f"Query failed: {query_path} returned code {response_code}: {response.get('log', 'Unknown error')}"
                logger.error(error_msg)
                raise Exception(error_msg)

            if "value" not in response or not response["value"]:
                logger.info("Query succeeded but returned no leases (empty result)")
                return []

            from akash.proto.akash.market.v1beta5.query_pb2 import QueryLeasesResponse
            import base64

            try:
                response_bytes = base64.b64decode(response["value"])
                leases_response = QueryLeasesResponse()
                leases_response.ParseFromString(response_bytes)

                leases = []
                state_mapping = {1: "active", 2: "insufficient_funds", 3: "closed"}

                for lease in leases_response.leases:
                    state_int = lease.lease.state
                    state_str = state_mapping.get(state_int, f"unknown({state_int})")

                    lease_dict = {
                        "lease_id": {
                            "owner": lease.lease.lease_id.owner,
                            "dseq": lease.lease.lease_id.dseq,
                            "gseq": lease.lease.lease_id.gseq,
                            "oseq": lease.lease.lease_id.oseq,
                            "provider": lease.lease.lease_id.provider,
                        },
                        "state": state_str,
                        "price": {
                            "denom": (
                                lease.lease.price.denom
                                if hasattr(lease.lease.price, "denom")
                                else "uakt"
                            ),
                            "amount": (
                                lease.lease.price.amount
                                if hasattr(lease.lease.price, "amount")
                                else "0"
                            ),
                        },
                        "created_at": (
                            lease.lease.created_at
                            if hasattr(lease.lease, "created_at")
                            else 0
                        ),
                        "closed_on": (
                            lease.lease.closed_on
                            if hasattr(lease.lease, "closed_on")
                            else 0
                        ),
                        "escrow_payment": (
                            {
                                "balance": (
                                    lease.escrow_payment.balance.amount
                                    if lease.escrow_payment
                                    and lease.escrow_payment.balance
                                    else "0"
                                ),
                                "state": (
                                    lease.escrow_payment.state
                                    if lease.escrow_payment
                                    else 0
                                ),
                                "withdrawn": (
                                    lease.escrow_payment.withdrawn.amount
                                    if lease.escrow_payment
                                    and hasattr(lease.escrow_payment, "withdrawn")
                                    else "0"
                                ),
                            }
                            if hasattr(lease, "escrow_payment")
                            else None
                        ),
                    }
                    leases.append(lease_dict)

                logger.info(f"Found {len(leases)} leases")
                return leases

            except Exception as parse_error:
                error_msg = f"Failed to parse leases response: {parse_error}"
                logger.error(error_msg)
                raise Exception(error_msg)

        except ImportError as e:
            logger.error(f"Failed to import market protobuf: {e}")
            raise ImportError(f"Protobuf import failed - cannot get orders: {e}")
        except Exception as e:
            logger.error(f"Lease query failed: {e}")
            raise

    def get_order(
        self, owner: str, dseq: int, gseq: int = 1, oseq: int = 1
    ) -> Optional[Dict[str, Any]]:
        """Get a specific order by ID."""
        try:
            orders = self.get_orders(
                owner=owner, dseq=dseq, gseq=gseq, oseq=oseq, limit=1
            )
            return orders[0] if orders else None
        except Exception as e:
            logger.error(f"Failed to get order {owner}/{dseq}/{gseq}/{oseq}: {e}")
            return None
