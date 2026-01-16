import base64
import logging
from typing import Dict, List, Any, Optional

from akash.proto.akash.audit.v1 import query_pb2 as audit_query_pb2
from akash.proto.cosmos.base.query.v1beta1 import pagination_pb2 as pagination_pb2

logger = logging.getLogger(__name__)


class AuditQuery:
    """
    Mixin for audit query operations.
    """

    def get_providers(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        count_total: bool = False,
    ) -> List[Dict]:
        """
        Query for all providers with audit attributes.

        Args:
            limit: Maximum number of results to return
            offset: Number of results to skip
            count_total: Include total count in response

        Returns:
            List[Dict]: List of provider attribute records
        """
        try:
            logger.info("Querying all providers attributes")

            request = audit_query_pb2.QueryAllProvidersAttributesRequest()

            # Add pagination if specified
            if limit is not None or offset is not None or count_total:
                page_request = pagination_pb2.PageRequest()
                if limit is not None:
                    page_request.limit = limit
                if offset is not None:
                    page_request.offset = offset
                if count_total:
                    page_request.count_total = count_total
                request.pagination.CopyFrom(page_request)

            path = "/akash.audit.v1.Query/AllProvidersAttributes"
            result = self.akash_client.rpc_query(
                "abci_query",
                [path, request.SerializeToString().hex().upper(), "0", False],
            )

            if not result or "response" not in result:
                logger.error(f"Query failed: No response from {path}")
                raise Exception(f"RPC query failed: No response from {path}")

            response = result["response"]
            response_code = response.get("code", -1)
            if response_code != 0:
                if response_code == 5:
                    logger.info("Query succeeded but returned no attributes")
                    return []
                else:
                    error_log = response.get("log", "Unknown error")
                    logger.error(f"Query failed with code {response_code}: {error_log}")
                    raise Exception(f"Query failed: {error_log}")

            if not response.get("value"):
                logger.info("Query succeeded but returned no attributes")
                return []

            response_bytes = base64.b64decode(response["value"])
            response = audit_query_pb2.QueryProvidersResponse()
            response.ParseFromString(response_bytes)

            providers = []
            for provider in response.providers:
                provider_info = {
                    "owner": provider.owner,
                    "auditor": provider.auditor,
                    "attributes": [
                        {"key": attr.key, "value": attr.value}
                        for attr in provider.attributes
                    ],
                }
                providers.append(provider_info)

            logger.info(f"Found {len(providers)} provider attribute records")
            return providers

        except Exception as e:
            logger.error(f"Failed to get all providers attributes: {e}")
            raise

    def get_provider(self, owner: str, auditor: str) -> Dict[str, Any]:
        """
        Query provider audit attributes by owner and auditor.

        Args:
            owner: Provider owner address
            auditor: Auditor address

        Returns:
            Dict[str, Any]: Provider audit attribute record or empty dict if not found
        """
        try:
            providers = self.get_provider_auditor_attributes(auditor, owner)
            if providers:
                return providers[0]  # First match
            return {}
        except Exception as e:
            logger.error(
                f"Failed to get provider audit attributes for {owner}/{auditor}: {e}"
            )
            raise

    def get_provider_attributes(
        self, owner: str, pagination: Dict = None
    ) -> List[Dict]:
        """
        Get attributes for a specific provider.

        Args:
            owner: Provider owner address
            pagination: Optional pagination parameters

        Returns:
            List[Dict]: List of provider attribute records
        """
        try:
            logger.info(f"Querying provider attributes for {owner}")

            request = audit_query_pb2.QueryProviderAttributesRequest()
            request.owner = owner
            if pagination:
                page_request = pagination_pb2.PageRequest()
                if "limit" in pagination:
                    page_request.limit = pagination["limit"]
                if "offset" in pagination:
                    page_request.offset = pagination["offset"]
                if "key" in pagination:
                    page_request.key = pagination["key"]
                request.pagination.CopyFrom(page_request)

            path = "/akash.audit.v1.Query/ProviderAttributes"
            result = self.akash_client.rpc_query(
                "abci_query",
                [path, request.SerializeToString().hex().upper(), "0", False],
            )

            if not result or "response" not in result:
                logger.error(f"Query failed: No response from {path}")
                raise Exception(f"RPC query failed: No response from {path}")

            response = result["response"]
            response_code = response.get("code", -1)
            if response_code != 0:
                if response_code == 5:
                    logger.info(f"Provider {owner} attributes not found")
                    return []
                else:
                    error_log = response.get("log", "Unknown error")
                    logger.error(f"Query failed with code {response_code}: {error_log}")
                    raise Exception(f"Query failed: {error_log}")

            if not response.get("value"):
                logger.info(f"Provider {owner} attributes not found")
                return []

            response_bytes = base64.b64decode(response["value"])
            response = audit_query_pb2.QueryProvidersResponse()
            response.ParseFromString(response_bytes)

            providers = []
            for provider in response.providers:
                provider_info = {
                    "owner": provider.owner,
                    "auditor": provider.auditor,
                    "attributes": [
                        {"key": attr.key, "value": attr.value}
                        for attr in provider.attributes
                    ],
                }
                providers.append(provider_info)

            logger.info(
                f"Found {len(providers)} attribute records for provider {owner}"
            )
            return providers

        except Exception as e:
            logger.error(f"Failed to get provider attributes for {owner}: {e}")
            raise

    def get_provider_auditor_attributes(self, auditor: str, owner: str) -> List[Dict]:
        """
        Get attributes for a specific provider from a specific auditor.

        Args:
            auditor: Auditor address
            owner: Provider owner address

        Returns:
            List[Dict]: List of provider attribute records
        """
        try:
            logger.info(
                f"Querying attributes for provider {owner} by auditor {auditor}"
            )

            request = audit_query_pb2.QueryProviderAuditorRequest()
            request.auditor = auditor
            request.owner = owner
            path = "/akash.audit.v1.Query/ProviderAuditorAttributes"

            result = self.akash_client.rpc_query(
                "abci_query",
                [path, request.SerializeToString().hex().upper(), "0", False],
            )

            if not result or "response" not in result:
                logger.error(f"Query failed: No response from {path}")
                raise Exception(f"RPC query failed: No response from {path}")

            response = result["response"]
            response_code = response.get("code", -1)
            if response_code != 0:
                if response_code == 5:
                    logger.info(
                        f"No attributes found for provider {owner} by auditor {auditor}"
                    )
                    return []
                else:
                    error_log = response.get("log", "Unknown error")
                    logger.error(f"Query failed with code {response_code}: {error_log}")
                    raise Exception(f"Query failed: {error_log}")

            if not response.get("value"):
                logger.info(
                    f"No attributes found for provider {owner} by auditor {auditor}"
                )
                return []

            response_bytes = base64.b64decode(response["value"])
            response = audit_query_pb2.QueryProvidersResponse()
            response.ParseFromString(response_bytes)

            providers = []
            for provider in response.providers:
                provider_info = {
                    "owner": provider.owner,
                    "auditor": provider.auditor,
                    "attributes": [
                        {"key": attr.key, "value": attr.value}
                        for attr in provider.attributes
                    ],
                }
                providers.append(provider_info)

            logger.info(
                f"Found {len(providers)} attribute records for provider {owner} by auditor {auditor}"
            )
            return providers

        except Exception as e:
            logger.error(
                f"Failed to get provider auditor attributes for {auditor}/{owner}: {e}"
            )
            raise

    def get_auditor_attributes(
        self, auditor: str, pagination: Dict = None
    ) -> List[Dict]:
        """
        Get all attributes signed by a specific auditor.

        Args:
            auditor: Auditor address
            pagination: Optional pagination parameters

        Returns:
            List[Dict]: List of provider attribute records signed by auditor
        """
        try:
            logger.info(f"Querying attributes signed by auditor {auditor}")

            request = audit_query_pb2.QueryAuditorAttributesRequest()
            request.auditor = auditor
            if pagination:
                page_request = pagination_pb2.PageRequest()
                if "limit" in pagination:
                    page_request.limit = pagination["limit"]
                if "offset" in pagination:
                    page_request.offset = pagination["offset"]
                if "key" in pagination:
                    page_request.key = pagination["key"]
                request.pagination.CopyFrom(page_request)

            path = "/akash.audit.v1.Query/AuditorAttributes"
            result = self.akash_client.rpc_query(
                "abci_query",
                [path, request.SerializeToString().hex().upper(), "0", False],
            )

            if not result or "response" not in result:
                logger.error(f"Query failed: No response from {path}")
                raise Exception(f"RPC query failed: No response from {path}")

            response = result["response"]
            response_code = response.get("code", -1)
            if response_code != 0:
                if response_code == 5:
                    logger.info(f"No attributes found for auditor {auditor}")
                    return []
                else:
                    error_log = response.get("log", "Unknown error")
                    logger.error(f"Query failed with code {response_code}: {error_log}")
                    raise Exception(f"Query failed: {error_log}")

            if not response.get("value"):
                logger.info(f"No attributes found for auditor {auditor}")
                return []

            response_bytes = base64.b64decode(response["value"])
            response = audit_query_pb2.QueryProvidersResponse()
            response.ParseFromString(response_bytes)

            providers = []
            for provider in response.providers:
                provider_info = {
                    "owner": provider.owner,
                    "auditor": provider.auditor,
                    "attributes": [
                        {"key": attr.key, "value": attr.value}
                        for attr in provider.attributes
                    ],
                }
                providers.append(provider_info)

            logger.info(
                f"Found {len(providers)} attribute records for auditor {auditor}"
            )
            return providers

        except Exception as e:
            logger.error(f"Failed to get auditor attributes for {auditor}: {e}")
            raise
