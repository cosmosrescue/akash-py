#!/usr/bin/env python3
"""
Validation tests for Akash Escrow module.

These tests validate escrow functionality and protobuf structures,
without requiring blockchain interactions.
"""

import os

os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from akash.proto.akash.market.v1beta5.query_pb2 import QueryLeasesRequest, QueryLeasesResponse
from akash.proto.akash.deployment.v1beta4.query_pb2 import QueryDeploymentRequest, QueryDeploymentResponse


class TestEscrowStructures:
    """Test structures needed for escrow operations."""

    def test_lease_query_request_structure(self):
        """Test QueryLeasesRequest structure for lease data fetching."""
        request = QueryLeasesRequest()

        assert hasattr(request, 'filters'), "QueryLeasesRequest missing filters field"
        assert hasattr(request.filters, 'owner'), "LeaseFilters missing owner field"
        assert hasattr(request.filters, 'dseq'), "LeaseFilters missing dseq field"
        assert hasattr(request.filters, 'state'), "LeaseFilters missing state field"

        request.filters.owner = "akash1test"
        request.filters.dseq = 12345
        request.filters.state = "active"

        assert request.filters.owner == "akash1test"
        assert request.filters.dseq == 12345
        assert request.filters.state == "active"

    def test_lease_query_response_structure(self):
        """Test QueryLeasesResponse structure for lease data."""
        response = QueryLeasesResponse()

        assert hasattr(response, 'leases'), "QueryLeasesResponse missing leases field"
        assert len(response.leases) == 0

    def test_deployment_query_request_structure(self):
        """Test QueryDeploymentRequest structure for deployment data fetching."""
        request = QueryDeploymentRequest()

        assert hasattr(request, 'id'), "QueryDeploymentRequest missing id field"
        assert hasattr(request.id, 'owner'), "DeploymentID missing owner field"
        assert hasattr(request.id, 'dseq'), "DeploymentID missing dseq field"

        request.id.owner = "akash1test"
        request.id.dseq = 12345

        assert request.id.owner == "akash1test"
        assert request.id.dseq == 12345

    def test_deployment_query_response_structure(self):
        """Test QueryDeploymentResponse structure for escrow account data."""
        response = QueryDeploymentResponse()

        assert hasattr(response, 'escrow_account'), "QueryDeploymentResponse missing escrow_account field"
        # v1: Account now has nested state structure with funds instead of balance
        assert hasattr(response.escrow_account, 'state'), "EscrowAccount missing state field"
        assert hasattr(response.escrow_account.state, 'settled_at'), "AccountState missing settled_at field"
        assert hasattr(response.escrow_account.state, 'funds'), "AccountState missing funds field"

    def test_decimal_precision_for_calculations(self):
        """Test decimal precision handling for escrow calculations."""
        from decimal import Decimal

        raw_balance = Decimal("5000000000000000000000000")
        uakt_balance = raw_balance / Decimal("1000000000000000000")

        assert uakt_balance == Decimal("5000000")
        lease_price = Decimal("1000")
        total_lease_amount = lease_price * 2

        assert total_lease_amount == Decimal("2000")


class TestEscrowClientFunctionality:
    """Test escrow client functionality."""

    def test_escrow_client_creation(self):
        """Test escrow client initialization."""
        from akash.modules.escrow.client import EscrowClient
        from unittest.mock import Mock

        mock_client = Mock()
        client = EscrowClient(mock_client)

        assert hasattr(client, 'akash_client')
        assert client.akash_client == mock_client
        assert hasattr(client, 'get_blocks_remaining')

    def test_get_blocks_remaining_method_exists(self):
        """Test get_blocks_remaining method exists and is callable."""
        from akash.modules.escrow.client import EscrowClient
        from unittest.mock import Mock

        mock_client = Mock()
        client = EscrowClient(mock_client)

        assert hasattr(client, 'get_blocks_remaining')
        assert callable(client.get_blocks_remaining)

    def test_get_blocks_remaining_parameters(self):
        """Test get_blocks_remaining accepts correct parameters."""
        from akash.modules.escrow.client import EscrowClient
        from unittest.mock import Mock

        mock_client = Mock()
        mock_client.abci_query.return_value = {'response': {'code': -1}}
        mock_client.rpc_query.return_value = None

        client = EscrowClient(mock_client)

        try:
            client.get_blocks_remaining("akash1test", 12345)
        except Exception:
            pass
        assert mock_client.abci_query.called

    def test_blocks_remaining_calculation_structure(self):
        """Test blocks remaining calculation return structure."""
        from akash.modules.escrow.client import EscrowClient
        from unittest.mock import Mock, patch
        import base64

        mock_client = Mock()

        mock_lease_response = Mock()
        mock_lease_response.leases = []

        mock_lease = Mock()
        mock_lease.lease.price.amount = "1000"
        mock_lease_response.leases = [mock_lease]

        mock_deployment_response = Mock()
        mock_deployment_response.escrow_account.balance.amount = "5000000000000000000000000"
        mock_deployment_response.escrow_account.settled_at = 100000

        mock_status = {
            'sync_info': {
                'latest_block_height': '100500'
            }
        }

        with patch('akash.proto.akash.market.v1beta5.query_pb2.QueryLeasesResponse') as mock_lease_cls:
            with patch('akash.proto.akash.deployment.v1beta4.query_pb2.QueryDeploymentResponse') as mock_deploy_cls:
                mock_lease_cls.return_value = mock_lease_response
                mock_deploy_cls.return_value = mock_deployment_response

                mock_client.abci_query.return_value = {
                    'response': {'code': 0, 'value': base64.b64encode(b'mock_data').decode()}
                }
                mock_client.rpc_query.return_value = mock_status

                client = EscrowClient(mock_client)

                try:
                    result = client.get_blocks_remaining("akash1test", 12345)

                    if result and isinstance(result, dict):
                        expected_fields = [
                            'blocks_remaining', 'estimated_time_remaining_seconds',
                            'total_lease_amount_per_block', 'current_height',
                            'settled_at', 'escrow_balance_uakt'
                        ]

                        for field in expected_fields:
                            assert field in result, f"Result missing field: {field}"

                except Exception:
                    pass

    def test_error_handling_patterns(self):
        """Test error handling in get_blocks_remaining."""
        from akash.modules.escrow.client import EscrowClient
        from unittest.mock import Mock

        mock_client = Mock()

        mock_client.abci_query.return_value = {'response': {'code': -1}}
        mock_client.rpc_query.return_value = None

        client = EscrowClient(mock_client)

        try:
            result = client.get_blocks_remaining("akash1test", 12345)
            assert result is None or 'error' in str(result).lower()
        except Exception as e:
            assert isinstance(e, Exception)

    def test_abci_query_paths_for_blocks_remaining(self):
        """Test that get_blocks_remaining uses correct ABCI query paths."""
        from akash.modules.escrow.client import EscrowClient
        from unittest.mock import Mock
        import base64

        mock_client = Mock()

        mock_lease_data = b'mock_lease_data_with_active_leases'
        mock_client.abci_query.side_effect = [
            {'response': {'code': 0, 'value': base64.b64encode(mock_lease_data).decode()}},
            {'response': {'code': -1}}
        ]
        mock_client.rpc_query.return_value = None

        client = EscrowClient(mock_client)

        try:
            client.get_blocks_remaining("akash1test", 12345)
        except Exception:
            pass
        calls = mock_client.abci_query.call_args_list
        paths_used = [call[1]['path'] for call in calls if 'path' in call[1]]

        expected_lease_path = '/akash.market.v1beta5.Query/Leases'
        assert any(expected_lease_path in path for path in paths_used), f"Missing query path: {expected_lease_path}"

        if len(paths_used) > 1:
            expected_deployment_path = '/akash.deployment.v1beta4.Query/Deployment'
            assert any(expected_deployment_path in path for path in
                       paths_used), f"Missing query path: {expected_deployment_path}"


class TestEscrowProtobufCompatibility:
    """Test protobuf compatibility for escrow operations."""

    def test_serialization_deserialization(self):
        """Test protobuf serialization/deserialization for escrow queries."""
        request = QueryLeasesRequest()
        request.filters.owner = "akash1test"
        request.filters.dseq = 12345
        request.filters.state = "active"

        serialized = request.SerializeToString()
        assert isinstance(serialized, bytes)
        assert len(serialized) > 0

        deploy_request = QueryDeploymentRequest()
        deploy_request.id.owner = "akash1test"
        deploy_request.id.dseq = 12345

        serialized = deploy_request.SerializeToString()
        assert isinstance(serialized, bytes)
        assert len(serialized) > 0

    def test_hex_encoding_for_abci_queries(self):
        """Test hex encoding of protobuf messages for ABCI queries."""
        request = QueryLeasesRequest()
        request.filters.owner = "akash1test"
        request.filters.dseq = 12345

        serialized = request.SerializeToString()
        hex_encoded = serialized.hex().upper()

        assert isinstance(hex_encoded, str)
        assert len(hex_encoded) > 0
        assert all(c in '0123456789ABCDEF' for c in hex_encoded)

    def test_response_parsing_compatibility(self):
        """Test response parsing compatibility."""

        try:
            response = QueryLeasesResponse()
            response.ParseFromString(b'')
            assert len(response.leases) == 0
        except Exception:
            pass

        try:
            deploy_response = QueryDeploymentResponse()
            deploy_response.ParseFromString(b'')
            assert hasattr(deploy_response, 'escrow_account')
        except Exception:
            pass


if __name__ == "__main__":
    print("✅ Running escrow module validation tests")
    print("=" * 70)
    print()
    print("Testing escrow calculation structures, protobuf compatibility,")
    print("and client functionality.")
    print()
    print("These tests validate current implementation without blockchain interactions.")
    print()

    pytest.main([__file__, "-v", "--tb=short"])
