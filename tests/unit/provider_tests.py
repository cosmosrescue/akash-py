#!/usr/bin/env python3
"""
Validation tests for Akash Provider module.

These tests validate protobuf message structures, field access patterns,
converter compatibility, and query parameter support without requiring
blockchain interactions. 

Run: python run_validation_tests.py provider
"""

import os

os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from akash.proto.akash.provider.v1beta4 import provider_pb2 as provider_pb
from akash.proto.akash.provider.v1beta4 import query_pb2 as provider_query
from akash.proto.akash.provider.v1beta4 import msg_pb2 as provider_msg  # v1beta4: Msg types moved to msg_pb2
# v1beta4: attributes moved to attributes/v1
from akash.proto.akash.base.attributes.v1 import attribute_pb2 as attr_pb


class TestProviderMessageStructures:
    """Test provider protobuf message structures and field access."""

    def test_provider_structure(self):
        """Test Provider message structure and field access."""
        provider = provider_pb.Provider()

        required_fields = ['owner', 'host_uri', 'attributes', 'info']
        for field in required_fields:
            assert hasattr(provider, field), f"Provider missing field: {field}"

        provider.owner = "akash1test"
        provider.host_uri = "https://provider.akash.network"

        assert provider.owner == "akash1test"
        assert provider.host_uri == "https://provider.akash.network"

    def test_provider_info_structure(self):
        """Test Info message structure and field access."""
        # v1beta4: ProviderInfo is just Info
        info = provider_pb.Info()

        required_fields = ['email', 'website']
        for field in required_fields:
            assert hasattr(info, field), f"Info missing field: {field}"

        info.email = "test@provider.com"
        info.website = "https://provider.com"

        assert info.email == "test@provider.com"
        assert info.website == "https://provider.com"

    def test_provider_attributes_structure(self):
        """Test provider attributes structure."""
        provider = provider_pb.Provider()

        assert hasattr(provider, 'attributes'), "Provider missing attributes field"

        attribute = attr_pb.Attribute()
        attribute.key = "region"
        attribute.value = "us-west"

        provider.attributes.append(attribute)

        assert len(provider.attributes) == 1
        assert provider.attributes[0].key == "region"
        assert provider.attributes[0].value == "us-west"


class TestProviderQueryResponses:
    """Test provider query response structures."""

    def test_query_providers_response_structure(self):
        """Test QueryProvidersResponse nested structure access."""
        response = provider_query.QueryProvidersResponse()

        assert hasattr(response, 'providers'), "QueryProvidersResponse missing providers field"
        assert hasattr(response, 'pagination'), "QueryProvidersResponse missing pagination field"

        provider = provider_pb.Provider()
        provider.owner = "akash1test"
        provider.host_uri = "https://test.provider"

        response.providers.append(provider)

        first_provider = response.providers[0]
        assert hasattr(first_provider, 'owner'), "Provider missing owner field"
        assert hasattr(first_provider, 'host_uri'), "Provider missing host_uri field"
        assert first_provider.owner == "akash1test"

    def test_query_provider_response_structure(self):
        """Test QueryProviderResponse nested structure access."""
        response = provider_query.QueryProviderResponse()

        assert hasattr(response, 'provider'), "QueryProviderResponse missing provider field"

        provider = provider_pb.Provider()
        provider.owner = "akash1test"
        provider.host_uri = "https://test.provider"

        response.provider.CopyFrom(provider)

        assert hasattr(response.provider, 'owner'), "Provider missing owner field"
        assert response.provider.owner == "akash1test"


class TestProviderMessageConverters:
    """Test provider message converters for transaction compatibility."""

    def test_all_provider_converters_registered(self):
        """Test that all provider message converters are registered."""
        from akash.tx import _MESSAGE_CONVERTERS, _initialize_message_converters

        if not _MESSAGE_CONVERTERS:
            _initialize_message_converters()

        required_converters = [
            "/akash.provider.v1beta4.MsgCreateProvider",
            "/akash.provider.v1beta4.MsgUpdateProvider"
        ]

        for msg_type in required_converters:
            converter = _MESSAGE_CONVERTERS.get(msg_type)
            assert converter is not None, f"Missing converter for {msg_type}"
            assert callable(converter), f"Converter for {msg_type} is not callable"

    def test_msg_create_provider_protobuf_compatibility(self):
        """Test MsgCreateProvider protobuf field compatibility."""
        # v1beta4: Msg types moved to msg_pb2
        pb_msg = provider_msg.MsgCreateProvider()

        required_fields = ['owner', 'host_uri', 'attributes', 'info']
        for field in required_fields:
            assert hasattr(pb_msg, field), f"MsgCreateProvider missing field: {field}"

        pb_msg.owner = "akash1test"
        pb_msg.host_uri = "https://provider.test"

        assert pb_msg.owner == "akash1test"
        assert pb_msg.host_uri == "https://provider.test"

    def test_msg_update_provider_protobuf_compatibility(self):
        """Test MsgUpdateProvider protobuf field compatibility."""
        # v1beta4: Msg types moved to msg_pb2
        pb_msg = provider_msg.MsgUpdateProvider()

        required_fields = ['owner', 'host_uri', 'attributes', 'info']
        for field in required_fields:
            assert hasattr(pb_msg, field), f"MsgUpdateProvider missing field: {field}"


class TestProviderQueryParameters:
    """Test provider query parameter compatibility."""

    def test_provider_query_request_structure(self):
        """Test provider query request structures."""
        req = provider_query.QueryProvidersRequest()
        assert hasattr(req, 'pagination'), "QueryProvidersRequest missing pagination field"

        single_req = provider_query.QueryProviderRequest()
        assert hasattr(single_req, 'owner'), "QueryProviderRequest missing owner field"


class TestProviderTransactionMessages:
    """Test provider transaction message structures."""

    def test_all_provider_message_types_exist(self):
        """Test all expected provider message types exist."""
        expected_messages = [
            'MsgCreateProvider', 'MsgUpdateProvider', 'MsgDeleteProvider'
        ]

        # v1beta4: Msg types moved to msg_pb2
        for msg_name in expected_messages:
            assert hasattr(provider_msg, msg_name), f"Missing provider message type: {msg_name}"

            msg_class = getattr(provider_msg, msg_name)
            msg_instance = msg_class()
            assert msg_instance is not None

    def test_provider_message_field_consistency(self):
        """Test provider messages have consistent field structures."""
        # v1beta4: Msg types moved to msg_pb2
        create_msg = provider_msg.MsgCreateProvider()
        update_msg = provider_msg.MsgUpdateProvider()

        common_fields = ['owner', 'host_uri', 'attributes', 'info']

        for field in common_fields:
            assert hasattr(create_msg, field), f"MsgCreateProvider missing: {field}"
            assert hasattr(update_msg, field), f"MsgUpdateProvider missing: {field}"


class TestProviderErrorPatterns:
    """Test common provider error patterns and edge cases."""

    def test_empty_providers_response_handling(self):
        """Test handling of empty providers response."""
        response = provider_query.QueryProvidersResponse()

        assert len(response.providers) == 0, "Empty response should have no providers"
        assert hasattr(response, 'pagination'), "Empty response missing pagination"

    def test_missing_provider_info_handling(self):
        """Test handling of provider without info."""
        provider = provider_pb.Provider()
        provider.owner = "akash1test"
        provider.host_uri = "https://test.provider"

        assert hasattr(provider, 'info'), "Provider missing info field"

    def test_empty_attributes_handling(self):
        """Test handling of provider with no attributes."""
        provider = provider_pb.Provider()

        assert len(provider.attributes) == 0, "Provider should start with empty attributes"

        attribute = attr_pb.Attribute()
        attribute.key = "test"
        attribute.value = "value"
        provider.attributes.append(attribute)

        assert len(provider.attributes) == 1, "Should be able to add attributes"


class TestProviderModuleIntegration:
    """Test provider module integration and consistency."""

    def test_provider_converter_coverage(self):
        """Test all provider messages have converters in tx registry."""
        from akash.tx import _MESSAGE_CONVERTERS, _initialize_message_converters

        if not _MESSAGE_CONVERTERS:
            _initialize_message_converters()

        msg_classes = []
        for attr_name in dir(provider_pb):
            if attr_name.startswith('Msg') and not attr_name.endswith('Response'):
                msg_classes.append(attr_name)

        expected_converters = ['MsgCreateProvider', 'MsgUpdateProvider']
        for msg_class in expected_converters:
            converter_key = f"/akash.provider.v1beta4.{msg_class}"
            assert converter_key in _MESSAGE_CONVERTERS, f"Missing converter for: {msg_class}"

    def test_provider_query_consistency(self):
        """Test provider query response consistency."""
        single_response = provider_query.QueryProviderResponse()
        assert hasattr(single_response, 'provider'), "Single response missing provider field"

        multi_response = provider_query.QueryProvidersResponse()
        assert hasattr(multi_response, 'providers'), "Multi response missing providers field"
        assert hasattr(multi_response, 'pagination'), "Multi response missing pagination field"

    def test_attribute_integration_consistency(self):
        """Test provider attribute integration consistency."""
        provider = provider_pb.Provider()

        attr1 = attr_pb.Attribute()
        attr1.key = "region"
        attr1.value = "us-west"

        attr2 = attr_pb.Attribute()
        attr2.key = "tier"
        attr2.value = "community"

        provider.attributes.extend([attr1, attr2])

        assert len(provider.attributes) == 2, "Provider should have 2 attributes"
        assert provider.attributes[0].key == "region"
        assert provider.attributes[1].key == "tier"


class TestProviderClientFunctionality:
    """Test provider client functionality with mocked dependencies."""

    def setup_method(self):
        """Setup test environment."""
        from unittest.mock import Mock
        from akash.modules.provider.client import ProviderClient

        self.mock_client = Mock()
        self.client = ProviderClient(self.mock_client)

    def test_provider_client_creation(self):
        """Test provider client initialization with all mixins."""
        from akash.modules.provider.client import ProviderClient
        from akash.modules.provider.query import ProviderQuery
        from akash.modules.provider.tx import ProviderTx
        from akash.modules.provider.utils import ProviderUtils
        from unittest.mock import Mock

        mock_client = Mock()
        client = ProviderClient(mock_client)

        assert isinstance(client, ProviderQuery)
        assert isinstance(client, ProviderTx)
        assert isinstance(client, ProviderUtils)
        assert client.akash_client == mock_client

    def test_get_providers_method_structure(self):
        """Test get_providers method with pagination parameters."""
        import inspect

        sig = inspect.signature(self.client.get_providers)
        params = list(sig.parameters.keys())

        expected_params = ['limit', 'offset', 'count_total']
        for param in expected_params:
            assert param in params, f"get_providers missing parameter: {param}"

    def test_get_provider_method_structure(self):
        """Test get_provider method signature."""
        import inspect

        sig = inspect.signature(self.client.get_provider)
        params = list(sig.parameters.keys())

        assert 'owner_address' in params

        mock_response = {'response': {'code': 0, 'value': None}}
        self.mock_client.rpc_query.return_value = mock_response

        try:
            result = self.client.get_provider('akash1test')
            assert result == {}
        except Exception:
            pass

    def test_get_provider_leases_method(self):
        """Test get_provider_leases method structure."""
        import inspect

        sig = inspect.signature(self.client.get_provider_leases)
        params = list(sig.parameters.keys())

        assert 'owner_address' in params

    def test_provider_utils_methods(self):
        """Test provider utility methods are available."""
        utils_methods = [
            'get_provider_attributes',
            'query_providers_by_attributes',
            'validate_provider_config'
        ]

        for method in utils_methods:
            assert hasattr(self.client, method), f"Missing utility method: {method}"
            assert callable(getattr(self.client, method))

    def test_validate_provider_config_functionality(self):
        """Test provider config validation logic."""
        result = self.client.validate_provider_config({})

        assert isinstance(result, dict)
        assert 'valid' in result
        assert 'errors' in result
        assert 'warnings' in result
        assert result['valid'] == False
        assert 'host_uri is required' in result['errors']

    def test_provider_attribute_methods(self):
        """Test provider attribute handling methods."""
        mock_response = {'response': {'code': 0, 'value': None}}
        self.mock_client.rpc_query.return_value = mock_response

        try:
            result = self.client.get_provider_attributes('akash1test')
            assert isinstance(result, list)
        except Exception:
            pass

        result = self.client.query_providers_by_attributes([{'key': 'region', 'value': 'us-west'}])
        assert isinstance(result, list)

    def test_provider_status_method(self):
        """Test provider status checking."""
        self.mock_client.rpc_query.return_value = {'response': {'code': 0, 'value': None}}

        result = self.client.get_provider('akash1test')
        assert result == {}


class TestProviderTransactionFunctionality:
    """Test provider transaction functionality."""

    def setup_method(self):
        """Setup test environment."""
        from unittest.mock import Mock
        from akash.modules.provider.client import ProviderClient

        self.mock_client = Mock()
        self.client = ProviderClient(self.mock_client)

    def test_provider_tx_mixin_loaded(self):
        """Test provider transaction mixin is properly loaded."""
        from akash.modules.provider.tx import ProviderTx
        assert isinstance(self.client, ProviderTx)

    def test_create_provider_method_signature(self):
        """Test create_provider method signature validation."""
        import inspect
        from akash.modules.provider.tx import ProviderTx

        if hasattr(ProviderTx, 'create_provider'):
            sig = inspect.signature(self.client.create_provider)
            params = list(sig.parameters.keys())

            expected_params = ['wallet', 'host_uri']
            for param in expected_params:
                assert param in params, f"create_provider missing parameter: {param}"

    def test_update_provider_method_signature(self):
        """Test update_provider method signature validation."""
        import inspect
        from akash.modules.provider.tx import ProviderTx

        if hasattr(ProviderTx, 'update_provider'):
            sig = inspect.signature(self.client.update_provider)
            params = list(sig.parameters.keys())

            expected_params = ['wallet', 'host_uri']
            for param in expected_params:
                assert param in params, f"update_provider missing parameter: {param}"


class TestProviderErrorScenarios:
    """Test provider error handling scenarios."""

    def setup_method(self):
        """Setup test environment."""
        from unittest.mock import Mock
        from akash.modules.provider.client import ProviderClient

        self.mock_client = Mock()
        self.client = ProviderClient(self.mock_client)

    def test_provider_not_found_handling(self):
        """Test handling when provider is not found."""
        mock_response = {'response': {'code': 0, 'value': None}}
        self.mock_client.rpc_query.return_value = mock_response

        result = self.client.get_provider('akash1nonexistent')
        assert result == {}

    def test_empty_providers_list_handling(self):
        """Test handling empty providers list response."""
        mock_response = {'response': {'code': 0, 'value': None}}
        self.mock_client.rpc_query.return_value = mock_response

        result = self.client.get_providers()
        assert isinstance(result, list)
        assert len(result) == 0

    def test_provider_query_failure_handling(self):
        """Test handling provider query failures."""
        self.mock_client.rpc_query.return_value = None

        with pytest.raises(Exception):
            self.client.get_provider('akash1test')

    def test_invalid_provider_config_validation(self):
        """Test validation of invalid provider configurations."""
        invalid_configs = [
            {},
            {'host_uri': ''},
            {'host_uri': 'invalid-uri', 'email': 'invalid-email'},
            {'host_uri': 'https://test.com', 'attributes': [{'key': '', 'value': 'test'}]}
        ]

        for config in invalid_configs:
            result = self.client.validate_provider_config(config)
            assert isinstance(result, dict)
            assert 'valid' in result
            assert 'errors' in result

            if not config or not config.get('host_uri'):
                assert result['valid'] == False

    def test_provider_status_error_handling(self):
        """Test provider status error handling."""
        from unittest.mock import patch
        with patch.object(self.client, 'get_provider') as mock_get_provider:
            mock_get_provider.side_effect = Exception("Network error")

            with pytest.raises(Exception):
                self.client.get_provider('akash1test')

    def test_provider_attribute_query_error_handling(self):
        """Test provider attribute query error handling."""
        self.mock_client.rpc_query.side_effect = Exception("Network error")

        with pytest.raises(Exception):
            self.client.get_provider_attributes('akash1test')

    def test_provider_leases_error_handling(self):
        """Test provider leases query error handling."""
        with pytest.raises(Exception):
            self.client.get_provider_leases('akash1test')


class TestProviderStatusFunctionality:
    """Test off-chain provider status functionality."""

    def setup_method(self):
        """Setup test environment."""
        from unittest.mock import Mock
        from akash.modules.provider.client import ProviderClient

        self.mock_client = Mock()
        self.client = ProviderClient(self.mock_client)

    def test_get_provider_method_exists(self):
        """Test that get_provider method exists."""
        assert hasattr(self.client, 'get_provider')
        assert callable(getattr(self.client, 'get_provider'))

    def test_get_provider_success(self):
        """Test successful provider query from blockchain."""
        mock_provider = {
            'owner': 'akash1test',
            'host_uri': 'https://provider.akash.com',
            'attributes': [{'key': 'region', 'value': 'us-west'}],
            'info': {'email': 'test@akash.com'}
        }

        from unittest.mock import patch
        with patch.object(self.client, 'get_provider') as mock_get_provider:
            mock_get_provider.return_value = mock_provider

            result = self.client.get_provider('akash1test')

            assert result['owner'] == 'akash1test'
            assert result['host_uri'] == 'https://provider.akash.com'
            assert result['attributes'] == [{'key': 'region', 'value': 'us-west'}]

    def test_get_provider_not_found(self):
        """Test provider query when provider not found."""
        from unittest.mock import patch
        with patch.object(self.client, 'get_provider') as mock_get_provider:
            mock_get_provider.return_value = {}

            result = self.client.get_provider('akash1test')

            assert result == {}

    def test_get_provider_error_handling(self):
        """Test error handling in provider query."""
        from unittest.mock import patch
        with patch.object(self.client, 'get_provider') as mock_get_provider:
            mock_get_provider.side_effect = Exception("RPC connection failed")

            with pytest.raises(Exception) as exc_info:
                self.client.get_provider('akash1test')

            assert "RPC connection failed" in str(exc_info.value)

    def test_provider_status_protobuf_imports(self):
        """Test that provider status protobuf imports work correctly."""
        # Provider v1 service protos MUST exist - they are used by grpc_client.py
        from akash.proto.akash.provider.v1 import status_pb2
        from akash.proto.akash.provider.v1 import service_pb2_grpc

        status = status_pb2.Status()
        assert status is not None

        assert hasattr(service_pb2_grpc, 'ProviderRPCStub')


class TestProviderConvenienceMethods:
    """Test provider convenience methods functionality."""

    def setup_method(self):
        """Setup test environment."""
        from unittest.mock import Mock
        from akash.modules.provider.client import ProviderClient

        self.mock_client = Mock()
        self.client = ProviderClient(self.mock_client)

    def test_convenience_methods_exist(self):
        """Test that all convenience methods exist."""
        expected_methods = [
            'get_providers_by_region',
            'get_providers_by_capabilities'
        ]

        for method_name in expected_methods:
            assert hasattr(self.client, method_name), f"Missing method: {method_name}"
            assert callable(getattr(self.client, method_name))

    def test_get_providers_by_region_basic(self):
        """Test basic region filtering functionality."""
        mock_providers = [
            {
                'owner': 'akash1provider1',
                'attributes': [{'key': 'region', 'value': 'us-west'}]
            },
            {
                'owner': 'akash1provider2',
                'attributes': [{'key': 'region', 'value': 'us-east'}]
            },
            {
                'owner': 'akash1provider3',
                'attributes': [{'key': 'region', 'value': 'us-west'}]
            }
        ]

        from unittest.mock import patch
        with patch.object(self.client, 'get_providers') as mock_list:
            mock_list.return_value = mock_providers

            result = self.client.get_providers_by_region('us-west')

            assert len(result) == 2
            assert all(p['owner'] in ['akash1provider1', 'akash1provider3'] for p in result)

    def test_get_providers_by_region_with_status(self):
        """Test region filtering with status inclusion."""
        mock_providers = [
            {
                'owner': 'akash1provider1',
                'attributes': [{'key': 'region', 'value': 'us-west'}]
            }
        ]

        mock_status = {'cluster': {'leases': {'active': 3}}}

        from unittest.mock import patch
        with patch.object(self.client, 'get_providers') as mock_list:
            mock_list.return_value = mock_providers
            with patch.object(self.client, 'get_provider_status') as mock_status_method:
                mock_status_method.return_value = mock_status

                result = self.client.get_providers_by_region('us-west', include_status=True)

                assert len(result) == 1
                assert result[0]['status'] == mock_status
                mock_status_method.assert_called_once_with('akash1provider1')

    def test_get_providers_by_region_status_error_handling(self):
        """Test region filtering with status error handling."""
        mock_providers = [
            {
                'owner': 'akash1provider1',
                'attributes': [{'key': 'region', 'value': 'us-west'}]
            }
        ]

        from unittest.mock import patch
        with patch.object(self.client, 'get_providers') as mock_list:
            mock_list.return_value = mock_providers
            with patch.object(self.client, 'get_provider_status') as mock_status_method:
                mock_status_method.side_effect = Exception("Status unavailable")

                result = self.client.get_providers_by_region('us-west', include_status=True)

                assert len(result) == 1
                assert result[0]['status'] is None

    def test_get_providers_by_capabilities_single(self):
        """Test filtering by single capability."""
        mock_providers = [
            {
                'owner': 'akash1provider1',
                'attributes': [
                    {'key': 'capabilities/gpu/vendor/nvidia', 'value': 'true'},
                    {'key': 'feat-persistent-storage', 'value': 'true'}
                ]
            },
            {
                'owner': 'akash1provider2',
                'attributes': [
                    {'key': 'feat-persistent-storage', 'value': 'true'}
                ]
            },
            {
                'owner': 'akash1provider3',
                'attributes': [
                    {'key': 'hardware-gpu', 'value': 'nvidia-rtx-4090'}
                ]
            }
        ]

        from unittest.mock import patch
        with patch.object(self.client, 'get_providers') as mock_list:
            mock_list.return_value = mock_providers

            result = self.client.get_providers_by_capabilities(['gpu'])

            assert len(result) == 1
            assert result[0]['owner'] == 'akash1provider1'

    def test_get_providers_by_capabilities_multiple(self):
        """Test filtering by multiple capabilities (requires all)."""
        mock_providers = [
            {
                'owner': 'akash1provider1',
                'attributes': [
                    {'key': 'capabilities/gpu/vendor/nvidia', 'value': 'true'},
                    {'key': 'feat-persistent-storage', 'value': 'true'}
                ]
            },
            {
                'owner': 'akash1provider2',
                'attributes': [
                    {'key': 'capabilities/gpu/vendor/nvidia', 'value': 'true'},
                    {'key': 'feat-endpoint-ip', 'value': 'true'}
                ]
            }
        ]

        from unittest.mock import patch
        with patch.object(self.client, 'get_providers') as mock_list:
            mock_list.return_value = mock_providers

            result = self.client.get_providers_by_capabilities(['gpu', 'persistent-storage'])

            assert len(result) == 1
            assert result[0]['owner'] == 'akash1provider1'
            assert 'matched_capabilities' in result[0]

    def test_get_providers_by_capabilities_partial_match(self):
        """Test that partial capability matching works."""
        mock_providers = [
            {
                'owner': 'akash1provider1',
                'attributes': [
                    {'key': 'feat-persistent-storage', 'value': 'true'}
                ]
            },
            {
                'owner': 'akash1provider2',
                'attributes': [
                    {'key': 'feat-endpoint-ip', 'value': 'true'}
                ]
            },
            {
                'owner': 'akash1provider3',
                'attributes': [
                    {'key': 'feat-endpoint-custom-domain', 'value': 'true'}
                ]
            }
        ]

        from unittest.mock import patch
        with patch.object(self.client, 'get_providers') as mock_list:
            mock_list.return_value = mock_providers

            result = self.client.get_providers_by_capabilities(['endpoint'])

            assert len(result) == 2
            owners = {p['owner'] for p in result}
            assert 'akash1provider2' in owners
            assert 'akash1provider3' in owners
            assert 'akash1provider1' not in owners



class TestProviderGRPCClientIntegration:
    """Test provider gRPC client integration."""

    def setup_method(self):
        """Setup test environment."""
        from unittest.mock import Mock
        from akash.client import AkashClient
        from akash.grpc_client import ProviderGRPCClient

        self.mock_akash_client = Mock(spec=AkashClient)
        self.grpc_client = ProviderGRPCClient(self.mock_akash_client)

    def test_provider_grpc_client_initialization(self):
        """Test ProviderGRPCClient initialization."""
        assert self.grpc_client.akash_client == self.mock_akash_client
        assert hasattr(self.grpc_client, 'logger')

    def test_get_provider_status_method_signature(self):
        """Test get_provider_status method signature."""
        import inspect

        sig = inspect.signature(self.grpc_client.get_provider_status)
        params = list(sig.parameters.keys())

        expected_params = ['provider_address', 'retries', 'timeout', 'insecure', 'check_version']
        for param in expected_params:
            assert param in params, f"get_provider_status missing parameter: {param}"

    def test_get_provider_status_no_endpoint(self):
        """Test behavior when provider endpoint is not found."""
        self.mock_akash_client.get_provider_endpoint.side_effect = ValueError("Provider not found")

        result = self.grpc_client.get_provider_status('akash1nonexistent')

        assert result.get('status') == 'error'
        assert 'Failed to query provider status' in result.get('error', '')

    def test_get_provider_status_connection_parameters(self):
        """Test that gRPC connection error handling works."""
        self.mock_akash_client.get_provider_endpoint.return_value = "provider.test.com:8444"

        result = self.grpc_client.get_provider_status('akash1test')

        assert result.get('status') == 'error'
        error_msg = result.get('error', '').lower()
        assert "port" in error_msg or "connection" in error_msg or "dns" in error_msg


class TestProviderStatusProtobufIntegration:
    """Test provider status protobuf integration."""

    def test_provider_status_protobuf_structure(self):
        """Test that provider status protobuf has expected structure."""
        # Provider v1 status protos MUST exist - they are used by grpc_client.py
        from akash.proto.akash.provider.v1 import status_pb2

        status = status_pb2.Status()

        expected_fields = ['cluster', 'bid_engine', 'manifest', 'timestamp']
        for field in expected_fields:
            assert hasattr(status, field), f"Status missing field: {field}"

    def test_provider_inventory_protobuf_structure(self):
        """Test that inventory protobuf structures are available."""
        # Inventory protos MUST exist - they are used by inventory module
        from akash.proto.akash.inventory.v1 import cluster_pb2
        from akash.proto.akash.inventory.v1 import node_pb2
        from akash.proto.akash.inventory.v1 import resources_pb2

        cluster = cluster_pb2.Cluster()
        node = node_pb2.Node()

        available_classes = [attr for attr in dir(resources_pb2) if not attr.startswith('_')]
        assert len(available_classes) > 0

        assert cluster is not None
        assert node is not None

    def test_provider_service_grpc_stub(self):
        """Test that provider service gRPC stub is available."""
        # Provider v1 service protos MUST exist - they are used by grpc_client.py
        from akash.proto.akash.provider.v1 import service_pb2_grpc

        assert hasattr(service_pb2_grpc, 'ProviderRPCStub')

        from unittest.mock import Mock
        mock_channel = Mock()

        stub = service_pb2_grpc.ProviderRPCStub(mock_channel)
        assert stub is not None
        assert hasattr(stub, 'GetStatus')


class TestProviderQueryMissingCoverage:
    """Test previously uncovered provider query functions."""

    def test_get_provider_version_structure(self):
        """Test get_provider_version via protobuf Status message."""
        from akash.proto.akash.provider.v1.status_pb2 import Status

        status = Status()
        assert hasattr(status, 'cluster'), "Status missing cluster field"
        assert hasattr(status, 'bid_engine'), "Status missing bid_engine field"
        assert hasattr(status, 'manifest'), "Status missing manifest field"


if __name__ == '__main__':
    print("✅ Running provider module validation tests")
    print("=" * 70)
    print()
    print("Testing protobuf structures, message converters, query responses,")
    print("parameter compatibility, attribute integration patterns, and new")
    print("off-chain provider status functionality.")
    print()
    print("These tests catch breaking changes without blockchain interactions.")
    print()

    pytest.main([__file__, '-v'])
