import base64
import logging
import requests
from typing import Dict, List, Any, Optional

from akash.proto.akash.provider.v1beta4 import query_pb2 as provider_query_pb2
from akash.proto.cosmos.base.query.v1beta1 import pagination_pb2 as pagination_pb2
from ..market.query import MarketQuery

logger = logging.getLogger(__name__)


class ProviderQuery(MarketQuery):
    """
    Mixin for provider query operations.
    """

    def get_providers(
        self,
        limit: Optional[int] = 100,
        offset: Optional[int] = None,
        count_total: bool = False,
    ) -> List[Dict[str, Any]]:
        """
        Get registered providers via RPC query.

        Args:
            limit: Maximum number of providers to return (default: 100)
            offset: Number of results to skip (default: 0)
            count_total: Include total count in response (default: False)

        Returns:
            List of provider information dictionaries
        """
        try:
            logger.info(f"Querying providers (limit: {limit}, offset: {offset})")

            query = provider_query_pb2.QueryProvidersRequest()

            if limit is not None or offset is not None or count_total:
                pagination = pagination_pb2.PageRequest()
                if limit is not None:
                    pagination.limit = limit
                if offset is not None:
                    pagination.offset = offset
                if count_total:
                    pagination.count_total = count_total
                query.pagination.CopyFrom(pagination)

            query_path = "/akash.provider.v1beta4.Query/Providers"
            result = self.akash_client.rpc_query(
                "abci_query",
                [query_path, query.SerializeToString().hex().upper(), "0", False],
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
                logger.info("Query succeeded but returned no providers")
                return []

            response_bytes = base64.b64decode(response["value"])
            providers_response = provider_query_pb2.QueryProvidersResponse()
            providers_response.ParseFromString(response_bytes)

            providers = []
            for provider in providers_response.providers:
                providers.append(
                    {
                        "owner": provider.owner,
                        "host_uri": provider.host_uri,
                        "attributes": [
                            {"key": attr.key, "value": attr.value}
                            for attr in provider.attributes
                        ],
                        "info": {
                            "email": provider.info.email,
                            "website": provider.info.website,
                        },
                    }
                )

            logger.info(f"Found {len(providers)} providers")
            return providers

        except Exception as e:
            logger.error(f"Failed to list providers: {e}")
            raise

    def get_provider(self, owner_address: str) -> Dict[str, Any]:
        """
        Get specific provider information using proper ABCI query.

        Args:
            owner_address: Provider owner address

        Returns:
            Provider information dictionary
        """
        try:
            logger.info(f"Querying provider: {owner_address}")

            query = provider_query_pb2.QueryProviderRequest()
            query.owner = owner_address
            query_path = "/akash.provider.v1beta4.Query/Provider"

            result = self.akash_client.rpc_query(
                "abci_query",
                [query_path, query.SerializeToString().hex().upper(), "0", False],
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
                logger.info(f"Provider {owner_address} not found")
                return {}

            response_bytes = base64.b64decode(response["value"])
            provider_response = provider_query_pb2.QueryProviderResponse()
            provider_response.ParseFromString(response_bytes)

            provider = provider_response.provider
            return {
                "owner": provider.owner,
                "host_uri": provider.host_uri,
                "attributes": [
                    {"key": attr.key, "value": attr.value}
                    for attr in provider.attributes
                ],
                "info": {
                    "email": provider.info.email,
                    "website": provider.info.website,
                },
            }

        except Exception as e:
            logger.error(f"Failed to get provider {owner_address}: {e}")
            raise

    def _get_all_providers(self) -> List[Dict[str, Any]]:
        """
        Internal method to fetch all providers across all pages.

        Returns:
            List of all provider information dictionaries
        """
        all_providers = []
        offset = 0
        limit = 100

        while True:
            providers = self.get_providers(limit=limit, offset=offset)
            if not providers:
                break
            all_providers.extend(providers)
            if len(providers) < limit:
                break
            offset += limit

        return all_providers


    def get_provider_leases(self, owner_address: str) -> List[Dict[str, Any]]:
        """
        Get active leases for a provider.

        Args:
            owner_address: Provider owner address

        Returns:
            List of lease information
        """
        try:
            logger.info(f"Querying leases for provider: {owner_address}")

            leases = self.get_leases(owner=owner_address)
            return [
                {
                    "lease_id": f"{lease['lease_id']['owner']}/{lease['lease_id']['dseq']}/"
                    f"{lease['lease_id']['gseq']}/{lease['lease_id']['oseq']}",
                    "tenant": lease["lease_id"]["owner"],
                    "provider": lease["lease_id"]["provider"],
                    "state": lease["state"],
                    "price": {
                        "amount": lease["price"]["amount"],
                        "denom": lease["price"]["denom"],
                    },
                    "created_at": lease.get("created_at", 0),
                    "closed_on": lease.get("closed_on", 0),
                    "escrow_payment": lease.get("escrow_payment", {}),
                }
                for lease in leases
            ]

        except Exception as e:
            logger.error(f"Failed to get provider leases: {e}")
            raise

    def get_provider_version(self, owner_address: str, timeout: int = 5000) -> Optional[Dict[str, str]]:
        """
        Get provider version information via REST API.

        Args:
            owner_address: Provider owner address
            timeout: Timeout in milliseconds (default: 5000)

        Returns:
            Dict with version information:
            - version: Provider version string
            - cosmos_sdk_version: Cosmos SDK version string
            Returns None if the query fails.
        """
        try:
            logger.info(f"Querying provider version: {owner_address}")
            return self.akash_client.grpc_client._get_provider_version(owner_address, timeout)
        except Exception as e:
            logger.warning(f"Failed to get provider version for {owner_address}: {e}")
            return None

    def get_provider_status(self, owner_address: str) -> Dict[str, Any]:
        """
        Get provider status information via off-chain gRPC query with REST fallback.

        This method first attempts to query the provider's gRPC endpoint directly for real-time
        status information. If gRPC fails, it automatically falls back to REST API.

        Args:
            owner_address: Provider owner address

        Returns:
            Dict containing provider status information:
            - inventory: Available/pending/allocated resources per node
            - available_leases: Number of available leases
            - orders: Map of order states to counts
            - bids: Map of bid states to counts
            - leases: Map of lease states to counts
            - cluster: Cluster status information
            - bid_engine: Bid engine status
            - manifest: Manifest processing status
            - active_leases: Number of active leases

        Raises:
            Exception: If both gRPC and REST queries fail or provider endpoint cannot be reached
        """
        try:
            logger.info(f"Querying off-chain provider status: {owner_address}")

            result = self.akash_client.grpc_client.get_provider_status(
                provider_address=owner_address, insecure=True
            )

            if result.get("status") == "success":
                logger.info(
                    f"Successfully retrieved off-chain status for provider {owner_address} via gRPC"
                )
                return result.get("response", {})
            else:
                logger.warning(
                    f"gRPC failed for {owner_address}: {result.get('error', 'Unknown error')}, trying REST fallback..."
                )

        except Exception as grpc_error:
            logger.warning(
                f"gRPC failed for {owner_address}: {grpc_error}, trying REST fallback..."
            )

        try:
            provider = self.get_provider(owner_address)
            if not provider or not provider.get('host_uri'):
                error_msg = f"Provider {owner_address} has no host_uri for REST fallback"
                logger.error(error_msg)
                raise Exception(error_msg)

            host_uri = provider.get('host_uri')
            logger.info(f"Attempting REST fallback to {host_uri}/status")

            response = requests.get(f"{host_uri}/status", timeout=10, verify=False)

            if response.status_code == 200:
                logger.info(
                    f"Successfully retrieved off-chain status for provider {owner_address} via REST"
                )
                return response.json()
            else:
                error_msg = f"REST status failed with HTTP {response.status_code}"
                logger.error(error_msg)
                raise Exception(error_msg)

        except Exception as rest_error:
            error_msg = f"Both gRPC and REST failed for {owner_address}: {rest_error}"
            logger.error(error_msg)
            raise Exception(error_msg)

    def get_providers_by_region(
        self, region: str, include_status: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Get providers filtered by region attribute.

        Args:
            region: Region to filter by (e.g., 'United States', 'Europe', 'Asia', 'East Coast')
                   Performs case-insensitive substring matching
            include_status: Whether to include off-chain status for each provider

        Returns:
            List of providers in the specified region
        """
        try:
            logger.info(f"Getting providers in region: {region}")

            providers = self._get_all_providers()
            region_providers = []

            region_lower = region.lower()

            for provider in providers:
                if "attributes" in provider:
                    for attr in provider["attributes"]:
                        key = attr.get("key", "")
                        value = attr.get("value", "")

                        if key in ["location-region", "region", "country", "city"]:
                            if region_lower in value.lower():
                                provider_info = provider.copy()

                                if include_status:
                                    try:
                                        status = self.get_provider_status(provider["owner"])
                                        provider_info["status"] = status
                                    except Exception as e:
                                        logger.warning(
                                            f"Failed to get status for provider {provider['owner']}: {e}"
                                        )
                                        provider_info["status"] = None

                                region_providers.append(provider_info)
                                break

            logger.info(f"Found {len(region_providers)} providers in region {region}")
            return region_providers

        except Exception as e:
            error_msg = f"Failed to get providers by region {region}: {e}"
            logger.error(error_msg)
            raise Exception(error_msg)

    def get_providers_by_capabilities(
        self, capabilities: List[str], include_status: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Get providers filtered by required capabilities.

        Providers expose capabilities through attributes with keys like:
        - "feat-persistent-storage", "feat-endpoint-ip", "feat-endpoint-custom-domain"
        - "capabilities/storage/1/persistent", "capabilities/storage/1/class"

        Args:
            capabilities: List of required capability keys or partial matches
                         (e.g., ['feat-persistent-storage', 'feat-endpoint-ip'])
                         Performs case-insensitive substring matching
            include_status: Whether to include off-chain status for each provider

        Returns:
            List of providers that have all specified capabilities
        """
        try:
            logger.info(f"Getting providers with capabilities: {capabilities}")

            providers = self._get_all_providers()
            capable_providers = []

            capabilities_lower = [cap.lower() for cap in capabilities]

            for provider in providers:
                if "attributes" in provider:
                    provider_capabilities = set()

                    for attr in provider["attributes"]:
                        key = attr.get("key", "")
                        value = attr.get("value", "")

                        if key.startswith("feat-") and value.lower() == "true":
                            provider_capabilities.add(key.lower())

                        elif key.startswith("capabilities/") and value.lower() == "true":
                            provider_capabilities.add(key.lower())

                    has_all = True
                    for required_cap in capabilities_lower:
                        found = False
                        for provider_cap in provider_capabilities:
                            if required_cap in provider_cap or provider_cap in required_cap:
                                found = True
                                break
                        if not found:
                            has_all = False
                            break

                    if has_all:
                        provider_info = provider.copy()
                        provider_info["matched_capabilities"] = list(provider_capabilities)

                        if include_status:
                            try:
                                status = self.get_provider_status(provider["owner"])
                                provider_info["status"] = status
                            except Exception as e:
                                logger.warning(
                                    f"Failed to get status for provider {provider['owner']}: {e}"
                                )
                                provider_info["status"] = None

                        capable_providers.append(provider_info)

            logger.info(
                f"Found {len(capable_providers)} providers with capabilities {capabilities}"
            )
            return capable_providers

        except Exception as e:
            error_msg = f"Failed to get providers by capabilities {capabilities}: {e}"
            logger.error(error_msg)
            raise Exception(error_msg)

