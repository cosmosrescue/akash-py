import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class EscrowQuery:
    """
    Mixin for escrow query operations.
    """

    def get_blocks_remaining(self, owner: str, dseq: int) -> Dict[str, Any]:
        """
        Compute the number of blocks remaining for an escrow account.

        This method is for fetching deployment info, lease data, and calculating remaining blocks.

        Args:
            owner: Deployment owner address
            dseq: Deployment sequence number

        Returns:
            Dict[str, Any]: Blocks remaining calculation info or raises exception
        """
        try:
            import base64
            from decimal import Decimal
            from akash.proto.akash.market.v1beta5.query_pb2 import (
                QueryLeasesRequest,
                QueryLeasesResponse,
            )
            from akash.proto.akash.deployment.v1beta4.query_pb2 import (
                QueryDeploymentRequest,
                QueryDeploymentResponse,
            )

            logger.info(f"Computing blocks remaining for owner {owner}, dseq {dseq}")

            lease_request = QueryLeasesRequest()
            lease_request.filters.owner = owner
            lease_request.filters.dseq = dseq
            lease_request.filters.state = "active"

            request_bytes = lease_request.SerializeToString()
            request_hex = request_bytes.hex().upper()

            result = self.akash_client.abci_query(
                path="/akash.market.v1beta5.Query/Leases", data=request_hex
            )

            if not result or "response" not in result:
                raise Exception("Failed to fetch leases")

            response = result["response"]
            if response.get("code", 0) != 0 or not response.get("value"):
                raise Exception("No active leases found for deployment")

            response_data = base64.b64decode(response["value"])
            leases_response = QueryLeasesResponse()
            leases_response.ParseFromString(response_data)

            if len(leases_response.leases) == 0:
                raise Exception("No active leases found for deployment")

            total_lease_amount = Decimal("0")
            for lease_response in leases_response.leases:

                lease_price = lease_response.lease.price
                lease_price_raw = Decimal(lease_price.amount)
                lease_denom = lease_price.denom

                logger.info(f"Raw lease price: {lease_price_raw} {lease_denom}")

                chain_id = self.akash_client.chain_id

                if chain_id == "akashnet-2":

                    lease_price_base_units = lease_price_raw / Decimal(
                        "1000000000000000000"
                    )
                    logger.info(
                        f"Mainnet - converted lease price: {lease_price_raw} -> {lease_price_base_units}"
                    )
                else:
                    lease_price_base_units = lease_price_raw
                    logger.info(
                        f"Testnet - using lease price as base units: {lease_price_base_units}"
                    )

                if lease_denom == "uakt":
                    logger.info(f"Lease price: {lease_price_base_units} uakt per block")
                elif lease_denom.startswith("ibc/"):
                    logger.info(
                        f"Lease price: {lease_price_base_units} IBC tokens per block"
                    )
                else:
                    logger.info(
                        f"Lease price: {lease_price_base_units} {lease_denom} per block"
                    )

                logger.info(f"Lease price (base units): {lease_price_base_units}")

                total_lease_amount += lease_price_base_units

            logger.info(
                f"Total lease amount per block (base units): {total_lease_amount}"
            )

            deployment_request = QueryDeploymentRequest()
            deployment_request.id.owner = owner
            deployment_request.id.dseq = dseq

            request_bytes = deployment_request.SerializeToString()
            request_hex = request_bytes.hex().upper()

            result = self.akash_client.abci_query(
                path="/akash.deployment.v1beta4.Query/Deployment", data=request_hex
            )

            if not result or "response" not in result:
                raise Exception("Failed to fetch deployment")

            response = result["response"]
            if response.get("code", 0) != 0 or not response.get("value"):
                raise Exception("Deployment not found")

            response_data = base64.b64decode(response["value"])
            deployment_response = QueryDeploymentResponse()
            deployment_response.ParseFromString(response_data)

            status_result = self.akash_client.rpc_query("status", [])
            if not status_result or "sync_info" not in status_result:
                raise Exception("Failed to get blockchain status")

            current_height = int(status_result["sync_info"]["latest_block_height"])

            escrow_account = deployment_response.escrow_account
            settled_at = escrow_account.settled_at

            balance_amount = Decimal(escrow_account.balance.amount)
            funds_amount = Decimal(escrow_account.funds.amount)
            raw_total_balance = balance_amount + funds_amount
            escrow_denom = escrow_account.balance.denom

            logger.info(f"Escrow balance: {balance_amount} {escrow_denom}")
            logger.info(f"Escrow funds: {funds_amount} {escrow_denom}")
            logger.info(f"Raw total balance: {raw_total_balance} {escrow_denom}")
            logger.info(f"Current height: {current_height}, Settled at: {settled_at}")

            total_balance_base_units = raw_total_balance / Decimal(
                "1000000000000000000"
            )

            if escrow_denom == "uakt":
                logger.info(f"Total escrow balance (uakt): {total_balance_base_units}")
            elif escrow_denom.startswith("ibc/"):
                logger.info(
                    f"Total escrow balance ({escrow_denom}): {total_balance_base_units}"
                )
            else:
                logger.info(
                    f"Total escrow balance ({escrow_denom}): {total_balance_base_units}"
                )

            balance_remaining = float(total_balance_base_units) - (
                float(current_height - settled_at) * float(total_lease_amount)
            )
            logger.info(
                f"Balance remaining calculation: {total_balance_base_units} - ({current_height - settled_at} * {total_lease_amount}) = {balance_remaining}"
            )

            if float(total_lease_amount) > 0:
                blocks_remaining = int(balance_remaining / float(total_lease_amount))
            else:
                blocks_remaining = 0

            blocks_remaining = max(0, blocks_remaining)

            # Assuming 6 second block time
            estimated_time_seconds = blocks_remaining * 6

            result_data = {
                "balance_remaining": balance_remaining,
                "blocks_remaining": blocks_remaining,
                "estimated_time_remaining_seconds": estimated_time_seconds,
                "estimated_hours": estimated_time_seconds / 3600,
                "total_lease_amount_per_block": str(total_lease_amount),
                "current_height": current_height,
                "settled_at": settled_at,
                "escrow_balance_uakt": str(total_balance_base_units),
                "escrow_balance_raw": str(raw_total_balance),
                # 14400 blocks per day (6 sec blocks) - in uakt
                "daily_cost": str(total_lease_amount * 14400),
            }

            logger.info(
                f"Blocks remaining calculation complete: {blocks_remaining} blocks, {balance_remaining} balance"
            )
            return result_data

        except ImportError as e:
            logger.error(f"Escrow protobuf imports failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Get blocks remaining failed: {e}")
            raise
