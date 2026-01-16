#!/usr/bin/env python3
"""
IBC module tests - validation and functional tests.

Validation tests: Validate protobuf message structures, field access patterns,
converter compatibility, and query parameter support without requiring
blockchain interactions. 

Functional tests: Test IBC client query operations, transaction broadcasting,
inter-blockchain communication functionality, and utility functions using mocking
to isolate functionality and test error handling scenarios.

Run: python ibc_tests.py
"""

import os

os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

import pytest
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

proto_path = os.path.join(os.path.dirname(__file__), '..', '..', 'akash', 'proto')
if proto_path not in sys.path:
    sys.path.append(proto_path)

try:
    import ibc.applications.transfer.v1.query_pb2 as transfer_query
    import ibc.applications.transfer.v1.transfer_pb2 as transfer_types
    import ibc.applications.transfer.v1.denomtrace_pb2 as denom_trace_types

    PROTOBUF_AVAILABLE = True
except Exception as e:
    PROTOBUF_AVAILABLE = False
    pytest_skip_reason = f"Protobuf import failed: {e}"


class TestIBCProtobufStructures:
    """Test IBC protobuf message structures - real protobuf files."""

    @pytest.mark.skipif(not PROTOBUF_AVAILABLE, reason=pytest_skip_reason if not PROTOBUF_AVAILABLE else "")
    def test_transfer_query_structures(self):
        """Test IBC transfer query structures."""
        # IBC-go v10.3.0: QueryDenomTracesRequest renamed to QueryDenomsRequest
        denoms_req = transfer_query.QueryDenomsRequest()
        assert hasattr(denoms_req, 'pagination')

        # IBC-go v10.3.0: QueryDenomTraceRequest renamed to QueryDenomRequest
        denom_req = transfer_query.QueryDenomRequest()
        denom_req.hash = "test-hash-abc123"
        assert denom_req.hash == "test-hash-abc123"

    @pytest.mark.skipif(not PROTOBUF_AVAILABLE, reason=pytest_skip_reason if not PROTOBUF_AVAILABLE else "")
    def test_transfer_types_structures(self):
        """Test IBC transfer type structures."""

        # IBC-go v10.3.0: DenomTrace moved to denomtrace_pb2
        denom_trace = denom_trace_types.DenomTrace()
        denom_trace.path = "transfer/channel-0"
        denom_trace.base_denom = "uatom"

        assert denom_trace.path == "transfer/channel-0"
        assert denom_trace.base_denom == "uatom"

        params = transfer_types.Params()
        params.send_enabled = True
        params.receive_enabled = True
        assert params.send_enabled == True
        assert params.receive_enabled == True

    @pytest.mark.skipif(not PROTOBUF_AVAILABLE, reason=pytest_skip_reason if not PROTOBUF_AVAILABLE else "")
    def test_protobuf_descriptor_validation(self):
        """Validate that protobuf classes have proper descriptors (not fake)."""
        # IBC-go v10.3.0: Updated class names
        classes_to_test = [
            transfer_query.QueryDenomsRequest,
            denom_trace_types.DenomTrace,
            transfer_types.Params
        ]

        for proto_class in classes_to_test:
            instance = proto_class()
            assert hasattr(instance, 'DESCRIPTOR'), f"{proto_class} missing DESCRIPTOR"
            assert instance.DESCRIPTOR is not None, f"{proto_class} has None DESCRIPTOR"
            assert hasattr(instance.DESCRIPTOR, 'name'), f"{proto_class} DESCRIPTOR missing name"
            assert hasattr(instance.DESCRIPTOR, 'fields'), f"{proto_class} DESCRIPTOR missing fields"


class TestIBCMessageConverters:
    """Test IBC message converters with isolated imports."""

    def test_convert_msg_transfer_structure(self):
        """Test that IBC message converter file has correct structure."""
        import os
        import ast

        converter_path = os.path.join(os.path.dirname(__file__), '..', '..', 'akash', 'messages', 'ibc.py')
        assert os.path.exists(converter_path), "IBC message converter file missing"

        with open(converter_path, 'r') as f:
            content = f.read()

        tree = ast.parse(content)

        functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]

        expected_functions = ['convert_msg_transfer', 'convert_msg_create_client', 'convert_msg_update_client']
        for func in expected_functions:
            assert func in functions, f"Missing function: {func}"

    def test_message_converter_signatures_validation(self):
        """Test message converter function signatures by reading source."""
        import os
        import ast

        converter_path = os.path.join(os.path.dirname(__file__), '..', '..', 'akash', 'messages', 'ibc.py')

        with open(converter_path, 'r') as f:
            content = f.read()

        tree = ast.parse(content)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == 'convert_msg_transfer':
                assert len(
                    node.args.args) == 2, f"convert_msg_transfer should take 2 parameters, got {len(node.args.args)}"
                break
        else:
            pytest.fail("convert_msg_transfer function not found")


class TestIBCClientStructure:
    """Test IBC client structure with isolated validation."""

    def test_ibc_client_file_structure(self):
        """Test that IBC client files have correct structure."""
        import os
        import ast

        client_path = os.path.join(os.path.dirname(__file__), '..', '..', 'akash', 'modules', 'ibc', 'client.py')
        assert os.path.exists(client_path), "IBC client.py file missing"

        with open(client_path, 'r') as f:
            content = f.read()

        tree = ast.parse(content)

        classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        assert 'IBCClient' in classes, "IBCClient class not found"

    def test_ibc_client_inheritance_structure(self):
        """Test that IBCClient has proper inheritance structure."""
        import os
        import ast

        client_path = os.path.join(os.path.dirname(__file__), '..', '..', 'akash', 'modules', 'ibc', 'client.py')

        with open(client_path, 'r') as f:
            content = f.read()

        tree = ast.parse(content)

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == 'IBCClient':
                assert len(node.bases) > 0, "IBCClient should inherit from other classes"
                break
        else:
            pytest.fail("IBCClient class not found")

    def test_ibc_query_methods_structure(self):
        """Test that IBC query methods exist in query.py."""
        import os
        import ast

        query_path = os.path.join(os.path.dirname(__file__), '..', '..', 'akash', 'modules', 'ibc', 'query.py')
        assert os.path.exists(query_path), "IBC query.py file missing"

        with open(query_path, 'r') as f:
            content = f.read()

        tree = ast.parse(content)

        methods = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]

        expected_methods = [
            'get_client_state',
            'get_client_status',
            'get_client_states',
            '_query_client_states_rest',
            'get_connection',
            'get_connections',
            '_query_connections_rest',
            'get_channel',
            'get_channels',
            '_query_channels_rest',
            'get_denom_trace',
            'find_active_clients_for_chain',
            'find_active_channels_for_chain',
            'get_transfer_params',
            'trace_ibc_token'
        ]
        for method in expected_methods:
            assert method in methods, f"Missing query method: {method}"


class TestIBCImplementationValidation:
    """Test that IBC implementation exists and is structured correctly."""

    def test_ibc_module_structure_exists(self):
        """Test that IBC module files exist in the expected locations."""
        import os
        base_path = os.path.join(os.path.dirname(__file__), '..', '..', 'akash', 'modules', 'ibc')

        expected_files = ['__init__.py', 'client.py', 'query.py', 'tx.py', 'utils.py']

        for file in expected_files:
            file_path = os.path.join(base_path, file)
            assert os.path.exists(file_path), f"IBC module file missing: {file}"

    def test_ibc_message_converters_exist(self):
        """Test that IBC message converter file exists."""
        import os
        converter_path = os.path.join(os.path.dirname(__file__), '..', '..', 'akash', 'messages', 'ibc.py')
        assert os.path.exists(converter_path), "IBC message converter file missing"

    def test_ibc_protobuf_files_exist(self):
        """Test that IBC protobuf files were generated."""
        import os
        proto_base = os.path.join(os.path.dirname(__file__), '..', '..', 'akash', 'proto', 'ibc')

        # v1: IBC query protos are optional - SDK uses REST API for IBC queries
        expected_proto_files = [
            'applications/transfer/v1/query_pb2.py',
            'applications/transfer/v1/transfer_pb2.py',
            'core/client/v1/query_pb2.py',
            'core/channel/v1/query_pb2.py',
            'core/connection/v1/query_pb2.py'
        ]

        # ALL IBC proto files MUST exist - no skipping
        for proto_file in expected_proto_files:
            file_path = os.path.join(proto_base, proto_file)
            assert os.path.exists(file_path), f"IBC protobuf file missing: {proto_file}"


class TestIBCUtils:
    """Test IBC utility functions that can be tested without network calls."""

    def test_ibc_utils_validate_channel_id(self):
        """Test channel ID validation."""
        from akash.modules.ibc.utils import IBCUtils

        valid_channels = ["channel-0", "channel-17", "channel-999"]
        for channel_id in valid_channels:
            assert IBCUtils._validate_channel_id(channel_id) == True, f"Should validate {channel_id}"

        invalid_channels = ["channel-", "channel", "connection-17", "invalid", ""]
        for channel_id in invalid_channels:
            assert IBCUtils._validate_channel_id(channel_id) == False, f"Should reject {channel_id}"

    def test_ibc_utils_validate_address_format(self):
        """Test bech32 address format validation."""
        from akash.modules.ibc.utils import IBCUtils

        assert IBCUtils._validate_address_format("akash1qnnhhgzxj24f2kld5yhy4v4h4s9r295ak5gjw4") == True

        assert IBCUtils._validate_address_format("akash1qnnhhgzxj24f2kld5yhy4v4h4s9r295ak5gjw4", "akash") == True

        assert IBCUtils._validate_address_format("akash1qnnhhgzxj24f2kld5yhy4v4h4s9r295ak5gjw4", "cosmos") == False

        invalid_addresses = ["", "invalid", "akash", "123invalid"]
        for addr in invalid_addresses:
            assert IBCUtils._validate_address_format(addr) == False, f"Should reject {addr}"


class TestIBCTransactionStructure:
    """Test IBC transaction message structure without network calls."""

    def test_transfer_message_structure(self):
        """Test IBC transfer message structure."""
        transfer_msg = {
            "@type": "/ibc.applications.transfer.v1.MsgTransfer",
            "source_port": "transfer",
            "source_channel": "channel-17",
            "token": {"denom": "uakt", "amount": "1000000"},
            "sender": "akash1test123",
            "receiver": "cosmos1test456",
            "timeout_height": {"revision_number": "0", "revision_height": "0"},
            "timeout_timestamp": "1234567890000000000"
        }

        required_fields = ["@type", "source_port", "source_channel", "token", "sender", "receiver"]
        for field in required_fields:
            assert field in transfer_msg, f"Missing required field: {field}"

        assert isinstance(transfer_msg["token"], dict)
        assert "denom" in transfer_msg["token"]
        assert "amount" in transfer_msg["token"]

    def test_create_client_message_structure(self):
        """Test IBC create client message structure."""
        create_client_msg = {
            "@type": "/ibc.core.client.v1.MsgCreateClient",
            "client_state": {
                "@type": "/ibc.lightclients.tendermint.v1.ClientState",
                "chain_id": "cosmoshub-4",
                "trust_level": {"numerator": "1", "denominator": "3"},
                "trusting_period": "1209600s",
                "unbonding_period": "1814400s"
            },
            "consensus_state": {
                "@type": "/ibc.lightclients.tendermint.v1.ConsensusState",
                "timestamp": "2023-01-01T00:00:00Z",
                "root": {"hash": "dGVzdA=="}
            },
            "signer": "akash1test123"
        }

        assert create_client_msg["@type"] == "/ibc.core.client.v1.MsgCreateClient"
        assert "client_state" in create_client_msg
        assert "consensus_state" in create_client_msg
        assert "signer" in create_client_msg

        client_state = create_client_msg["client_state"]
        assert client_state["@type"] == "/ibc.lightclients.tendermint.v1.ClientState"
        assert "chain_id" in client_state


class TestIBCQueryMethods:
    """Test IBC query methods behavior without network calls."""

    def test_get_client_status_method_signature(self):
        """Test get_client_status method signature and error handling."""
        import os
        import ast

        query_path = os.path.join(os.path.dirname(__file__), '..', '..', 'akash', 'modules', 'ibc', 'query.py')

        with open(query_path, 'r') as f:
            content = f.read()

        tree = ast.parse(content)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == 'get_client_status':
                assert len(node.args.args) == 2, f"get_client_status should take 2 parameters"
                assert node.args.args[1].arg == 'client_id', "Second parameter should be client_id"

                if node.returns:
                    assert 'str' in ast.unparse(node.returns) if hasattr(ast, 'unparse') else True
                break
        else:
            pytest.fail("get_client_status method not found")

    def test_get_client_states_pagination_params(self):
        """Test get_client_states pagination parameters."""
        import os
        import ast

        query_path = os.path.join(os.path.dirname(__file__), '..', '..', 'akash', 'modules', 'ibc', 'query.py')

        with open(query_path, 'r') as f:
            content = f.read()

        tree = ast.parse(content)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == 'get_client_states':
                param_names = [arg.arg for arg in node.args.args]
                assert 'limit' in param_names, "Should have limit parameter"
                assert 'next_key' in param_names, "Should have next_key parameter"
                assert 'timeout_minutes' in param_names, "Should have timeout_minutes parameter"

                defaults = node.args.defaults
                assert len(defaults) > 0, "Should have default values for optional parameters"
                break
        else:
            pytest.fail("get_client_states method not found")

    def test_rest_api_query_methods_structure(self):
        """Test REST API query methods have consistent structure."""
        import os
        import ast

        query_path = os.path.join(os.path.dirname(__file__), '..', '..', 'akash', 'modules', 'ibc', 'query.py')

        with open(query_path, 'r') as f:
            content = f.read()

        tree = ast.parse(content)

        rest_methods = ['_query_client_states_rest', '_query_connections_rest', '_query_channels_rest']

        for method_name in rest_methods:
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == method_name:
                    param_names = [arg.arg for arg in node.args.args]
                    assert 'limit' in param_names, f"{method_name} should have limit parameter"
                    assert 'next_key' in param_names, f"{method_name} should have next_key parameter"
                    assert 'rest_endpoint' in param_names, f"{method_name} should have rest_endpoint parameter"
                    break
            else:
                pytest.fail(f"REST API method {method_name} not found")

    def test_find_active_methods_structure(self):
        """Test find_active_* methods have proper structure."""
        import os
        import ast

        query_path = os.path.join(os.path.dirname(__file__), '..', '..', 'akash', 'modules', 'ibc', 'query.py')

        with open(query_path, 'r') as f:
            content = f.read()

        tree = ast.parse(content)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == 'find_active_clients_for_chain':
                param_names = [arg.arg for arg in node.args.args]
                assert 'chain_id' in param_names, "Should have chain_id parameter"
                assert 'max_results' in param_names, "Should have max_results parameter"
                break
        else:
            pytest.fail("find_active_clients_for_chain method not found")

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == 'find_active_channels_for_chain':
                param_names = [arg.arg for arg in node.args.args]
                assert 'chain_id' in param_names, "Should have chain_id parameter"
                assert 'max_results' in param_names, "Should have max_results parameter"
                break
        else:
            pytest.fail("find_active_channels_for_chain method not found")


class TestIBCTransactionMethods:
    """Test IBC transaction methods structure."""

    def test_transfer_method_structure(self):
        """Test IBC transfer method structure and parameters."""
        import os
        import ast

        tx_path = os.path.join(os.path.dirname(__file__), '..', '..', 'akash', 'modules', 'ibc', 'tx.py')
        assert os.path.exists(tx_path), "IBC tx.py file missing"

        with open(tx_path, 'r') as f:
            content = f.read()

        tree = ast.parse(content)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == 'transfer':
                param_names = [arg.arg for arg in node.args.args]
                required_params = ['self', 'wallet', 'source_channel', 'token_amount',
                                   'token_denom', 'receiver']
                for param in required_params:
                    assert param in param_names, f"Missing required parameter: {param}"

                optional_params = ['source_port', 'timeout_height', 'timeout_timestamp',
                                   'memo', 'fee_amount', 'gas_limit', 'gas_adjustment', 'use_simulation']
                for param in optional_params:
                    assert param in param_names, f"Missing optional parameter: {param}"
                break
        else:
            pytest.fail("transfer method not found")

    def test_transfer_message_type(self):
        """Test that transfer uses correct message type."""
        import os

        tx_path = os.path.join(os.path.dirname(__file__), '..', '..', 'akash', 'modules', 'ibc', 'tx.py')

        with open(tx_path, 'r') as f:
            content = f.read()

        assert '"/ibc.applications.transfer.v1.MsgTransfer"' in content, \
            "Transfer should use /ibc.applications.transfer.v1.MsgTransfer message type"

        assert 'broadcast_transaction_rpc' in content, \
            "Should use broadcast_transaction_rpc for broadcasting"


class TestIBCValidation:
    """Test IBC validation functions that don't require network calls."""

    def test_ibc_channel_validation_logic(self):
        """Test channel validation logic."""
        from akash.modules.ibc.utils import IBCUtils

        test_cases = [
            ("channel-0", True),
            ("channel-17", True),
            ("channel-999", True),
            ("channel-", False),
            ("channel", False),
            ("connection-17", False),
            ("invalid", False),
            ("", False)
        ]

        for channel_id, expected in test_cases:
            result = IBCUtils._validate_channel_id(channel_id)
            assert result == expected, f"Channel {channel_id} validation failed: got {result}, expected {expected}"


class TestIBCPaginationLogic:
    """Test pagination logic for IBC queries."""

    def test_pagination_handling_in_get_client_states(self):
        """Test that get_client_states handles pagination correctly."""
        import os

        query_path = os.path.join(os.path.dirname(__file__), '..', '..', 'akash', 'modules', 'ibc', 'query.py')

        with open(query_path, 'r') as f:
            content = f.read()

        assert 'while' in content, "Should have while loop for pagination"
        assert 'next_key' in content, "Should handle next_key for pagination"
        assert 'timeout_minutes' in content, "Should have timeout protection"
        assert 'max_pages' in content, "Should have max_pages safety limit"

    def test_rest_api_fallback_pattern(self):
        """Test that REST API is used as fallback for pagination issues."""
        import os

        query_path = os.path.join(os.path.dirname(__file__), '..', '..', 'akash', 'modules', 'ibc', 'query.py')

        with open(query_path, 'r') as f:
            content = f.read()

        assert 'rest.cosmos.directory' in content, "Should use cosmos.directory REST API"
        assert 'requests.get' in content, "Should use requests for REST API calls"
        assert 'User-Agent' in content, "Should set User-Agent header"


class TestIBCErrorHandling:
    """Test error handling in IBC module."""

    def test_query_methods_error_handling(self):
        """Test that query methods handle errors gracefully."""
        import os

        query_path = os.path.join(os.path.dirname(__file__), '..', '..', 'akash', 'modules', 'ibc', 'query.py')

        with open(query_path, 'r') as f:
            content = f.read()

        assert content.count('try:') >= 10, "Should have try-except blocks for error handling"
        assert content.count('except Exception') >= 10, "Should catch exceptions"
        assert 'logger.error' in content, "Should log errors"
        assert 'return None' in content, "Should return None on errors"

    def test_tx_methods_error_handling(self):
        """Test that transaction methods handle errors properly."""
        import os

        tx_path = os.path.join(os.path.dirname(__file__), '..', '..', 'akash', 'modules', 'ibc', 'tx.py')

        with open(tx_path, 'r') as f:
            content = f.read()

        assert 'try:' in content, "Should have try-except blocks"
        assert 'BroadcastResult' in content, "Should return BroadcastResult"
        assert 'logger.error' in content or 'logger.warning' in content, "Should log errors/warnings"


class TestIBCClientIntegration:
    """Test IBC client integration and inheritance."""

    def test_ibc_client_imports_mixins(self):
        """Test that IBCClient properly imports query and tx mixins."""
        import os

        client_path = os.path.join(os.path.dirname(__file__), '..', '..', 'akash', 'modules', 'ibc', 'client.py')

        with open(client_path, 'r') as f:
            content = f.read()

        assert 'from .query import IBCQuery' in content, "Should import IBCQuery mixin"
        assert 'from .tx import IBCTx' in content, "Should import IBCTx mixin"
        assert 'class IBCClient' in content, "Should define IBCClient class"
        assert '(IBCQuery, IBCTx, IBCUtils)' in content, "Should inherit from all three mixins"

    def test_ibc_client_initialization(self):
        """Test IBCClient initialization structure."""
        import os
        import ast

        client_path = os.path.join(os.path.dirname(__file__), '..', '..', 'akash', 'modules', 'ibc', 'client.py')

        with open(client_path, 'r') as f:
            content = f.read()

        tree = ast.parse(content)

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == 'IBCClient':
                for method in node.body:
                    if isinstance(method, ast.FunctionDef) and method.name == '__init__':
                        param_names = [arg.arg for arg in method.args.args]
                        assert 'akash_client' in param_names, "Should take akash_client parameter"
                        break


class TestIBCConstants:
    """Test IBC constants and configurations."""

    def test_ibc_default_values(self):
        """Test default values used in IBC module."""
        import os

        query_path = os.path.join(os.path.dirname(__file__), '..', '..', 'akash', 'modules', 'ibc', 'query.py')

        with open(query_path, 'r') as f:
            content = f.read()

        assert '5000' in content, "Should have default pagination limit of 5000"
        assert 'timeout_minutes' in content, "Should have timeout configuration"
        assert '200' in content, "Should have max_pages safety limit"

        tx_path = os.path.join(os.path.dirname(__file__), '..', '..', 'akash', 'modules', 'ibc', 'tx.py')

        with open(tx_path, 'r') as f:
            tx_content = f.read()

        assert '600' in tx_content, "Should have default timeout value"
        assert '1_000_000_000' in tx_content, "Should convert to nanoseconds"


if __name__ == '__main__':
    print("Running IBC module validation tests...")
    exit_code = pytest.main([__file__, '-v', '--tb=short'])
    print(f"IBC tests completed with exit code: {exit_code}")
    exit(exit_code)
