import base64
import logging
from typing import Dict, List, Any, Optional

from akash.proto.akash.deployment.v1 import deployment_pb2 as deployment_pb
from akash.proto.akash.deployment.v1beta4 import filters_pb2
from akash.proto.akash.deployment.v1beta4 import query_pb2 as query_pb
from akash.proto.cosmos.base.query.v1beta1.pagination_pb2 import PageRequest

logger = logging.getLogger(__name__)


class DeploymentQuery:
    """
    Mixin for deployment query operations.
    """

    def get_deployments(
        self,
        owner: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        count_total: bool = False,
    ) -> List[Dict[str, Any]]:
        """
        List deployments using proper ABCI queries.

        Args:
            owner: Optional deployment owner filter
            limit: Maximum number of results to return
            offset: Number of results to skip
            count_total: Include total count in response

        Returns:
            List of deployments
        """
        try:
            logger.info(
                f"Querying deployments for owner: {owner or 'all'}, limit: {limit}, offset: {offset}"
            )

            query = query_pb.QueryDeploymentsRequest()
            if owner:
                filters = filters_pb2.DeploymentFilters(owner=owner)
                query.filters.CopyFrom(filters)

            if limit is not None or offset is not None or count_total:
                pagination = PageRequest()
                if limit is not None:
                    pagination.limit = limit
                if offset is not None:
                    pagination.offset = offset
                if count_total:
                    pagination.count_total = count_total
                query.pagination.CopyFrom(pagination)

            query_path = "/akash.deployment.v1beta4.Query/Deployments"
            query_data = query.SerializeToString()

            result = self.akash_client.abci_query(
                path=query_path, data=query_data.hex() if query_data else ""
            )

            if not result or "response" not in result:
                logger.error(f"Query failed: No response from {query_path}")
                return []

            response = result["response"]
            if response.get("code", -1) != 0:
                logger.error(
                    f"Query failed: {query_path} returned code {response.get('code')}: {response.get('log', 'Unknown error')}"
                )
                return []

            if "value" not in response or not response["value"]:
                logger.info("Query succeeded but returned no deployments")
                return []

            response_bytes = base64.b64decode(response["value"])
            deployment_response = query_pb.QueryDeploymentsResponse()
            deployment_response.ParseFromString(response_bytes)

            deployments = []
            for deployment_resp in deployment_response.deployments:
                deployment_dict = {
                    "deployment": {
                        "deployment_id": {
                            "owner": deployment_resp.deployment.deployment_id.owner,
                            "dseq": deployment_resp.deployment.deployment_id.dseq,
                        },
                        "state": deployment_resp.deployment.state,
                        "version": (
                            self._safe_decode_bytes(deployment_resp.deployment.version)
                            if deployment_resp.deployment.version
                            else ""
                        ),
                        "created_at": deployment_resp.deployment.created_at,
                    },
                    "groups": [
                        {
                            "group_id": {
                                "owner": group.group_id.owner,
                                "dseq": group.group_id.dseq,
                                "gseq": group.group_id.gseq,
                            },
                            "state": group.state,
                            "name": (
                                group.group_spec.name
                                if hasattr(group.group_spec, "name")
                                and group.group_spec.name
                                else ""
                            ),
                            "created_at": group.created_at,
                        }
                        for group in deployment_resp.groups
                    ],
                    "escrow_account": self._parse_escrow_account(
                        deployment_resp.escrow_account
                    ),
                }
                deployments.append(deployment_dict)

            logger.info(f"Found {len(deployments)} deployments")
            return deployments

        except Exception as e:
            logger.error(f"Deployment query failed: {e}")
            return []

    def get_deployment(self, owner: str, dseq: int) -> Dict[str, Any]:
        """
        Get deployment information using proper ABCI query.

        Args:
            owner: Deployment owner address
            dseq: Deployment sequence number

        Returns:
            Deployment information
        """
        try:
            logger.info(f"Querying deployment {dseq} for owner {owner}")

            deployment_id = deployment_pb.DeploymentID(owner=owner, dseq=dseq)
            query = query_pb.QueryDeploymentRequest(id=deployment_id)

            query_path = "/akash.deployment.v1beta4.Query/Deployment"
            query_data = query.SerializeToString()

            result = self.akash_client.abci_query(
                path=query_path, data=query_data.hex() if query_data else ""
            )

            if not result or "response" not in result:
                logger.error(f"Query failed: No response from {query_path}")
                return {}

            response = result["response"]
            if response.get("code", -1) != 0:
                logger.error(
                    f"Query failed: {query_path} returned code {response.get('code')}: {response.get('log', 'Unknown error')}"
                )
                return {}

            if "value" not in response or not response["value"]:
                logger.info(f"Query succeeded but deployment {owner}/{dseq} not found")
                return {}

            response_bytes = base64.b64decode(response["value"])
            deployment_info_response = query_pb.QueryDeploymentResponse()
            deployment_info_response.ParseFromString(response_bytes)

            deployment_info = {
                "deployment": {
                    "deployment_id": {
                        "owner": deployment_info_response.deployment.deployment_id.owner,
                        "dseq": deployment_info_response.deployment.deployment_id.dseq,
                    },
                    "state": deployment_info_response.deployment.state,
                    "version": (
                        self._safe_decode_bytes(
                            deployment_info_response.deployment.version
                        )
                        if deployment_info_response.deployment.version
                        else ""
                    ),
                    "created_at": deployment_info_response.deployment.created_at,
                },
                "groups": [
                    {
                        "group_id": {
                            "owner": group.group_id.owner,
                            "dseq": group.group_id.dseq,
                            "gseq": group.group_id.gseq,
                        },
                        "state": group.state,
                        "name": (
                            group.group_spec.name
                            if hasattr(group.group_spec, "name")
                            and group.group_spec.name
                            else ""
                        ),
                    }
                    for group in deployment_info_response.groups
                ],
                "escrow_account": self._parse_escrow_account(
                    deployment_info_response.escrow_account
                ),
            }

            logger.info(f"Successfully retrieved deployment {owner}/{dseq}")
            return deployment_info

        except Exception as e:
            logger.error(f"Failed to get deployment info: {e}")
            return {}

    def _parse_escrow_account(self, escrow_account):
        """
        Parse escrow account data consistently.

        Args:
            escrow_account: Escrow account protobuf object

        Returns:
            Dict: Parsed escrow account data
        """
        if not escrow_account:
            return None

        PRECISION = 1000000000000000000
        return {
            "balance": (
                str(int(escrow_account.balance.amount) // PRECISION)
                if escrow_account.balance
                else "0"
            ),
            "raw_balance": (
                escrow_account.balance.amount if escrow_account.balance else "0"
            ),
            "state": escrow_account.state,
        }
