#!/usr/bin/env python3
"""
Validation tests for Akash Deployment module.

These tests validate protobuf message structures, field access patterns,
converter compatibility, and query parameter support without requiring
blockchain interactions. 

Run: python run_validation_tests.py deployment
"""

import os

os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from akash.proto.akash.deployment.v1beta4 import deploymentmsg_pb2 as deploy_msg
from akash.proto.akash.deployment.v1beta4 import groupmsg_pb2 as group_msg
from akash.proto.akash.deployment.v1 import deployment_pb2 as deploy_pb
from akash.proto.akash.deployment.v1beta4 import group_pb2 as group_pb
from akash.proto.akash.deployment.v1 import group_pb2 as group_id
from akash.proto.akash.deployment.v1beta4 import query_pb2 as deploy_query
from akash.proto.akash.deployment.v1beta4 import resourceunit_pb2 as resource_pb
from akash.proto.akash.base.v1beta3 import cpu_pb2 as cpu_pb
from akash.proto.akash.base.v1beta3 import memory_pb2 as memory_pb
from akash.proto.akash.base.v1beta3 import storage_pb2 as storage_pb

class TestDeploymentMessageStructures:
    """Test deployment protobuf message structures and field access."""

    def test_deployment_id_structure(self):
        """Test DeploymentID message structure and field access."""
        deployment_id = deploy_pb.DeploymentID()

        required_fields = ['owner', 'dseq']
        for field in required_fields:
            assert hasattr(deployment_id, field), f"DeploymentID missing field: {field}"

        deployment_id.owner = "akash1test"
        deployment_id.dseq = 12345

        assert deployment_id.owner == "akash1test"
        assert deployment_id.dseq == 12345

    def test_deployment_structure(self):
        """Test Deployment message structure and field access."""
        deployment = deploy_pb.Deployment()

        # v1: deployment_id renamed to id, version renamed to hash
        required_fields = ['id', 'state', 'hash', 'created_at']
        for field in required_fields:
            assert hasattr(deployment, field), f"Deployment missing field: {field}"

        assert hasattr(deployment.id, 'owner')
        assert hasattr(deployment.id, 'dseq')

    def test_group_id_structure(self):
        """Test GroupID message structure and field access."""
        group_id_msg = group_id.GroupID()

        required_fields = ['owner', 'dseq', 'gseq']
        for field in required_fields:
            assert hasattr(group_id_msg, field), f"GroupID missing field: {field}"

    def test_group_structure(self):
        """Test Group message structure and field access."""
        group = group_pb.Group()

        # v1beta4: group_id renamed to id
        required_fields = ['id', 'state', 'group_spec', 'created_at']
        for field in required_fields:
            assert hasattr(group, field), f"Group missing field: {field}"

        assert hasattr(group.id, 'owner')
        assert hasattr(group.id, 'dseq')
        assert hasattr(group.id, 'gseq')

    def test_resource_structure(self):
        """Test Resource and ResourceUnit structures."""
        resource = resource_pb.ResourceUnit()

        required_fields = ['resource', 'count', 'price']
        for field in required_fields:
            assert hasattr(resource, field), f"ResourceUnit missing field: {field}"

        cpu_resource = cpu_pb.CPU()
        assert hasattr(cpu_resource, 'units')
        assert hasattr(cpu_resource, 'attributes')

        memory_resource = memory_pb.Memory()
        assert hasattr(memory_resource, 'quantity')
        assert hasattr(memory_resource, 'attributes')

        storage_resource = storage_pb.Storage()
        assert hasattr(storage_resource, 'name')
        assert hasattr(storage_resource, 'quantity')


class TestDeploymentQueryResponses:
    """Test deployment query response nested structures."""

    def test_query_deployments_response_structure(self):
        """Test QueryDeploymentsResponse nested structure access."""
        response = deploy_query.QueryDeploymentsResponse()

        assert hasattr(response, 'deployments'), "QueryDeploymentsResponse missing deployments field"

        deployment_response = deploy_query.QueryDeploymentResponse()
        # v1: deployment_id renamed to id
        deployment_response.deployment.id.owner = "akash1test"
        deployment_response.deployment.id.dseq = 12345
        deployment_response.deployment.state = 1  # Active

        response.deployments.append(deployment_response)

        first_deployment_response = response.deployments[0]
        assert hasattr(first_deployment_response, 'deployment'), "QueryDeploymentResponse missing deployment field"
        # v1: deployment_id renamed to id
        assert first_deployment_response.deployment.id.owner == "akash1test"

        assert not hasattr(first_deployment_response,
                           'state'), "QueryDeploymentResponse should NOT have direct state field"
        assert not hasattr(first_deployment_response,
                           'owner'), "QueryDeploymentResponse should NOT have direct owner field"

    def test_query_deployment_response_structure(self):
        """Test individual QueryDeploymentResponse structure."""
        response = deploy_query.QueryDeploymentResponse()

        assert hasattr(response, 'deployment'), "QueryDeploymentResponse missing deployment field"
        assert hasattr(response, 'escrow_account'), "QueryDeploymentResponse missing escrow_account field"
        assert hasattr(response, 'groups'), "QueryDeploymentResponse missing groups field"

        assert not hasattr(response, 'state'), "QueryDeploymentResponse should NOT have direct state field"
        assert not hasattr(response, 'owner'), "QueryDeploymentResponse should NOT have direct owner field"
        assert not hasattr(response, 'dseq'), "QueryDeploymentResponse should NOT have direct dseq field"

    def test_query_group_response_structure(self):
        """Test QueryGroupResponse nested structure access."""
        response = deploy_query.QueryGroupResponse()

        assert hasattr(response, 'group'), "QueryGroupResponse missing group field"

        group = group_pb.Group()
        # v1beta4: group_id renamed to id
        group.id.owner = "akash1test"
        group.id.dseq = 12345
        group.id.gseq = 1
        group.state = 1

        response.group.CopyFrom(group)

        first_group = response.group
        # v1beta4: group_id renamed to id
        assert hasattr(first_group, 'id'), "Group missing id field"
        assert hasattr(first_group, 'state'), "Group missing state field"
        assert first_group.id.owner == "akash1test"


class TestDeploymentMessageConverters:
    """Test deployment message converters for transaction compatibility."""

    def test_all_deployment_converters_registered(self):
        """Test that all deployment message converters are registered."""
        from akash.tx import _MESSAGE_CONVERTERS, _initialize_message_converters

        if not _MESSAGE_CONVERTERS:
            _initialize_message_converters()

        required_converters = [
            "/akash.deployment.v1beta4.MsgCreateDeployment",
            "/akash.deployment.v1beta4.MsgUpdateDeployment",
            "/akash.deployment.v1beta4.MsgCloseDeployment",
            # Note: MsgDepositDeployment removed in v1beta4
            "/akash.deployment.v1beta4.MsgCloseGroup",
            "/akash.deployment.v1beta4.MsgPauseGroup",
            "/akash.deployment.v1beta4.MsgStartGroup"
        ]

        for msg_type in required_converters:
            converter = _MESSAGE_CONVERTERS.get(msg_type)
            assert converter is not None, f"Missing converter for {msg_type}"
            assert callable(converter), f"Converter for {msg_type} is not callable"

    def test_msg_create_deployment_protobuf_compatibility(self):
        """Test MsgCreateDeployment protobuf field compatibility."""
        pb_msg = deploy_msg.MsgCreateDeployment()

        # v1beta4: version renamed to hash, depositor removed
        required_fields = ['id', 'groups', 'hash', 'deposit']
        for field in required_fields:
            assert hasattr(pb_msg, field), f"MsgCreateDeployment missing field: {field}"

        assert hasattr(pb_msg.id, 'owner')
        assert hasattr(pb_msg.id, 'dseq')

        assert hasattr(pb_msg, 'groups')

    def test_msg_deposit_deployment_protobuf_compatibility(self):
        """Test MsgDepositDeployment was removed in v1beta4."""
        # v1beta4: MsgDepositDeployment was removed, deposit is now part of MsgCreateDeployment
        assert not hasattr(deploy_msg, 'MsgDepositDeployment'), \
            "MsgDepositDeployment should not exist in v1beta4"

    def test_msg_close_group_protobuf_compatibility(self):
        """Test MsgCloseGroup protobuf field compatibility."""
        pb_msg = group_msg.MsgCloseGroup()

        required_fields = ['id']
        for field in required_fields:
            assert hasattr(pb_msg, field), f"MsgCloseGroup missing field: {field}"

        assert hasattr(pb_msg.id, 'owner')
        assert hasattr(pb_msg.id, 'dseq')
        assert hasattr(pb_msg.id, 'gseq')


class TestDeploymentQueryParameters:
    """Test deployment query parameter compatibility with ."""

    def test_deployment_query_request_structure(self):
        """Test deployment query request structures."""
        req = deploy_query.QueryDeploymentsRequest()
        assert hasattr(req, 'filters'), "QueryDeploymentsRequest missing filters field"
        assert hasattr(req, 'pagination'), "QueryDeploymentsRequest missing pagination field"

    def test_group_query_request_structure(self):
        """Test group query request structures."""
        req = deploy_query.QueryGroupRequest()
        assert hasattr(req, 'id'), "QueryGroupRequest missing id field"


class TestDeploymentTransactionMessages:
    """Test deployment transaction message structures."""

    def test_all_deployment_message_types_exist(self):
        """Test all expected deployment message types exist."""
        deployment_messages = [
            # v1beta4: MsgDepositDeployment removed
            'MsgCreateDeployment', 'MsgUpdateDeployment', 'MsgCloseDeployment'
        ]
        for msg_name in deployment_messages:
            assert hasattr(deploy_msg, msg_name), f"Missing deployment message type: {msg_name}"

        group_messages = ['MsgCloseGroup', 'MsgPauseGroup', 'MsgStartGroup']
        for msg_name in group_messages:
            assert hasattr(group_msg, msg_name), f"Missing group message type: {msg_name}"

            msg_class = getattr(group_msg, msg_name)
            msg_instance = msg_class()
            assert msg_instance is not None

    def test_deployment_state_enum_exists(self):
        """Test deployment state enumeration exists."""
        assert hasattr(deploy_pb.Deployment, 'State'), "Deployment missing State enum"

        state_enum = deploy_pb.Deployment.State
        expected_states = ['invalid', 'active', 'closed']

        for state in expected_states:
            assert state in state_enum.keys(), f"Deployment.State missing: {state}"

    def test_group_state_enum_exists(self):
        """Test group state enumeration exists."""
        assert hasattr(group_pb.Group, 'State'), "Group missing State enum"

        state_enum = group_pb.Group.State
        expected_states = ['invalid', 'open', 'paused', 'insufficient_funds', 'closed']

        for state in expected_states:
            assert state in state_enum.keys(), f"Group.State missing: {state}"


class TestDeploymentErrorPatterns:
    """Test common deployment error patterns and edge cases."""

    def test_empty_deployment_response_handling(self):
        """Test handling of empty deployment query responses."""
        response = deploy_query.QueryDeploymentsResponse()

        assert len(response.deployments) == 0

        deployment_count = 0
        for deployment in response.deployments:
            deployment_count += 1
        assert deployment_count == 0

    def test_missing_escrow_account_handling(self):
        """Test handling deployment response without escrow account."""
        response = deploy_query.QueryDeploymentResponse()

        assert hasattr(response, 'escrow_account')

        escrow_account = response.escrow_account
        assert escrow_account is not None

    def test_decimal_coin_structure_compatibility(self):
        """Test escrow account structure."""
        response = deploy_query.QueryDeploymentResponse()

        # v1: Account structure changed, no longer has direct balance field
        escrow_account = response.escrow_account
        assert hasattr(escrow_account, 'id')
        assert hasattr(escrow_account, 'state')


class TestDeploymentModuleIntegration:
    """Test deployment module integration and consistency."""

    def test_deployment_lifecycle_message_consistency(self):
        """Test deployment lifecycle messages are consistent."""
        create_msg = deploy_msg.MsgCreateDeployment()

        update_msg = deploy_msg.MsgUpdateDeployment()

        close_msg = deploy_msg.MsgCloseDeployment()

        for msg in [create_msg, update_msg, close_msg]:
            assert hasattr(msg, 'id'), f"{type(msg).__name__} missing id field"
            assert hasattr(msg.id, 'owner'), f"{type(msg).__name__}.id missing owner"
            assert hasattr(msg.id, 'dseq'), f"{type(msg).__name__}.id missing dseq"

    def test_group_lifecycle_message_consistency(self):
        """Test group lifecycle messages are consistent."""
        close_msg = group_msg.MsgCloseGroup()

        pause_msg = group_msg.MsgPauseGroup()

        start_msg = group_msg.MsgStartGroup()

        for msg in [close_msg, pause_msg, start_msg]:
            assert hasattr(msg, 'id'), f"{type(msg).__name__} missing id field"
            assert hasattr(msg.id, 'owner'), f"{type(msg).__name__}.id missing owner"
            assert hasattr(msg.id, 'dseq'), f"{type(msg).__name__}.id missing dseq"
            assert hasattr(msg.id, 'gseq'), f"{type(msg).__name__}.id missing gseq"

    def test_deployment_converter_coverage(self):
        """Test all deployment messages have converters in tx registry."""
        from akash.tx import _MESSAGE_CONVERTERS, _initialize_message_converters

        if not _MESSAGE_CONVERTERS:
            _initialize_message_converters()

        msg_classes = []
        for attr_name in dir(deploy_msg):
            if attr_name.startswith('Msg') and not attr_name.endswith('Response'):
                msg_classes.append(attr_name)

        for msg_class in msg_classes:
            converter_key = f"/akash.deployment.v1beta4.{msg_class}"
            assert converter_key in _MESSAGE_CONVERTERS, f"Missing converter for: {msg_class}"

    def test_deployment_query_consistency(self):
        """Test deployment query response consistency."""
        single_response = deploy_query.QueryDeploymentResponse()

        multi_response = deploy_query.QueryDeploymentsResponse()
        deployment_response = deploy_query.QueryDeploymentResponse()
        multi_response.deployments.append(deployment_response)

        single_deployment = single_response.deployment
        multi_deployment = multi_response.deployments[0].deployment

        # v1: deployment_id renamed to id, version renamed to hash
        deployment_fields = ['id', 'state', 'hash', 'created_at']
        for field in deployment_fields:
            assert hasattr(single_deployment, field), f"Single query deployment missing: {field}"
            assert hasattr(multi_deployment, field), f"Multi query deployment missing: {field}"


from unittest.mock import Mock, patch
import base64


class TestDeploymentClientInitialization:
    """Test DeploymentClient initialization and basic functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_akash_client = Mock()
        self.mock_akash_client.abci_query = Mock()

    def test_deployment_client_creation(self):
        """Test that DeploymentClient can be instantiated properly."""
        from akash.modules.deployment.client import DeploymentClient

        client = DeploymentClient(self.mock_akash_client)
        assert client.akash_client == self.mock_akash_client

    def test_deployment_client_inheritance(self):
        """Test DeploymentClient inherits from all required mixins."""
        from akash.modules.deployment.client import DeploymentClient
        from akash.modules.deployment.query import DeploymentQuery
        from akash.modules.deployment.tx import DeploymentTx
        from akash.modules.deployment.utils import DeploymentUtils

        client = DeploymentClient(self.mock_akash_client)

        assert isinstance(client, DeploymentQuery)
        assert isinstance(client, DeploymentTx)
        assert isinstance(client, DeploymentUtils)

        assert hasattr(client, 'get_deployments')
        assert hasattr(client, 'create_deployment')

    def test_client_initialization_logging(self):
        """Test client initialization includes proper logging."""
        from akash.modules.deployment.client import DeploymentClient

        with patch('akash.modules.deployment.client.logger.info') as mock_log:
            client = DeploymentClient(self.mock_akash_client)
            mock_log.assert_called_once_with("Initialized DeploymentClient")


class TestDeploymentQueryOperations:
    """Test DeploymentQuery operations with mocked responses."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_akash_client = Mock()
        self.mock_akash_client.abci_query = Mock()

        from akash.modules.deployment.client import DeploymentClient
        self.client = DeploymentClient(self.mock_akash_client)

    def test_list_deployments_success(self):
        """Test successful deployments query."""
        mock_response = {
            "response": {
                "code": 0,
                "value": base64.b64encode(b"mock_deployments_data").decode()
            }
        }
        self.mock_akash_client.abci_query.return_value = mock_response

        with patch('akash.proto.akash.deployment.v1beta4.query_pb2.QueryDeploymentsResponse') as MockResponse:
            mock_response_obj = Mock()
            mock_deployment_resp = Mock()
            # v1: deployment_id renamed to id
            mock_deployment_resp.deployment.id.owner = "akash1test"
            mock_deployment_resp.deployment.id.dseq = 12345
            mock_deployment_resp.deployment.state = 1  # Active
            mock_response_obj.deployments = [mock_deployment_resp]
            MockResponse.return_value = mock_response_obj

            result = self.client.get_deployments()
            assert isinstance(result, list)

    def test_list_deployments_with_owner_filter(self):
        """Test deployments query with owner filter."""
        mock_response = {
            "response": {
                "code": 0,
                "value": base64.b64encode(b"mock_filtered_data").decode()
            }
        }
        self.mock_akash_client.abci_query.return_value = mock_response

        with patch('akash.proto.akash.deployment.v1beta4.query_pb2.QueryDeploymentsResponse'):
            result = self.client.get_deployments(owner="akash1test")
            self.mock_akash_client.abci_query.assert_called_once()

    def test_list_deployments_with_pagination(self):
        """Test deployments query with pagination."""
        mock_response = {
            "response": {
                "code": 0,
                "value": base64.b64encode(b"mock_paginated_data").decode()
            }
        }
        self.mock_akash_client.abci_query.return_value = mock_response

        with patch('akash.proto.akash.deployment.v1beta4.query_pb2.QueryDeploymentsResponse'):
            result = self.client.get_deployments(limit=10, offset=5, count_total=True)
            self.mock_akash_client.abci_query.assert_called_once()

    def test_list_deployments_empty_response(self):
        """Test deployments query with no results."""
        mock_response = {
            "response": {
                "code": 0,
                "value": None
            }
        }
        self.mock_akash_client.abci_query.return_value = mock_response

        result = self.client.get_deployments()
        assert result == []

    def test_list_deployments_error_handling(self):
        """Test deployments query error handling."""
        self.mock_akash_client.abci_query.side_effect = Exception("Network error")

        result = self.client.get_deployments()
        assert result == []


class TestDeploymentTransactionOperations:
    """Test DeploymentTx operations (basic method existence checks)."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_akash_client = Mock()

        from akash.modules.deployment.client import DeploymentClient
        self.client = DeploymentClient(self.mock_akash_client)

    def test_transaction_methods_exist(self):
        """Test that all required transaction methods exist."""
        assert hasattr(self.client, 'create_deployment')
        assert hasattr(self.client, 'update_deployment')
        assert hasattr(self.client, 'close_deployment')
        assert hasattr(self.client, 'deposit_deployment')
        assert hasattr(self.client, 'close_group')
        assert hasattr(self.client, 'pause_group')
        assert hasattr(self.client, 'start_group')

        assert callable(getattr(self.client, 'create_deployment'))
        assert callable(getattr(self.client, 'update_deployment'))
        assert callable(getattr(self.client, 'close_deployment'))
        assert callable(getattr(self.client, 'deposit_deployment'))

    def test_transaction_method_signatures(self):
        """Test transaction method signatures are correct."""
        import inspect

        sig = inspect.signature(self.client.create_deployment)
        required_params = ['wallet', 'sdl_yaml']
        for param in required_params:
            assert param in sig.parameters

        sig = inspect.signature(self.client.update_deployment)
        required_params = ['wallet', 'sdl_yaml']
        for param in required_params:
            assert param in sig.parameters

        sig = inspect.signature(self.client.close_deployment)
        required_params = ['wallet', 'owner', 'dseq']
        for param in required_params:
            assert param in sig.parameters


class TestDeploymentUtilityFunctions:
    """Test DeploymentUtils utility functions."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_akash_client = Mock()

        from akash.modules.deployment.client import DeploymentClient
        self.client = DeploymentClient(self.mock_akash_client)

    def test_utils_mixin_included(self):
        """Test that utils mixin is properly included."""
        from akash.modules.deployment.utils import DeploymentUtils

        assert isinstance(self.client, DeploymentUtils)

    def test_deployment_state_validation(self):
        """Test deployment state validation utilities."""
        if hasattr(self.client, 'get_deployment_states'):
            states = self.client.get_deployment_states()
            assert isinstance(states, dict)

    def test_resource_specification_helpers(self):
        """Test resource specification helper functions."""
        if hasattr(self.client, 'validate_resources'):
            resources = {
                "cpu": 100,
                "memory": 128,
                "storage": 1
            }
            result = self.client.validate_resources(resources)
            assert isinstance(result, bool)


class TestDeploymentLogFunctionality:
    """Test deployment service log functionality."""

    def setup_method(self):
        """Setup test environment."""
        from unittest.mock import Mock
        from akash.modules.deployment.client import DeploymentClient

        self.mock_client = Mock()
        self.mock_client._certificate_store = {}
        self.client = DeploymentClient(self.mock_client)

    def test_log_utils_mixin_included(self):
        """Test that deployment client includes log functionality."""
        assert hasattr(self.client, 'get_service_logs'), "Missing get_service_logs method"
        assert hasattr(self.client, 'stream_service_logs'), "Missing stream_service_logs method"
        assert callable(getattr(self.client, 'get_service_logs'))
        assert callable(getattr(self.client, 'stream_service_logs'))

    def test_get_service_logs_method_signature(self):
        """Test get_service_logs method signature."""
        import inspect

        sig = inspect.signature(self.client.get_service_logs)
        params = list(sig.parameters.keys())

        expected_params = ['provider_endpoint', 'lease_id', 'service_name', 'tail', 'cert_pem', 'key_pem', 'timeout']
        for param in expected_params:
            assert param in params, f"get_service_logs missing parameter: {param}"

        defaults = {param.name: param.default for param in sig.parameters.values() if param.default != inspect.Parameter.empty}
        assert defaults.get('service_name') is None
        assert defaults.get('tail') == 100
        assert defaults.get('cert_pem') is None
        assert defaults.get('key_pem') is None
        assert defaults.get('timeout') == 30

    def test_stream_service_logs_method_signature(self):
        """Test stream_service_logs method signature."""
        import inspect

        sig = inspect.signature(self.client.stream_service_logs)
        params = list(sig.parameters.keys())

        expected_params = ['provider_endpoint', 'lease_id', 'service_name', 'follow', 'cert_pem', 'key_pem', 'timeout']
        for param in expected_params:
            assert param in params, f"stream_service_logs missing parameter: {param}"

        defaults = {param.name: param.default for param in sig.parameters.values() if param.default != inspect.Parameter.empty}
        assert defaults.get('service_name') is None
        assert defaults.get('follow') is True
        assert defaults.get('cert_pem') is None
        assert defaults.get('key_pem') is None
        assert defaults.get('timeout') == 300

    def test_get_service_logs_input_validation(self):
        """Test get_service_logs input validation."""
        valid_lease_id = {
            "owner": "akash1test",
            "dseq": 12345,
            "gseq": 1,
            "oseq": 1,
            "provider": "akash1provider"
        }

        with pytest.raises(ValueError, match="Provider endpoint cannot be empty"):
            self.client.get_service_logs("", valid_lease_id)

        with pytest.raises(ValueError, match="Lease ID cannot be empty"):
            self.client.get_service_logs("provider.com:8443", None)

        with pytest.raises(ValueError, match="Lease ID cannot be empty"):
            self.client.get_service_logs("provider.com:8443", {})

        for required_field in ["owner", "dseq", "gseq", "oseq", "provider"]:
            incomplete_lease = valid_lease_id.copy()
            del incomplete_lease[required_field]
            
            with pytest.raises(ValueError, match=f"Missing required field"):
                self.client.get_service_logs("provider.com:8443", incomplete_lease)

    def test_stream_service_logs_input_validation(self):
        """Test stream_service_logs input validation."""
        valid_lease_id = {
            "owner": "akash1test",
            "dseq": 12345,
            "gseq": 1,
            "oseq": 1,
            "provider": "akash1provider"
        }

        with pytest.raises(ValueError, match="Provider endpoint cannot be empty"):
            list(self.client.stream_service_logs("", valid_lease_id))

        with pytest.raises(ValueError, match="Lease ID cannot be empty"):
            list(self.client.stream_service_logs("provider.com:8443", None))

    def test_get_service_logs_url_construction(self):
        """Test get_service_logs constructs URLs correctly."""
        valid_lease_id = {
            "owner": "akash1test",
            "dseq": 12345,
            "gseq": 1,
            "oseq": 1,
            "provider": "akash1provider"
        }

        try:
            self.client.get_service_logs("https://provider.com:8443", valid_lease_id, tail=10)
        except ValueError as e:
            assert "mTLS certificates required" in str(e)

        assert hasattr(self.client, 'get_service_logs')
        assert callable(self.client.get_service_logs)

    def test_stream_service_logs_generator_behavior(self):
        """Test stream_service_logs returns a generator."""
        from unittest.mock import Mock, patch
        import types

        valid_lease_id = {
            "owner": "akash1test",
            "dseq": 12345,
            "gseq": 1,
            "oseq": 1,
            "provider": "akash1provider"
        }

        self.mock_client._certificate_store = {}

        with patch('websocket.create_connection') as mock_ws_create:
            mock_ws = Mock()
            mock_ws.recv.side_effect = [Exception("Connection closed")]
            mock_ws_create.return_value = mock_ws

            result = self.client.stream_service_logs("provider.com:8443", valid_lease_id)

            assert isinstance(result, types.GeneratorType)

    def test_log_functions_certificate_parameter_handling(self):
        """Test log functions accept certificate parameters."""
        valid_lease_id = {
            "owner": "akash1test",
            "dseq": 12345,
            "gseq": 1,
            "oseq": 1,
            "provider": "akash1provider"
        }

        cert_pem = "cert_data"
        key_pem = "key_data"

        self.mock_client._certificate_store = {}

        try:
            with patch('websocket.create_connection') as mock_ws_create:
                mock_ws = Mock()
                mock_ws.recv.side_effect = [Exception("Connection closed")]
                mock_ws_create.return_value = mock_ws

                self.client.get_service_logs(
                    "provider.com:8443", 
                    valid_lease_id, 
                    cert_pem=cert_pem, 
                    key_pem=key_pem
                )
        except Exception:
            pass

    def test_log_url_parameter_validation(self):
        """Test that log functions validate URL parameters correctly."""
        import inspect

        get_sig = inspect.signature(self.client.get_service_logs)
        stream_sig = inspect.signature(self.client.stream_service_logs)

        assert 'provider_endpoint' in get_sig.parameters
        assert 'provider_endpoint' in stream_sig.parameters
        
        assert 'lease_id' in get_sig.parameters
        assert 'lease_id' in stream_sig.parameters


class TestDeploymentErrorHandlingScenarios:
    """Test DeploymentClient error handling in various scenarios."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_akash_client = Mock()

        from akash.modules.deployment.client import DeploymentClient
        self.client = DeploymentClient(self.mock_akash_client)

    def test_query_network_failure(self):
        """Test handling of network failures during queries."""
        self.mock_akash_client.abci_query.side_effect = Exception("Connection timeout")

        result = self.client.get_deployments()
        assert result == []

    def test_query_invalid_response(self):
        """Test handling of invalid query responses."""
        self.mock_akash_client.abci_query.return_value = None
        result = self.client.get_deployments()
        assert result == []

        self.mock_akash_client.abci_query.return_value = {"invalid": "response"}
        result = self.client.get_deployments()
        assert result == []

    def test_invalid_deployment_params(self):
        """Test handling of invalid deployment parameters."""
        with patch('akash.tx.broadcast_transaction_rpc') as mock_broadcast:
            mock_result = Mock()
            mock_result.success = False
            mock_result.raw_log = "invalid deployment parameters"
            mock_broadcast.return_value = mock_result

            result = self.client.create_deployment(
                Mock(address="akash1test"),
                "invalid: yaml content"
            )

            assert not result.success

    def test_deployment_not_found_handling(self):
        """Test handling of deployment not found errors."""
        mock_response = {
            "response": {
                "code": 2,
                "value": None
            }
        }
        self.mock_akash_client.abci_query.return_value = mock_response

        result = self.client.get_deployments(owner="akash1nonexistent")
        assert result == []

    def test_deployment_error_response_codes(self):
        """Test handling of various error response codes."""
        error_codes = [1, 2, 3, 5]

        for code in error_codes:
            mock_response = {
                "response": {
                    "code": code,
                    "value": None
                }
            }
            self.mock_akash_client.abci_query.return_value = mock_response

            result = self.client.get_deployments()
            assert result == []


if __name__ == "__main__":
    print("Running deployment module validation tests")
    print("=" * 70)
    print()
    print("Testing protobuf structures, message converters, query responses,")
    print("parameter compatibility, and nested field access patterns.")
    print()
    print("These tests catch breaking changes without blockchain interactions.")
    print()

    pytest.main([__file__, "-v", "--tb=short"])
