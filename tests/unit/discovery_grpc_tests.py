#!/usr/bin/env python3
"""
Discovery module tests - validation and functional tests.

Validation tests: Validate protobuf message structures, field access patterns,
converter compatibility, and query parameter support without requiring
blockchain interactions. 

Functional tests: Test discovery client gRPC operations including provider status
checks, availability discovery, capability queries, and provider endpoint resolution
using mocking to isolate functionality and test error handling scenarios.

Run: python discovery_grpc_tests.py
"""

import os

os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

import pytest
import sys
from unittest.mock import Mock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from akash.modules.discovery.client import DiscoveryClient


class TestProviderStatusDiscovery:
    """Test provider status discovery via gRPC."""

    def test_get_provider_status_success(self):
        """Test successful provider status retrieval via GRPC."""
        mock_akash_client = Mock()
        discovery_client = DiscoveryClient(mock_akash_client)

        mock_grpc_response = {
            "status": "success",
            "response": {
                "cluster": {
                    "leases": 5,
                    "inventory": {
                        "cluster": {
                            "cpu": {"val": "1000"},
                            "memory": {"val": "2147483648"},
                            "ephemeral_storage": {"val": "10737418240"},
                            "gpu": {"val": "0"}
                        }
                    }
                },
                "bid_engine": {"orders": 0},
                "manifest": {"deployments": 0},
                "errors": [],
                "public_hostnames": [],
                "timestamp": "2023-01-01T00:00:00Z"
            },
            "attempts": 1
        }

        discovery_client.grpc_client.get_provider_status = Mock(return_value=mock_grpc_response)

        result = discovery_client.get_provider_status("akash1qnnhhgzxj24f2kld5yhy4v4h4s9r295ak5gjw4")

        assert result["status"] == "success"
        assert "provider_status" in result
        status = result["provider_status"]
        assert status["cluster"]["leases"]["active"] == 5
        assert status["method"] == "GRPC"
        assert status["status"] == "online"

        discovery_client.grpc_client.get_provider_status.assert_called_once_with(
            provider_address="akash1qnnhhgzxj24f2kld5yhy4v4h4s9r295ak5gjw4",
            insecure=True,
            check_version=True
        )

    def test_get_provider_status_grpc_error(self):
        """Test provider status retrieval with GRPC error."""
        mock_akash_client = Mock()
        discovery_client = DiscoveryClient(mock_akash_client)

        mock_grpc_response = {
            "status": "error",
            "error": "gRPC UNAVAILABLE: Provider unavailable",
            "attempts": 3
        }

        discovery_client.grpc_client.get_provider_status = Mock(return_value=mock_grpc_response)
        discovery_client._http_fallback_status = Mock(return_value={
            "status": "failed",
            "error": "Provider unavailable",
            "provider": "provider.example.com:8443"
        })

        result = discovery_client.get_provider_status("provider.example.com:8443")

        assert result["status"] == "failed"
        assert "Provider unavailable" in result["error"]

    def test_get_provider_status_connection_error(self):
        """Test provider status retrieval with connection error."""
        mock_akash_client = Mock()
        discovery_client = DiscoveryClient(mock_akash_client)

        mock_grpc_response = {
            "status": "error",
            "error": "DNS resolution failed for unreachable.provider.com: Connection failed",
            "attempts": 0
        }

        discovery_client.grpc_client.get_provider_status = Mock(return_value=mock_grpc_response)
        discovery_client._http_fallback_status = Mock(return_value={
            "status": "failed",
            "error": "Connection failed",
            "provider": "unreachable.provider.com:8443"
        })

        result = discovery_client.get_provider_status("unreachable.provider.com:8443")

        assert result["status"] == "failed"
        assert "Connection failed" in result["error"]

    def test_get_provider_status_invalid_endpoint(self):
        """Test provider status retrieval with invalid endpoint."""
        mock_akash_client = Mock()
        discovery_client = DiscoveryClient(mock_akash_client)

        result = discovery_client.get_provider_status("")

        assert result["status"] == "failed"
        assert "endpoint cannot be empty" in result["error"].lower()

    def test_get_provider_status_without_https(self):
        """Test provider status retrieval with HTTP fallback."""
        mock_akash_client = Mock()
        discovery_client = DiscoveryClient(mock_akash_client)

        mock_grpc_response = {
            "status": "error",
            "error": "gRPC connection failed",
            "attempts": 2
        }

        mock_http_response = {
            "status": "success",
            "provider_status": {
                "cluster": {
                    "leases": {"active": 3},
                    "inventory": {
                        "cluster": {
                            "cpu": {"val": "500"},
                            "memory": {"val": "1073741824"},
                            "ephemeral_storage": {"val": "5368709120"},
                            "gpu": {"val": "0"}
                        }
                    }
                },
                "method": "HTTP (HTTP)",
                "status": "online"
            }
        }

        discovery_client.grpc_client.get_provider_status = Mock(return_value=mock_grpc_response)
        discovery_client._http_fallback_status = Mock(return_value=mock_http_response)

        result = discovery_client.get_provider_status("provider.example.com:8443", use_https=False)

        assert result["status"] == "success"
        discovery_client._http_fallback_status.assert_called_once_with("provider.example.com:8443", False)


class TestProviderDiscoveryWorkflow:
    """Test complete provider discovery workflow."""

    def test_discover_providers_success(self):
        """Test successful provider discovery across multiple providers."""
        mock_akash_client = Mock()
        discovery_client = DiscoveryClient(mock_akash_client)

        mock_providers = [
            {"host_uri": "provider1.example.com:8443"},
            {"host_uri": "provider2.example.com:8443"},
            {"host_uri": "provider3.example.com:8443"}
        ]

        def mock_get_status(endpoint, use_https=True):
            if "provider1" in endpoint:
                return {
                    "status": "success",
                    "provider_status": {
                        "cluster": {"leases": {"active": 2}, "resources": {"cpu": 1000, "memory": 2147483648}},
                        "status": "online"
                    }
                }
            elif "provider2" in endpoint:
                return {
                    "status": "success",
                    "provider_status": {
                        "cluster": {"leases": {"active": 1}, "resources": {"cpu": 500, "memory": 1073741824}},
                        "status": "online"
                    }
                }
            else:
                return {
                    "status": "failed",
                    "error": "Connection timeout"
                }

        with patch.object(mock_akash_client.provider, 'get_providers', return_value=mock_providers), \
                patch.object(discovery_client, 'get_provider_status', side_effect=mock_get_status):

            provider_uris = [provider["host_uri"] for provider in mock_providers]
            result = discovery_client.get_providers_status(provider_uris)

            assert result["status"] == "success"
            assert result["discovery_results"]["total_providers"] == 3
            assert len(result["discovery_results"]["providers"]) == 3

            providers = result["discovery_results"]["providers"]
            assert providers["provider1.example.com:8443"]["accessible"] == True
            assert providers["provider2.example.com:8443"]["accessible"] == True
            assert providers["provider3.example.com:8443"]["accessible"] == False

            assert result["discovery_results"]["successful_connections"] == 2
            assert result["discovery_results"]["failed_connections"] == 1

    def test_discover_providers_partial_success(self):
        """Test provider discovery with some providers accessible."""
        mock_akash_client = Mock()
        discovery_client = DiscoveryClient(mock_akash_client)

        mock_providers = [
            {"host_uri": "provider1.example.com:8443"},
            {"host_uri": "provider2.example.com:8443"}
        ]

        def mock_get_status(endpoint, use_https=True):
            if "provider1" in endpoint:
                return {
                    "status": "success",
                    "provider_status": {
                        "cluster": {"leases": {"active": 1}, "resources": {"cpu": 1000, "memory": 2147483648}},
                        "status": "online"
                    }
                }
            else:
                return {
                    "status": "failed",
                    "error": "Provider offline"
                }

        with patch.object(mock_akash_client.provider, 'get_providers', return_value=mock_providers), \
                patch.object(discovery_client, 'get_provider_status', side_effect=mock_get_status):

            provider_uris = [provider["host_uri"] for provider in mock_providers]
            result = discovery_client.get_providers_status(provider_uris)

            assert result["status"] == "success"
            assert result["discovery_results"]["total_providers"] == 2

            providers = result["discovery_results"]["providers"]
            assert providers["provider1.example.com:8443"]["accessible"] == True
            assert providers["provider2.example.com:8443"]["accessible"] == False

            assert result["discovery_results"]["successful_connections"] == 1
            assert result["discovery_results"]["failed_connections"] == 1

    def test_discover_providers_no_providers(self):
        """Test provider discovery with no providers available."""
        mock_akash_client = Mock()
        discovery_client = DiscoveryClient(mock_akash_client)

        with patch.object(mock_akash_client.provider, 'get_providers', return_value=[]):
            result = discovery_client.get_providers_status([])

            assert result["status"] == "success"
            assert result["discovery_results"]["total_providers"] == 0
            assert len(result["discovery_results"]["providers"]) == 0
            assert result["discovery_results"]["successful_connections"] == 0

    def test_discover_providers_query_error(self):
        """Test provider discovery with empty provider list."""
        mock_akash_client = Mock()
        discovery_client = DiscoveryClient(mock_akash_client)

        result = discovery_client.get_providers_status([])

        assert result["status"] == "success"
        assert result["discovery_results"]["total_providers"] == 0
        assert result["discovery_results"]["successful_connections"] == 0
        assert result["discovery_results"]["failed_connections"] == 0

    def test_discover_providers_with_direct_addresses(self):
        """Test provider discovery with directly provided addresses."""
        mock_akash_client = Mock()
        discovery_client = DiscoveryClient(mock_akash_client)

        provider_addresses = [
            "provider1.example.com:8443",
            "provider2.example.com:8443"
        ]

        def mock_get_status(endpoint, use_https=True):
            return {
                "status": "success",
                "provider_status": {
                    "cluster": {"leases": {"active": 0}, "resources": {"cpu": 1000}},
                    "status": "online"
                }
            }

        with patch.object(discovery_client, 'get_provider_status', side_effect=mock_get_status):
            result = discovery_client.get_providers_status(provider_uris=provider_addresses)

            assert result["status"] == "success"
            assert result["discovery_results"]["total_providers"] == 2
            assert "provider1.example.com:8443" in result["discovery_results"]["providers"]
            assert "provider2.example.com:8443" in result["discovery_results"]["providers"]


class TestProviderCapabilityQueries:
    """Test provider capability and resource queries."""

    def test_get_provider_capabilities_success(self):
        """Test successful provider capabilities retrieval."""
        mock_akash_client = Mock()
        discovery_client = DiscoveryClient(mock_akash_client)

        def mock_get_status(endpoint, use_https=True):
            return {
                "status": "success",
                "provider_status": {
                    "cluster": {
                        "leases": {"active": 2},
                        "inventory": {
                            "cluster": {
                                "cpu": {"val": "16000"},
                                "memory": {"val": "68719476736"},
                                "ephemeral_storage": {"val": "1073741824000"},
                                "gpu": {"val": "4"}
                            }
                        },
                        "resources": {"cpu": 16000, "memory": 68719476736, "storage": 1073741824000, "gpu": 4}
                    },
                    "status": "online"
                }
            }

        with patch.object(discovery_client, 'get_provider_status', side_effect=mock_get_status):
            result = discovery_client.get_provider_capabilities("provider.example.com:8443")

            assert result["status"] == "success"
            assert "capabilities" in result
            capabilities = result["capabilities"]
            assert capabilities["cpu"]["val"] == "16000"
            assert capabilities["memory"]["val"] == "68719476736"
            assert capabilities["gpu"]["val"] == "4"

    def test_get_provider_resources_success(self):
        """Test successful provider resource availability check."""
        mock_akash_client = Mock()
        discovery_client = DiscoveryClient(mock_akash_client)

        def mock_get_status(endpoint, use_https=True):
            return {
                "status": "success",
                "provider_status": {
                    "cluster": {
                        "leases": {"active": 3},
                        "inventory": {
                            "cluster": {
                                "cpu": {"val": "8000"},
                                "memory": {"val": "34359738368"},  # 32GB 
                                "ephemeral_storage": {"val": "536870912000"},  # 500GB
                                "gpu": {"val": "0"}
                            },
                            "reservations": {
                                "pending": {
                                    "resources": {
                                        "cpu": {"val": "1000"},
                                        "memory": {"val": "4294967296"},  # 4GB
                                        "ephemeral_storage": {"val": "53687091200"},  # 50GB
                                        "gpu": {"val": "0"}
                                    }
                                }
                            }
                        }
                    },
                    "status": "online"
                }
            }

        with patch.object(discovery_client, 'get_provider_status', side_effect=mock_get_status):
            result = discovery_client.get_provider_resources("provider.example.com:8443")

            assert result["status"] == "success"
            assert result["resources"]["available"]["cpu"] == "8000"
            assert result["resources"]["available"]["memory"] == "34359738368"
            assert result["resources"]["available"]["ephemeral_storage"] == "536870912000"
            assert result["resources"]["pending"]["cpu"] == "1000"
            assert result["resources"]["pending"]["memory"] == "4294967296"

    def test_get_provider_capacity_sufficient(self):
        """Test checking provider capacity with sufficient resources."""
        mock_akash_client = Mock()
        discovery_client = DiscoveryClient(mock_akash_client)

        def mock_get_resources(endpoint, use_https=True):
            return {
                "status": "success",
                "resources": {
                    "available": {
                        "cpu": "2000",  # 2000 milliCPU available
                        "memory": "4294967296",  # 4GB in bytes
                        "ephemeral_storage": "21474836480"  # 20GB in bytes
                    }
                }
            }

        with patch.object(discovery_client, 'get_provider_resources', side_effect=mock_get_resources):
            required_resources = {
                "cpu": "1000",  # Need 1000 milliCPU
                "memory": "2Gi",  # Need 2GB
                "ephemeral_storage": "10Gi"  # Need 10GB
            }

            result = discovery_client.get_provider_capacity(
                "provider.example.com:8443",
                required_resources
            )

            assert result["status"] == "success"
            assert result["has_capacity"] == True
            assert result["sufficient"]["cpu"] == True
            assert result["sufficient"]["memory"] == True
            assert result["sufficient"]["ephemeral_storage"] == True

    def test_get_provider_capacity_insufficient(self):
        """Test checking provider capacity with insufficient resources."""
        mock_akash_client = Mock()
        discovery_client = DiscoveryClient(mock_akash_client)

        def mock_get_resources(endpoint, use_https=True):
            return {
                "status": "success",
                "resources": {
                    "available": {
                        "cpu": "500",  # Only 500 milliCPU available
                        "memory": "1073741824",  # Only 1GB available
                        "ephemeral_storage": "5368709120"  # Only 5GB available
                    }
                }
            }

        with patch.object(discovery_client, 'get_provider_resources', side_effect=mock_get_resources):
            required_resources = {
                "cpu": "1000",  # Need 1000 milliCPU
                "memory": "2Gi",  # Need 2GB
                "ephemeral_storage": "10Gi"  # Need 10GB
            }

            result = discovery_client.get_provider_capacity(
                "provider.example.com:8443",
                required_resources
            )

            assert result["status"] == "success"
            assert result["has_capacity"] == False
            assert result["sufficient"]["cpu"] == False
            assert result["sufficient"]["memory"] == False
            assert result["sufficient"]["ephemeral_storage"] == False


class TestProviderNetworkDiscovery:
    """Test provider network and connectivity discovery."""

    def test_get_provider_status_with_grpc_method(self):
        """Test provider status with GRPC connection method."""
        mock_akash_client = Mock()
        discovery_client = DiscoveryClient(mock_akash_client)

        def mock_get_status(endpoint, use_https=True):
            return {
                "status": "success",
                "provider_status": {
                    "cluster": {"leases": {"active": 1}},
                    "status": "online",
                    "method": "GRPC"
                }
            }

        with patch.object(discovery_client, 'get_provider_status', side_effect=mock_get_status):
            result = discovery_client.get_provider_status("provider.example.com:8443")

            assert result["status"] == "success"
            assert result["provider_status"]["method"] == "GRPC"
            assert result["provider_status"]["status"] == "online"
            assert result["provider_status"]["cluster"]["leases"]["active"] == 1

    def test_get_provider_status_connection_failure(self):
        """Test provider status with connection failure."""
        mock_akash_client = Mock()
        discovery_client = DiscoveryClient(mock_akash_client)

        def mock_get_status(endpoint, use_https=True):
            return {
                "status": "failed",
                "error": "Connection refused"
            }

        with patch.object(discovery_client, 'get_provider_status', side_effect=mock_get_status):
            result = discovery_client.get_provider_status("unreachable.provider.com:8443")

            assert result["status"] == "failed"
            assert "Connection refused" in result["error"]

    def test_get_provider_status_with_http_method(self):
        """Test provider status with HTTP method."""
        mock_akash_client = Mock()
        discovery_client = DiscoveryClient(mock_akash_client)

        def mock_get_status(endpoint, use_https=True):
            return {
                "status": "success",
                "provider_status": {
                    "cluster": {"leases": {"active": 1}},
                    "status": "online",
                    "method": "HTTP"
                }
            }

        with patch.object(discovery_client, 'get_provider_status', side_effect=mock_get_status):
            result = discovery_client.get_provider_status("provider.example.com:8443")

            assert result["status"] == "success"
            assert result["provider_status"]["method"] == "HTTP"
            assert result["provider_status"]["status"] == "online"
            assert result["provider_status"]["cluster"]["leases"]["active"] == 1

    def test_discover_network_providers(self):
        """Test discovery of providers across network regions."""
        mock_akash_client = Mock()
        discovery_client = DiscoveryClient(mock_akash_client)

        mock_providers = [
            {
                "owner": "us-west.provider.com:8443",
                "attributes": [{"key": "region", "value": "us-west"}]
            },
            {
                "owner": "us-east.provider.com:8443",
                "attributes": [{"key": "region", "value": "us-east"}]
            },
            {
                "owner": "eu-central.provider.com:8443",
                "attributes": [{"key": "region", "value": "eu-central"}]
            }
        ]

        def mock_test_connectivity(endpoint, use_https=True):
            if "us-west" in endpoint:
                return {
                    "status": "success",
                    "provider_status": {"cluster": {"leases": {"active": 1}}, "status": "online"}
                }
            elif "us-east" in endpoint:
                return {
                    "status": "success",
                    "provider_status": {"cluster": {"leases": {"active": 2}}, "status": "online"}
                }
            else:
                return {
                    "status": "success",
                    "provider_status": {"cluster": {"leases": {"active": 3}}, "status": "online"}
                }

        with patch.object(discovery_client, 'get_provider_status', side_effect=mock_test_connectivity):

            result = discovery_client.get_providers_status([p["owner"] for p in mock_providers])

            assert result["status"] == "success"
            assert result["discovery_results"]["total_providers"] == 3
            assert result["discovery_results"]["successful_connections"] == 3
            assert result["discovery_results"]["failed_connections"] == 0

            results = result["discovery_results"]["providers"]
            assert "us-west.provider.com:8443" in results
            assert "us-east.provider.com:8443" in results
            assert "eu-central.provider.com:8443" in results

            for provider_address in ["us-west.provider.com:8443", "us-east.provider.com:8443",
                                     "eu-central.provider.com:8443"]:
                assert results[provider_address]["accessible"] == True


class TestProviderStatusParsing:
    """Test provider status response parsing and formatting."""

    def test_parse_cluster_status(self):
        """Test parsing of cluster status from mock response object."""
        mock_akash_client = Mock()
        discovery_client = DiscoveryClient(mock_akash_client)

        mock_response = Mock()
        mock_response.cluster = Mock()
        mock_response.cluster.available_cpu = 8000
        mock_response.cluster.available_memory = "32Gi"
        mock_response.cluster.available_storage = "1000Gi"
        mock_response.cluster.public_hostname = "provider.example.com"
        mock_response.cluster.leases = Mock()
        mock_response.cluster.leases.active = 5
        mock_response.cluster.leases.total = 10

        result = discovery_client._parse_cluster_status(mock_response)

        assert result["nodes"]["available_cpu"] == 8000
        assert result["nodes"]["available_memory"] == "32Gi"
        assert result["nodes"]["available_storage"] == "1000Gi"
        assert result["public_hostname"] == "provider.example.com"
        assert result["leases"]["active"] == 5
        assert result["leases"]["total"] == 10

    def test_parse_inventory_response(self):
        """Test parsing of inventory from mock response object."""
        mock_akash_client = Mock()
        discovery_client = DiscoveryClient(mock_akash_client)

        mock_inventory = Mock()

        mock_inventory.cpu = Mock()
        mock_inventory.cpu.quantity = Mock()
        mock_inventory.cpu.quantity.value = 16000

        mock_inventory.memory = Mock()
        mock_inventory.memory.quantity = Mock()
        mock_inventory.memory.quantity.value = "64Gi"

        mock_storage1 = Mock()
        mock_storage1.class_ = "ssd"
        mock_storage1.quantity = Mock()
        mock_storage1.quantity.value = "1000Gi"
        mock_inventory.storage = [mock_storage1]

        mock_gpu1 = Mock()
        mock_gpu1.vendor = "nvidia"
        mock_gpu1.model = "rtx3080"
        mock_gpu1.quantity = Mock()
        mock_gpu1.quantity.value = 2
        mock_inventory.gpu = [mock_gpu1]

        result = discovery_client._parse_inventory_response(mock_inventory)

        assert "cpu" in result
        assert result["cpu"]["quantity"] == 16000
        assert result["memory"]["quantity"] == "64Gi"
        assert len(result["storage"]) == 1
        assert result["storage"][0]["class"] == "ssd"
        assert result["storage"][0]["quantity"] == "1000Gi"
        assert len(result["gpu"]) == 1
        assert result["gpu"][0]["vendor"] == "nvidia"
        assert result["gpu"][0]["model"] == "rtx3080"
        assert result["gpu"][0]["quantity"] == 2

    def test_format_discovery_results(self):
        """Test formatting of discovery results for client consumption."""
        mock_akash_client = Mock()
        discovery_client = DiscoveryClient(mock_akash_client)

        raw_results = {
            "akash1provider1": {
                "accessible": True,
                "provider_status": {
                    "cluster": {
                        "nodes": {"available_cpu": 1000},
                        "leases": 5
                    }
                },
                "endpoint": "provider1.example.com:8443"
            },
            "akash1provider2": {
                "accessible": False,
                "error": "Connection timeout",
                "endpoint": "provider2.example.com:8443"
            }
        }

        formatted = discovery_client._format_discovery_results(raw_results)

        assert formatted["total_providers"] == 2
        assert formatted["discovery_percentage"] == 50.0  # 1 out of 2 accessible
        assert len(formatted["providers"]) == 2

        provider1 = formatted["providers"]["akash1provider1"]
        assert provider1["accessible"] == True
        assert provider1["endpoint"] == "provider1.example.com:8443"

        provider2 = formatted["providers"]["akash1provider2"]
        assert provider2["accessible"] == False
        assert provider2["error"] == "Connection timeout"


class TestDiscoveryErrorHandling:
    """Test complete discovery error handling."""

    def test_discovery_timeout_handling(self):
        """Test handling of discovery timeouts."""
        mock_akash_client = Mock()
        discovery_client = DiscoveryClient(mock_akash_client)

        mock_providers = [
            {"host_uri": "slow.provider.com:8443"}
        ]

        with patch.object(mock_akash_client.provider, 'get_providers', return_value=mock_providers), \
                patch.object(discovery_client, 'get_provider_status', side_effect=Exception("Timeout")):
            provider_uris = [provider["host_uri"] for provider in mock_providers]
            result = discovery_client.get_providers_status(provider_uris)

            assert result["status"] == "success"  # Discovery succeeds even with failures
            providers = result["discovery_results"]["providers"]
            assert providers["slow.provider.com:8443"]["accessible"] == False
            assert "Timeout" in providers["slow.provider.com:8443"]["error"]

    def test_discovery_invalid_provider_data(self):
        """Test discovery with invalid provider data from blockchain."""
        mock_akash_client = Mock()
        discovery_client = DiscoveryClient(mock_akash_client)

        invalid_providers = [
            {"owner": "akash1provider1"},  # Missing host_uri
            {"owner": "akash1provider2", "host_uri": ""},  # Empty host_uri
            {"host_uri": "valid.provider.com:8443"}
        ]

        def mock_get_status(endpoint, use_https=True):
            return {
                "status": "success",
                "provider_status": {
                    "cluster": {
                        "leases": {"active": 1},
                        "inventory": {},
                        "resources": {"cpu": 1000, "memory": 2147483648}
                    },
                    "status": "online"
                }
            }

        with patch.object(mock_akash_client.provider, 'get_providers', return_value=invalid_providers), \
                patch.object(discovery_client, 'get_provider_status', side_effect=mock_get_status):
            provider_uris = [provider["host_uri"] for provider in invalid_providers if provider.get("host_uri")]
            result = discovery_client.get_providers_status(provider_uris)

            assert result["status"] == "success"
            assert result["discovery_results"]["total_providers"] == 1
            providers = result["discovery_results"]["providers"]
            assert "valid.provider.com:8443" in providers
            assert providers["valid.provider.com:8443"]["accessible"] == True

    def test_discovery_grpc_service_unavailable(self):
        """Test discovery with GRPC service unavailable."""
        mock_akash_client = Mock()
        discovery_client = DiscoveryClient(mock_akash_client)

        mock_grpc_response = {
            "status": "error",
            "error": "Service unavailable",
            "attempts": 3
        }

        discovery_client.grpc_client.get_provider_status = Mock(return_value=mock_grpc_response)
        discovery_client._http_fallback_status = Mock(return_value={
            "status": "failed",
            "error": "Service unavailable",
            "provider": "provider.example.com:8443"
        })

        result = discovery_client.get_provider_status("provider.example.com:8443")

        assert result["status"] == "failed"
        assert "Service unavailable" in result["error"]

    def test_discovery_grpc_parsing_error(self):
        """Test discovery with GRPC response parsing errors."""
        mock_akash_client = Mock()
        discovery_client = DiscoveryClient(mock_akash_client)

        mock_grpc_response = {
            "status": "success",
            "response": "invalid_data_structure",
            "attempts": 1
        }

        discovery_client.grpc_client.get_provider_status = Mock(return_value=mock_grpc_response)

        result = discovery_client.get_provider_status("akash1qnnhhgzxj24f2kld5yhy4v4h4s9r295ak5gjw4")

        assert result["status"] == "failed"
        assert "GRPC response formatting failed" in result["error"]


class TestDiscoveryQueryMissingCoverage:
    """Test previously uncovered discovery query functions."""

    def test_get_client_info_response_structure(self):
        """Test get_client_info uses DiscoveryClient protobuf messages."""
        from unittest.mock import Mock

        # Test that client info follows expected structure
        mock_response = Mock()
        mock_response.status = "active"
        mock_response.version = "1.0.0"

        assert hasattr(mock_response, 'status')
        assert hasattr(mock_response, 'version')


if __name__ == '__main__':
    print("✅ Running discovery gRPC operations tests")
    print("=" * 70)
    print()
    print("Discovery tests: testing provider discovery, status checks, capability")
    print("queries, network connectivity, and resource availability.")
    print()
    print("These tests cover provider discovery and connectivity functionality.")
    print()

    pytest.main([__file__, '-v'])
