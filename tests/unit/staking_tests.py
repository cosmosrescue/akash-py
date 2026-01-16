#!/usr/bin/env python3
"""
Staking module tests - validation and functional tests.

Validation tests: Validate protobuf message structures, field access patterns,
converter compatibility, and query parameter support without requiring
blockchain interactions. 

Functional tests: Test staking client query operations, transaction broadcasting,
validator operations, delegation management, and reward withdrawal using mocking
to isolate functionality and test error handling scenarios.

Run: python staking_tests.py
"""

import os

os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from akash.proto.cosmos.staking.v1beta1 import staking_pb2 as staking_pb
from akash.proto.cosmos.staking.v1beta1 import tx_pb2 as staking_tx
from akash.proto.cosmos.staking.v1beta1 import query_pb2 as staking_query


class TestStakingMessageStructures:
    """Test staking protobuf message structures and field access."""

    def test_msg_delegate_structure(self):
        """Test MsgDelegate message structure and field access."""
        msg_delegate = staking_tx.MsgDelegate()

        required_fields = ['delegator_address', 'validator_address', 'amount']
        for field in required_fields:
            assert hasattr(msg_delegate, field), f"MsgDelegate missing field: {field}"
        msg_delegate.delegator_address = "akash1delegator"
        msg_delegate.validator_address = "akashvaloper1validator"

        assert msg_delegate.delegator_address == "akash1delegator"
        assert msg_delegate.validator_address == "akashvaloper1validator"

        msg_delegate.amount.denom = "uakt"
        msg_delegate.amount.amount = "1000000"

        assert msg_delegate.amount.denom == "uakt"
        assert msg_delegate.amount.amount == "1000000"

    def test_msg_undelegate_structure(self):
        """Test MsgUndelegate message structure and field access."""
        msg_undelegate = staking_tx.MsgUndelegate()

        required_fields = ['delegator_address', 'validator_address', 'amount']
        for field in required_fields:
            assert hasattr(msg_undelegate, field), f"MsgUndelegate missing field: {field}"

    def test_msg_begin_redelegate_structure(self):
        """Test MsgBeginRedelegate message structure and field access."""
        msg_redelegate = staking_tx.MsgBeginRedelegate()

        required_fields = ['delegator_address', 'validator_src_address', 'validator_dst_address', 'amount']
        for field in required_fields:
            assert hasattr(msg_redelegate, field), f"MsgBeginRedelegate missing field: {field}"
        msg_redelegate.delegator_address = "akash1delegator"
        msg_redelegate.validator_src_address = "akashvaloper1source"
        msg_redelegate.validator_dst_address = "akashvaloper1dest"

        assert msg_redelegate.delegator_address == "akash1delegator"
        assert msg_redelegate.validator_src_address == "akashvaloper1source"
        assert msg_redelegate.validator_dst_address == "akashvaloper1dest"

    def test_validator_structure(self):
        """Test Validator message structure and field access."""
        validator = staking_pb.Validator()

        required_fields = ['operator_address', 'consensus_pubkey', 'jailed', 'status', 'tokens', 'delegator_shares',
                           'description', 'unbonding_height', 'unbonding_time', 'commission', 'min_self_delegation']
        for field in required_fields:
            assert hasattr(validator, field), f"Validator missing field: {field}"
        validator.operator_address = "akashvaloper1test"
        validator.jailed = False
        validator.tokens = "1000000000"

        assert validator.operator_address == "akashvaloper1test"
        assert validator.jailed == False
        assert validator.tokens == "1000000000"

    def test_delegation_structure(self):
        """Test Delegation message structure and field access."""
        delegation = staking_pb.Delegation()

        required_fields = ['delegator_address', 'validator_address', 'shares']
        for field in required_fields:
            assert hasattr(delegation, field), f"Delegation missing field: {field}"
        delegation.delegator_address = "akash1delegator"
        delegation.validator_address = "akashvaloper1validator"
        delegation.shares = "1000.000000000000000000"

        assert delegation.delegator_address == "akash1delegator"
        assert delegation.validator_address == "akashvaloper1validator"
        assert delegation.shares == "1000.000000000000000000"


class TestStakingQueryResponses:
    """Test staking query response structures."""

    def test_query_validators_response_structure(self):
        """Test QueryValidatorsResponse nested structure access."""
        response = staking_query.QueryValidatorsResponse()

        assert hasattr(response, 'validators'), "QueryValidatorsResponse missing validators field"
        assert hasattr(response, 'pagination'), "QueryValidatorsResponse missing pagination field"

        validator = staking_pb.Validator()
        validator.operator_address = "akashvaloper1test"
        validator.jailed = False

        response.validators.append(validator)

        first_validator = response.validators[0]
        assert hasattr(first_validator, 'operator_address'), "Validator missing operator_address field"
        assert hasattr(first_validator, 'jailed'), "Validator missing jailed field"
        assert first_validator.operator_address == "akashvaloper1test"

    def test_query_delegations_response_structure(self):
        """Test QueryDelegatorDelegationsResponse structure."""
        response = staking_query.QueryDelegatorDelegationsResponse()

        assert hasattr(response,
                       'delegation_responses'), "QueryDelegatorDelegationsResponse missing delegation_responses field"
        assert hasattr(response, 'pagination'), "QueryDelegatorDelegationsResponse missing pagination field"

        delegation_response = staking_pb.DelegationResponse()
        delegation_response.delegation.delegator_address = "akash1delegator"
        delegation_response.delegation.validator_address = "akashvaloper1validator"

        response.delegation_responses.append(delegation_response)

        assert len(response.delegation_responses) == 1
        assert response.delegation_responses[0].delegation.delegator_address == "akash1delegator"


class TestStakingMessageConverters:
    """Test staking message converters for transaction compatibility."""

    def test_all_staking_converters_registered(self):
        """Test that all staking message converters are registered."""
        from akash.tx import _MESSAGE_CONVERTERS, _initialize_message_converters

        if not _MESSAGE_CONVERTERS:
            _initialize_message_converters()

        required_converters = [
            "/cosmos.staking.v1beta1.MsgDelegate",
            "/cosmos.staking.v1beta1.MsgUndelegate",
            "/cosmos.staking.v1beta1.MsgBeginRedelegate",
            "/cosmos.staking.v1beta1.MsgCreateValidator",
            "/cosmos.staking.v1beta1.MsgEditValidator"
        ]

        for msg_type in required_converters:
            converter = _MESSAGE_CONVERTERS.get(msg_type)
            assert converter is not None, f"Missing converter for {msg_type}"
            assert callable(converter), f"Converter for {msg_type} is not callable"

    def test_delegation_messages_protobuf_compatibility(self):
        """Test delegation messages protobuf field compatibility."""
        msg_delegate = staking_tx.MsgDelegate()
        required_fields = ['delegator_address', 'validator_address', 'amount']
        for field in required_fields:
            assert hasattr(msg_delegate, field), f"MsgDelegate missing field: {field}"

        msg_undelegate = staking_tx.MsgUndelegate()
        for field in required_fields:
            assert hasattr(msg_undelegate, field), f"MsgUndelegate missing field: {field}"

        msg_redelegate = staking_tx.MsgBeginRedelegate()
        redelegate_fields = ['delegator_address', 'validator_src_address', 'validator_dst_address', 'amount']
        for field in redelegate_fields:
            assert hasattr(msg_redelegate, field), f"MsgBeginRedelegate missing field: {field}"

    def test_validator_messages_protobuf_compatibility(self):
        """Test validator messages protobuf field compatibility."""
        msg_create = staking_tx.MsgCreateValidator()
        create_fields = ['description', 'commission', 'min_self_delegation', 'delegator_address', 'validator_address',
                         'pubkey', 'value']
        for field in create_fields:
            assert hasattr(msg_create, field), f"MsgCreateValidator missing field: {field}"

        msg_edit = staking_tx.MsgEditValidator()
        edit_fields = ['description', 'validator_address', 'commission_rate', 'min_self_delegation']
        for field in edit_fields:
            assert hasattr(msg_edit, field), f"MsgEditValidator missing field: {field}"


class TestStakingQueryParameters:
    """Test staking query parameter compatibility."""

    def test_validator_query_request_structures(self):
        """Test validator query request structures."""
        validator_req = staking_query.QueryValidatorRequest()
        assert hasattr(validator_req, 'validator_addr'), "QueryValidatorRequest missing validator_addr field"

        validators_req = staking_query.QueryValidatorsRequest()
        assert hasattr(validators_req, 'status'), "QueryValidatorsRequest missing status field"
        assert hasattr(validators_req, 'pagination'), "QueryValidatorsRequest missing pagination field"

    def test_delegation_query_request_structures(self):
        """Test delegation query request structures."""
        delegation_req = staking_query.QueryDelegationRequest()
        assert hasattr(delegation_req, 'delegator_addr'), "QueryDelegationRequest missing delegator_addr field"
        assert hasattr(delegation_req, 'validator_addr'), "QueryDelegationRequest missing validator_addr field"

        delegator_delegations_req = staking_query.QueryDelegatorDelegationsRequest()
        assert hasattr(delegator_delegations_req,
                       'delegator_addr'), "QueryDelegatorDelegationsRequest missing delegator_addr field"
        assert hasattr(delegator_delegations_req,
                       'pagination'), "QueryDelegatorDelegationsRequest missing pagination field"


class TestStakingTransactionMessages:
    """Test staking transaction message structures."""

    def test_all_staking_message_types_exist(self):
        """Test all expected staking message types exist."""
        expected_messages = [
            'MsgDelegate', 'MsgUndelegate', 'MsgBeginRedelegate',
            'MsgCreateValidator', 'MsgEditValidator'
        ]

        for msg_name in expected_messages:
            assert hasattr(staking_tx, msg_name), f"Missing staking message type: {msg_name}"

            msg_class = getattr(staking_tx, msg_name)
            msg_instance = msg_class()
            assert msg_instance is not None

    def test_staking_message_response_types_exist(self):
        """Test staking message response types exist."""
        expected_responses = [
            'MsgDelegateResponse', 'MsgUndelegateResponse', 'MsgBeginRedelegateResponse',
            'MsgCreateValidatorResponse', 'MsgEditValidatorResponse'
        ]

        for response_name in expected_responses:
            assert hasattr(staking_tx, response_name), f"Missing staking response type: {response_name}"

            response_class = getattr(staking_tx, response_name)
            response_instance = response_class()
            assert response_instance is not None

    def test_delegation_message_consistency(self):
        """Test delegation message field consistency."""
        msg_delegate = staking_tx.MsgDelegate()
        msg_undelegate = staking_tx.MsgUndelegate()
        msg_redelegate = staking_tx.MsgBeginRedelegate()

        common_fields = ['delegator_address', 'amount']
        for field in common_fields:
            assert hasattr(msg_delegate, field), f"MsgDelegate missing: {field}"
            assert hasattr(msg_undelegate, field), f"MsgUndelegate missing: {field}"
            assert hasattr(msg_redelegate, field), f"MsgBeginRedelegate missing: {field}"

        assert hasattr(msg_delegate, 'validator_address'), "MsgDelegate missing validator_address"
        assert hasattr(msg_undelegate, 'validator_address'), "MsgUndelegate missing validator_address"
        assert hasattr(msg_redelegate, 'validator_src_address'), "MsgBeginRedelegate missing validator_src_address"
        assert hasattr(msg_redelegate, 'validator_dst_address'), "MsgBeginRedelegate missing validator_dst_address"


class TestStakingErrorPatterns:
    """Test common staking error patterns and edge cases."""

    def test_empty_validators_response_handling(self):
        """Test handling of empty validators response."""
        response = staking_query.QueryValidatorsResponse()

        assert len(response.validators) == 0, "Empty response should have no validators"

        assert hasattr(response, 'pagination'), "Empty response missing pagination"

    def test_empty_delegations_response_handling(self):
        """Test handling of empty delegations response."""
        response = staking_query.QueryDelegatorDelegationsResponse()

        assert len(response.delegation_responses) == 0, "Empty response should have no delegations"

    def test_validator_status_enum_handling(self):
        """Test validator status enum handling."""
        validator = staking_pb.Validator()

        assert hasattr(validator, 'status'), "Validator missing status field"

        status_values = [
            staking_pb.BOND_STATUS_UNSPECIFIED,
            staking_pb.BOND_STATUS_UNBONDED,
            staking_pb.BOND_STATUS_UNBONDING,
            staking_pb.BOND_STATUS_BONDED
        ]

        for status in status_values:
            validator.status = status
            assert validator.status == status, f"Validator status assignment failed for {status}"

    def test_zero_amount_handling(self):
        """Test handling of zero amounts."""
        msg_delegate = staking_tx.MsgDelegate()

        msg_delegate.amount.denom = "uakt"
        msg_delegate.amount.amount = "0"

        assert msg_delegate.amount.amount == "0"
        assert msg_delegate.amount.denom == "uakt"


class TestStakingModuleIntegration:
    """Test staking module integration and consistency."""

    def test_staking_converter_coverage(self):
        """Test all staking messages have converters in tx registry."""
        from akash.tx import _MESSAGE_CONVERTERS, _initialize_message_converters

        if not _MESSAGE_CONVERTERS:
            _initialize_message_converters()

        expected_converters = ['MsgDelegate', 'MsgUndelegate', 'MsgBeginRedelegate', 'MsgCreateValidator',
                               'MsgEditValidator']
        for msg_class in expected_converters:
            converter_key = f"/cosmos.staking.v1beta1.{msg_class}"
            assert converter_key in _MESSAGE_CONVERTERS, f"Missing converter for: {msg_class}"

    def test_staking_query_consistency(self):
        """Test staking query response consistency."""
        validator_response = staking_query.QueryValidatorResponse()
        validators_response = staking_query.QueryValidatorsResponse()

        assert hasattr(validator_response, 'validator'), "Single validator response missing validator"
        assert hasattr(validators_response, 'validators'), "Validators response missing validators"

    def test_address_consistency(self):
        """Test address handling consistency across staking structures."""
        msg_delegate = staking_tx.MsgDelegate()
        delegation = staking_pb.Delegation()
        validator = staking_pb.Validator()

        test_delegator = "akash1delegator123"
        test_validator = "akashvaloper1validator123"

        msg_delegate.delegator_address = test_delegator
        msg_delegate.validator_address = test_validator

        delegation.delegator_address = test_delegator
        delegation.validator_address = test_validator

        validator.operator_address = test_validator

        assert msg_delegate.delegator_address == test_delegator
        assert msg_delegate.validator_address == test_validator
        assert delegation.delegator_address == test_delegator
        assert delegation.validator_address == test_validator
        assert validator.operator_address == test_validator

    def test_coin_amount_consistency(self):
        """Test coin/amount handling consistency."""
        msg_delegate = staking_tx.MsgDelegate()
        msg_undelegate = staking_tx.MsgUndelegate()
        msg_redelegate = staking_tx.MsgBeginRedelegate()

        test_denom = "uakt"
        test_amount = "1000000"

        messages = [msg_delegate, msg_undelegate, msg_redelegate]
        for msg in messages:
            msg.amount.denom = test_denom
            msg.amount.amount = test_amount

            assert msg.amount.denom == test_denom, f"Amount denom inconsistent in {type(msg).__name__}"
            assert msg.amount.amount == test_amount, f"Amount value inconsistent in {type(msg).__name__}"

    def test_validator_lifecycle_consistency(self):
        """Test validator creation and editing message consistency."""
        msg_create = staking_tx.MsgCreateValidator()
        msg_edit = staking_tx.MsgEditValidator()

        test_validator = "akashvaloper1test"
        msg_create.validator_address = test_validator
        msg_edit.validator_address = test_validator

        assert msg_create.validator_address == test_validator
        assert msg_edit.validator_address == test_validator

        assert hasattr(msg_create, 'description'), "MsgCreateValidator missing description"
        assert hasattr(msg_edit, 'description'), "MsgEditValidator missing description"


import base64
from unittest.mock import Mock, patch

from akash.modules.staking import StakingClient
from akash.tx import BroadcastResult


class TestStakingClientInitialization:
    """Test StakingClient initialization and basic functionality."""

    def test_staking_client_initialization(self):
        """Test basic StakingClient initialization."""
        mock_akash_client = Mock()

        client = StakingClient(mock_akash_client)

        assert client.akash_client == mock_akash_client
        assert hasattr(client, 'get_validators')
        assert hasattr(client, 'delegate')


class TestStakingQueryOperations:
    """Test staking query operations with mocked responses."""

    def setup_method(self):
        """Setup staking client for testing."""
        self.mock_akash_client = Mock()
        self.client = StakingClient(self.mock_akash_client)

    def test_get_validators_success(self):
        """Test successful validators query."""
        mock_response_data = base64.b64encode(b"mock_validators_response").decode()
        self.mock_akash_client.rpc_query.return_value = {
            "response": {
                "code": 0,
                "value": mock_response_data
            }
        }

        with patch('akash.modules.staking.query.staking_query_pb2.QueryValidatorsResponse') as mock_response_class:
            mock_instance = Mock()
            mock_validator = Mock()
            mock_validator.operator_address = "akashvaloper1test"
            mock_validator.consensus_pubkey = "pubkey_data"
            mock_validator.jailed = False
            mock_validator.status = 3  # Bonded
            mock_validator.tokens = "1000000"
            mock_validator.delegator_shares = "1000000000000000000000000"
            mock_validator.description.moniker = "Test Validator"
            mock_validator.description.identity = ""
            mock_validator.description.website = ""
            mock_validator.description.details = ""
            mock_validator.commission.commission_rates.rate = "100000000000000000"
            mock_validator.commission.commission_rates.max_rate = "200000000000000000"
            mock_validator.commission.commission_rates.max_change_rate = "10000000000000000"
            mock_validator.min_self_delegation = "1"

            mock_instance.validators = [mock_validator]
            mock_response_class.return_value = mock_instance

            result = self.client.get_validators()

            assert len(result) == 1
            assert result[0]["operator_address"] == "akashvaloper1test"
            assert result[0]["jailed"] is False
            assert result[0]["description"]["moniker"] == "Test Validator"

    def test_get_validators_empty_response(self):
        """Test validators query with empty response."""
        self.mock_akash_client.rpc_query.return_value = {
            "response": {
                "code": 0,
                "value": ""
            }
        }

        result = self.client.get_validators()
        assert result == []

    def test_get_validators_error_response(self):
        """Test validators query with error response."""
        self.mock_akash_client.rpc_query.return_value = {
            "response": {
                "code": 1,
                "log": "Query failed"
            }
        }

        with pytest.raises(Exception, match="Query failed"):
            self.client.get_validators()

    def test_get_validators_with_status_filter_string(self):
        """Test validators query with status filter using string format."""
        mock_response_data = base64.b64encode(b"mock_validators_response").decode()
        self.mock_akash_client.rpc_query.return_value = {
            "response": {
                "code": 0,
                "value": mock_response_data
            }
        }

        with patch('akash.modules.staking.query.staking_query_pb2.QueryValidatorsResponse') as mock_response_class:
            mock_instance = Mock()
            mock_validator = Mock()
            mock_validator.operator_address = "akashvaloper1test"
            mock_validator.jailed = False
            mock_validator.status = 3  # BOND_STATUS_BONDED
            mock_validator.tokens = "1000000"
            mock_validator.delegator_shares = "1000000000000000000000000"
            mock_validator.description.moniker = "Test Validator"
            mock_validator.description.identity = ""
            mock_validator.description.website = ""
            mock_validator.description.details = ""
            mock_validator.commission.commission_rates.rate = "100000000000000000"
            mock_validator.commission.commission_rates.max_rate = "200000000000000000"
            mock_validator.commission.commission_rates.max_change_rate = "10000000000000000"
            mock_validator.min_self_delegation = "1000000"

            mock_instance.validators = [mock_validator]
            mock_response_class.return_value = mock_instance

            result = self.client.get_validators(status="BOND_STATUS_BONDED")

            assert isinstance(result, list)
            assert len(result) == 1
            assert result[0]["operator_address"] == "akashvaloper1test"
            assert result[0]["status"] == 3

    def test_get_validators_with_status_filter_numeric(self):
        """Test validators query with status filter using numeric format."""
        mock_response_data = base64.b64encode(b"mock_validators_response").decode()
        self.mock_akash_client.rpc_query.return_value = {
            "response": {
                "code": 0,
                "value": mock_response_data
            }
        }

        with patch('akash.modules.staking.query.staking_query_pb2.QueryValidatorsResponse') as mock_response_class:
            mock_instance = Mock()
            mock_validator = Mock()
            mock_validator.operator_address = "akashvaloper1test"
            mock_validator.jailed = False
            mock_validator.status = 1  # BOND_STATUS_UNBONDED
            mock_validator.tokens = "1000000"
            mock_validator.delegator_shares = "1000000000000000000000000"
            mock_validator.description.moniker = "Test Validator"
            mock_validator.description.identity = ""
            mock_validator.description.website = ""
            mock_validator.description.details = ""
            mock_validator.commission.commission_rates.rate = "100000000000000000"
            mock_validator.commission.commission_rates.max_rate = "200000000000000000"
            mock_validator.commission.commission_rates.max_change_rate = "10000000000000000"
            mock_validator.min_self_delegation = "1000000"

            mock_instance.validators = [mock_validator]
            mock_response_class.return_value = mock_instance

            result = self.client.get_validators(status="1")

            assert isinstance(result, list)
            assert len(result) == 1
            assert result[0]["operator_address"] == "akashvaloper1test"
            assert result[0]["status"] == 1

    def test_get_validators_invalid_status_filter(self):
        """Test validators query with invalid status filter."""
        with pytest.raises(ValueError, match="Invalid status value"):
            self.client.get_validators(status="INVALID_STATUS")

    def test_get_validator_found(self):
        """Test getting specific validator that exists."""
        mock_validators = [
            {"operator_address": "akashvaloper1test", "moniker": "Test Validator"},
            {"operator_address": "akashvaloper1other", "moniker": "Other Validator"}
        ]

        with patch.object(self.client, 'get_validators', return_value=mock_validators):
            result = self.client.get_validator("akashvaloper1test")

            assert result is not None
            assert result["operator_address"] == "akashvaloper1test"
            assert result["moniker"] == "Test Validator"

    def test_get_validator_not_found(self):
        """Test getting validator that doesn't exist."""
        with patch.object(self.client, 'get_validators', return_value=[]):
            result = self.client.get_validator("akashvaloper1nonexistent")
            assert result is None

    def test_get_delegations_success(self):
        """Test successful delegations query."""
        mock_response_data = base64.b64encode(b"mock_delegations_response").decode()
        self.mock_akash_client.rpc_query.return_value = {
            "response": {
                "code": 0,
                "value": mock_response_data
            }
        }

        with patch(
                'akash.modules.staking.query.staking_query_pb2.QueryDelegatorDelegationsResponse') as mock_response_class:
            mock_instance = Mock()
            mock_delegation_response = Mock()
            mock_delegation_response.delegation.delegator_address = "akash1test"
            mock_delegation_response.delegation.validator_address = "akashvaloper1test"
            mock_delegation_response.delegation.shares = "1000000000000000000000000"
            mock_delegation_response.balance.denom = "uakt"
            mock_delegation_response.balance.amount = "1000000"

            mock_instance.delegation_responses = [mock_delegation_response]
            mock_response_class.return_value = mock_instance

            result = self.client.get_delegations("akash1test")

            assert len(result) == 1
            assert result[0]["delegation"]["delegator_address"] == "akash1test"
            assert result[0]["balance"]["amount"] == "1000000"

    def test_get_delegations_empty(self):
        """Test delegations query with no delegations."""
        self.mock_akash_client.rpc_query.return_value = {
            "response": {
                "code": 0,
                "value": ""
            }
        }

        result = self.client.get_delegations("akash1test")
        assert result == []

    def test_get_delegation_success(self):
        """Test successful specific delegation query."""
        mock_response_data = base64.b64encode(b"mock_delegation_response").decode()
        self.mock_akash_client.rpc_query.return_value = {
            "response": {
                "code": 0,
                "value": mock_response_data
            }
        }

        with patch('akash.modules.staking.query.staking_query_pb2.QueryDelegationResponse') as mock_response_class:
            mock_instance = Mock()
            mock_delegation_response = Mock()
            mock_delegation_response.delegation.delegator_address = "akash1test"
            mock_delegation_response.delegation.validator_address = "akashvaloper1test"
            mock_delegation_response.delegation.shares = "1000000000000000000000000"
            mock_delegation_response.balance.denom = "uakt"
            mock_delegation_response.balance.amount = "1000000"

            mock_instance.delegation_response = mock_delegation_response
            mock_response_class.return_value = mock_instance

            result = self.client.get_delegation("akash1test", "akashvaloper1test")

            assert result is not None
            assert result["delegation"]["delegator_address"] == "akash1test"
            assert result["balance"]["amount"] == "1000000"

    def test_get_delegation_not_found(self):
        """Test delegation query when delegation doesn't exist."""
        self.mock_akash_client.rpc_query.return_value = {
            "response": {
                "code": 0,
                "value": ""
            }
        }

        result = self.client.get_delegation("akash1test", "akashvaloper1test")
        assert result is None

    def test_get_staking_params_success(self):
        """Test successful staking parameters query."""
        mock_response_data = base64.b64encode(b"mock_params_response").decode()
        self.mock_akash_client.rpc_query.return_value = {
            "response": {
                "code": 0,
                "value": mock_response_data
            }
        }

        with patch('akash.modules.staking.query.staking_query_pb2.QueryParamsResponse') as mock_response_class:
            mock_instance = Mock()
            mock_instance.params.unbonding_time = "1814400s"  # 21 days
            mock_instance.params.max_validators = 125
            mock_instance.params.max_entries = 7
            mock_instance.params.historical_entries = 10000
            mock_instance.params.bond_denom = "uakt"
            mock_instance.params.min_commission_rate = "50000000000000000"  # 0.05 or 5%

            mock_response_class.return_value = mock_instance

            result = self.client.get_staking_params()

            assert result["unbonding_time"] == "1814400s"
            assert result["max_validators"] == 125
            assert result["bond_denom"] == "uakt"
            assert result["min_commission_rate"] == "0.05"

    def test_get_pool_success(self):
        """Test successful staking pool query."""
        mock_response_data = base64.b64encode(b"mock_pool_response").decode()
        self.mock_akash_client.rpc_query.return_value = {
            "response": {
                "code": 0,
                "value": mock_response_data
            }
        }

        with patch('akash.modules.staking.query.staking_query_pb2.QueryPoolResponse') as mock_response_class:
            mock_instance = Mock()
            mock_instance.pool.not_bonded_tokens = "500000000"
            mock_instance.pool.bonded_tokens = "50000000000"

            mock_response_class.return_value = mock_instance

            result = self.client.get_pool()

            assert result["not_bonded_tokens"] == "500000000"
            assert result["bonded_tokens"] == "50000000000"


class TestStakingTransactionOperations:
    """Test staking transaction operations with mocked broadcasting."""

    def setup_method(self):
        """Setup staking client and wallet for testing."""
        self.mock_akash_client = Mock()
        self.client = StakingClient(self.mock_akash_client)
        self.mock_wallet = Mock()
        self.mock_wallet.address = "akash1test"

    @patch('akash.modules.staking.tx.broadcast_transaction_rpc')
    def test_delegate_success(self, mock_broadcast):
        """Test successful delegation transaction."""
        mock_broadcast.return_value = BroadcastResult(
            "ABCD1234", 0, "success", True
        )

        result = self.client.delegate(
            wallet=self.mock_wallet,
            validator_address="akashvaloper1test",
            amount="1000000",
            memo="Test delegation"
        )

        assert result.success is True
        assert result.tx_hash == "ABCD1234"

        mock_broadcast.assert_called_once()
        call_args = mock_broadcast.call_args
        messages = call_args[1]['messages']
        assert len(messages) == 1
        assert messages[0]['@type'] == '/cosmos.staking.v1beta1.MsgDelegate'
        assert messages[0]['validator_address'] == 'akashvaloper1test'
        assert messages[0]['amount']['amount'] == '1000000'

    @patch('akash.modules.staking.tx.broadcast_transaction_rpc')
    def test_delegate_exception(self, mock_broadcast):
        """Test delegation with exception."""
        mock_broadcast.side_effect = Exception("Broadcast failed")

        result = self.client.delegate(
            wallet=self.mock_wallet,
            validator_address="akashvaloper1test",
            amount="1000000"
        )

        assert result.success is False
        assert "Delegation failed" in result.raw_log

    @patch('akash.modules.staking.tx.broadcast_transaction_rpc')
    def test_undelegate_success(self, mock_broadcast):
        """Test successful undelegation transaction."""
        mock_broadcast.return_value = BroadcastResult(
            "EFGH5678", 0, "success", True
        )

        result = self.client.undelegate(
            wallet=self.mock_wallet,
            validator_address="akashvaloper1test",
            amount="500000",
            memo="Test undelegation"
        )

        assert result.success is True
        assert result.tx_hash == "EFGH5678"

        call_args = mock_broadcast.call_args
        messages = call_args[1]['messages']
        assert messages[0]['@type'] == '/cosmos.staking.v1beta1.MsgUndelegate'

    @patch('akash.modules.staking.tx.broadcast_transaction_rpc')
    def test_redelegate_success(self, mock_broadcast):
        """Test successful redelegation transaction."""
        mock_broadcast.return_value = BroadcastResult(
            "IJKL9012", 0, "success", True
        )

        result = self.client.redelegate(
            wallet=self.mock_wallet,
            src_validator_address="akashvaloper1test1",
            dst_validator_address="akashvaloper1test2",
            amount="250000",
            memo="Test redelegation"
        )

        assert result.success is True

        call_args = mock_broadcast.call_args
        messages = call_args[1]['messages']
        assert messages[0]['@type'] == '/cosmos.staking.v1beta1.MsgBeginRedelegate'
        assert messages[0]['validator_src_address'] == 'akashvaloper1test1'
        assert messages[0]['validator_dst_address'] == 'akashvaloper1test2'

    @patch('akash.modules.staking.tx.broadcast_transaction_rpc')
    def test_withdraw_rewards_success(self, mock_broadcast):
        """Test successful reward withdrawal."""
        mock_broadcast.return_value = BroadcastResult(
            "MNOP3456", 0, "success", True
        )

        result = self.client.withdraw_rewards(
            wallet=self.mock_wallet,
            validator_address="akashvaloper1test"
        )

        assert result.success is True

        call_args = mock_broadcast.call_args
        messages = call_args[1]['messages']
        assert messages[0]['@type'] == '/cosmos.distribution.v1beta1.MsgWithdrawDelegatorReward'
        assert messages[0]['validator_address'] == 'akashvaloper1test'

    @patch('akash.modules.staking.tx.broadcast_transaction_rpc')
    def test_withdraw_all_rewards_success(self, mock_broadcast):
        """Test successful withdrawal of all rewards."""
        mock_delegations = [
            {"delegation": {"validator_address": "akashvaloper1test1"}},
            {"delegation": {"validator_address": "akashvaloper1test2"}}
        ]

        with patch.object(self.client, 'get_delegations', return_value=mock_delegations):
            mock_broadcast.return_value = BroadcastResult(
                "QRST7890", 0, "success", True
            )

            result = self.client.withdraw_all_rewards(self.mock_wallet)

            assert result.success is True

            call_args = mock_broadcast.call_args
            messages = call_args[1]['messages']
            assert len(messages) == 2
            assert all(msg['@type'] == '/cosmos.distribution.v1beta1.MsgWithdrawDelegatorReward'
                       for msg in messages)

    @patch('akash.modules.staking.tx.broadcast_transaction_rpc')
    def test_withdraw_all_rewards_no_delegations(self, mock_broadcast):
        """Test withdraw all rewards with no delegations."""
        with patch.object(self.client, 'get_delegations', return_value=[]):
            result = self.client.withdraw_all_rewards(self.mock_wallet)

            assert result.success is False
            assert "No delegations found" in result.raw_log
            mock_broadcast.assert_not_called()

    @patch('akash.modules.staking.tx.broadcast_transaction_rpc')
    @patch('akash.modules.staking.tx.bech32.bech32_decode')
    @patch('akash.modules.staking.tx.bech32.bech32_encode')
    def test_create_validator_success(self, mock_encode, mock_decode, mock_broadcast):
        """Test successful validator creation."""
        mock_decode.return_value = ("akash", [1, 2, 3, 4, 5])
        mock_encode.return_value = "akashvaloper1test"

        mock_broadcast.return_value = BroadcastResult(
            "VWXY1234", 0, "success", True
        )

        validator_info = {
            "description": {"moniker": "Test Validator"},
            "commission": {"rate": "0.1", "max_rate": "0.2", "max_change_rate": "0.01"},
            "min_self_delegation": "1000000",
            "pubkey": {"@type": "/cosmos.crypto.ed25519.PubKey", "key": "test_key"},
            "value": {"denom": "uakt", "amount": "1000000"}
        }

        result = self.client.create_validator(
            wallet=self.mock_wallet,
            validator_info=validator_info
        )

        assert result.success is True

        call_args = mock_broadcast.call_args
        messages = call_args[1]['messages']
        assert messages[0]['@type'] == '/cosmos.staking.v1beta1.MsgCreateValidator'
        assert messages[0]['validator_address'] == 'akashvaloper1test'

    @patch('akash.modules.staking.tx.broadcast_transaction_rpc')
    @patch('akash.modules.staking.tx.bech32.bech32_decode')
    @patch('akash.modules.staking.tx.bech32.bech32_encode')
    def test_edit_validator_success(self, mock_encode, mock_decode, mock_broadcast):
        """Test successful validator editing."""
        mock_decode.return_value = ("akash", [1, 2, 3, 4, 5])
        mock_encode.return_value = "akashvaloper1test"

        mock_broadcast.return_value = BroadcastResult(
            "ZABC5678", 0, "success", True
        )

        description = {"moniker": "Updated Validator"}

        result = self.client.edit_validator(
            wallet=self.mock_wallet,
            description=description,
            commission_rate="0.15"
        )

        assert result.success is True

        call_args = mock_broadcast.call_args
        messages = call_args[1]['messages']
        assert messages[0]['@type'] == '/cosmos.staking.v1beta1.MsgEditValidator'
        assert "commission_rate" in messages[0]

    def test_edit_validator_no_params_error(self):
        """Test that edit_validator raises error when no parameters provided."""
        with pytest.raises(ValueError, match="At least one parameter"):
            self.client.edit_validator(wallet=self.mock_wallet)


class TestStakingUtilityFunctions:
    """Test staking utility functions and constants."""

    def setup_method(self):
        """Setup staking client for testing."""
        mock_akash_client = Mock()
        self.client = StakingClient(mock_akash_client)

        assert constants["module_name"] == "staking"
        assert constants["module_version"] == "v1beta1"
        assert "query_endpoints" in constants
        assert "transaction_endpoints" in constants
        assert "validator_address_prefixes" in constants
        assert "bond_statuses" in constants
        assert constants["default_denom"] == "uakt"

        assert "/cosmos.staking.v1beta1.Query/Validators" in constants["query_endpoints"]
        assert "/cosmos.staking.v1beta1.MsgDelegate" in constants["transaction_endpoints"]

        bond_statuses = constants["bond_statuses"]
        assert bond_statuses["BOND_STATUS_UNSPECIFIED"] == 0
        assert bond_statuses["BOND_STATUS_UNBONDED"] == 1
        assert bond_statuses["BOND_STATUS_UNBONDING"] == 2
        assert bond_statuses["BOND_STATUS_BONDED"] == 3

        assert constants["validator_address_prefixes"]["akash"] == "akashvaloper"


class TestStakingErrorHandlingScenarios:
    """Test staking error handling and edge cases."""

    def setup_method(self):
        """Setup staking client for testing."""
        self.mock_akash_client = Mock()
        self.client = StakingClient(self.mock_akash_client)
        self.mock_wallet = Mock()
        self.mock_wallet.address = "akash1test"

    def test_get_validators_network_error(self):
        """Test validators query with network error."""
        self.mock_akash_client.rpc_query.side_effect = Exception("Network error")

        with pytest.raises(Exception, match="Network error"):
            self.client.get_validators()

    def test_get_validators_no_response(self):
        """Test validators query with no response."""
        self.mock_akash_client.rpc_query.return_value = None

        with pytest.raises(Exception, match="Query failed"):
            self.client.get_validators()

    def test_get_validator_query_exception(self):
        """Test get_validator with query exception."""
        with patch.object(self.client, 'get_validators', side_effect=Exception("Query failed")):
            result = self.client.get_validator("akashvaloper1test")
            assert result is None

    def test_get_delegations_parsing_error(self):
        """Test delegations query with parsing error."""
        self.mock_akash_client.rpc_query.return_value = {
            "response": {
                "code": 0,
                "value": "invalid_base64"
            }
        }

        with pytest.raises(Exception):
            self.client.get_delegations("akash1test")

    def test_get_delegation_exception(self):
        """Test get_delegation with exception handling."""
        self.mock_akash_client.rpc_query.side_effect = Exception("Query failed")

        result = self.client.get_delegation("akash1test", "akashvaloper1test")
        assert result is None

    @patch('akash.modules.staking.tx.bech32.bech32_decode')
    def test_create_validator_invalid_address(self, mock_decode):
        """Test create_validator with invalid address."""
        mock_decode.return_value = (None, None)

        validator_info = {"description": {"moniker": "Test"}}

        with pytest.raises(Exception, match="Invalid wallet address"):
            self.client.create_validator(self.mock_wallet, validator_info)


class TestStakingQueryMissingCoverage:
    """Test previously uncovered staking query functions."""

    def test_query_unbonding_delegations_response_structure(self):
        """Test QueryUnbondingDelegationsResponse structure."""
        response = staking_query.QueryDelegatorUnbondingDelegationsResponse()

        assert hasattr(response, 'unbonding_responses'), "QueryDelegatorUnbondingDelegationsResponse missing unbonding_responses"
        assert hasattr(response, 'pagination'), "QueryDelegatorUnbondingDelegationsResponse missing pagination"

    def test_query_redelegations_response_structure(self):
        """Test QueryRedelegationsResponse structure."""
        response = staking_query.QueryRedelegationsResponse()

        assert hasattr(response, 'redelegation_responses'), "QueryRedelegationsResponse missing redelegation_responses"
        assert hasattr(response, 'pagination'), "QueryRedelegationsResponse missing pagination"

    def test_query_validator_delegations_response_structure(self):
        """Test QueryValidatorDelegationsResponse structure."""
        response = staking_query.QueryValidatorDelegationsResponse()

        assert hasattr(response, 'delegation_responses'), "QueryValidatorDelegationsResponse missing delegation_responses"
        assert hasattr(response, 'pagination'), "QueryValidatorDelegationsResponse missing pagination"


if __name__ == '__main__':
    print("Running staking module tests")
    print("=" * 50)
    print()
    print("Validation tests: protobuf structures, message converters, query responses")
    print("Functional tests: query operations, transaction broadcasting, error handling")
    print()
    print("These tests provide coverage without blockchain interactions.")
    print()

    pytest.main([__file__, '-v'])
