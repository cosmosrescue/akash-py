#!/usr/bin/env python3
"""
Validation tests for Cosmos Distribution module.

These tests validate protobuf message structures, field access patterns,
converter compatibility, and query parameter support without requiring
blockchain interactions. 

Run: python run_validation_tests.py distribution
"""

import os

os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from akash.proto.cosmos.distribution.v1beta1 import distribution_pb2 as dist_pb
from akash.proto.cosmos.distribution.v1beta1 import tx_pb2 as dist_tx
from akash.proto.cosmos.distribution.v1beta1 import query_pb2 as dist_query
from akash.proto.cosmos.base.v1beta1 import coin_pb2


class TestDistributionMessageStructures:
    """Test distribution protobuf message structures and field access."""

    def test_msg_withdraw_delegator_reward_structure(self):
        """Test MsgWithdrawDelegatorReward message structure and field access."""
        msg_withdraw = dist_tx.MsgWithdrawDelegatorReward()

        required_fields = ['delegator_address', 'validator_address']
        for field in required_fields:
            assert hasattr(msg_withdraw, field), f"MsgWithdrawDelegatorReward missing field: {field}"
        msg_withdraw.delegator_address = "akash1delegator"
        msg_withdraw.validator_address = "akashvaloper1validator"

        assert msg_withdraw.delegator_address == "akash1delegator"
        assert msg_withdraw.validator_address == "akashvaloper1validator"

    def test_msg_set_withdraw_address_structure(self):
        """Test MsgSetWithdrawAddress message structure and field access."""
        msg_set_address = dist_tx.MsgSetWithdrawAddress()

        required_fields = ['delegator_address', 'withdraw_address']
        for field in required_fields:
            assert hasattr(msg_set_address, field), f"MsgSetWithdrawAddress missing field: {field}"
        msg_set_address.delegator_address = "akash1delegator"
        msg_set_address.withdraw_address = "akash1withdraw"

        assert msg_set_address.delegator_address == "akash1delegator"
        assert msg_set_address.withdraw_address == "akash1withdraw"

    def test_delegation_delegator_reward_structure(self):
        """Test DelegationDelegatorReward message structure."""
        reward = dist_pb.DelegationDelegatorReward()

        required_fields = ['validator_address', 'reward']
        for field in required_fields:
            assert hasattr(reward, field), f"DelegationDelegatorReward missing field: {field}"
        reward.validator_address = "akashvaloper1validator"

        coin = coin_pb2.DecCoin()
        coin.denom = "uakt"
        coin.amount = "1000.500000000000000000"
        reward.reward.append(coin)

        assert reward.validator_address == "akashvaloper1validator"
        assert len(reward.reward) == 1
        assert reward.reward[0].denom == "uakt"

    def test_validator_outstanding_rewards_structure(self):
        """Test ValidatorOutstandingRewards message structure."""
        outstanding = dist_pb.ValidatorOutstandingRewards()

        assert hasattr(outstanding, 'rewards'), "ValidatorOutstandingRewards missing rewards field"
        coin = coin_pb2.DecCoin()
        coin.denom = "uakt"
        coin.amount = "5000.250000000000000000"
        outstanding.rewards.append(coin)

        assert len(outstanding.rewards) == 1
        assert outstanding.rewards[0].denom == "uakt"
        assert outstanding.rewards[0].amount == "5000.250000000000000000"

    def test_fee_pool_structure(self):
        """Test FeePool message structure."""
        fee_pool = dist_pb.FeePool()

        assert hasattr(fee_pool, 'community_pool'), "FeePool missing community_pool field"
        coin = coin_pb2.DecCoin()
        coin.denom = "uakt"
        coin.amount = "10000.750000000000000000"
        fee_pool.community_pool.append(coin)

        assert len(fee_pool.community_pool) == 1
        assert fee_pool.community_pool[0].denom == "uakt"


class TestDistributionQueryResponses:
    """Test distribution query response structures."""

    def test_query_delegation_rewards_response_structure(self):
        """Test QueryDelegationRewardsResponse structure."""
        response = dist_query.QueryDelegationRewardsResponse()

        assert hasattr(response, 'rewards'), "QueryDelegationRewardsResponse missing rewards field"
        coin = coin_pb2.DecCoin()
        coin.denom = "uakt"
        coin.amount = "2500.125000000000000000"
        response.rewards.append(coin)

        assert len(response.rewards) == 1
        assert response.rewards[0].denom == "uakt"

    def test_query_delegation_total_rewards_response_structure(self):
        """Test QueryDelegationTotalRewardsResponse structure."""
        response = dist_query.QueryDelegationTotalRewardsResponse()

        assert hasattr(response, 'rewards'), "QueryDelegationTotalRewardsResponse missing rewards field"
        assert hasattr(response, 'total'), "QueryDelegationTotalRewardsResponse missing total field"
        delegation_reward = dist_pb.DelegationDelegatorReward()
        delegation_reward.validator_address = "akashvaloper1validator"
        response.rewards.append(delegation_reward)

        total_coin = coin_pb2.DecCoin()
        total_coin.denom = "uakt"
        total_coin.amount = "7500.875000000000000000"
        response.total.append(total_coin)

        assert len(response.rewards) == 1
        assert len(response.total) == 1
        assert response.rewards[0].validator_address == "akashvaloper1validator"
        assert response.total[0].denom == "uakt"

    def test_query_community_pool_response_structure(self):
        """Test QueryCommunityPoolResponse structure."""
        response = dist_query.QueryCommunityPoolResponse()

        assert hasattr(response, 'pool'), "QueryCommunityPoolResponse missing pool field"
        coin = coin_pb2.DecCoin()
        coin.denom = "uakt"
        coin.amount = "15000.500000000000000000"
        response.pool.append(coin)

        assert len(response.pool) == 1
        assert response.pool[0].denom == "uakt"


class TestDistributionMessageConverters:
    """Test distribution message converters for transaction compatibility."""

    def test_all_distribution_converters_registered(self):
        """Test that all distribution message converters are registered."""
        from akash.tx import _MESSAGE_CONVERTERS, _initialize_message_converters

        if not _MESSAGE_CONVERTERS:
            _initialize_message_converters()

        required_converters = [
            "/cosmos.distribution.v1beta1.MsgWithdrawDelegatorReward",
            "/cosmos.distribution.v1beta1.MsgSetWithdrawAddress"
        ]

        for msg_type in required_converters:
            converter = _MESSAGE_CONVERTERS.get(msg_type)
            assert converter is not None, f"Missing converter for {msg_type}"
            assert callable(converter), f"Converter for {msg_type} is not callable"

    def test_withdraw_messages_protobuf_compatibility(self):
        """Test withdraw messages protobuf field compatibility."""
        msg_withdraw = dist_tx.MsgWithdrawDelegatorReward()
        required_fields = ['delegator_address', 'validator_address']
        for field in required_fields:
            assert hasattr(msg_withdraw, field), f"MsgWithdrawDelegatorReward missing field: {field}"

        msg_withdraw.delegator_address = "akash1test"
        msg_withdraw.validator_address = "akashvaloper1test"

        assert msg_withdraw.delegator_address == "akash1test"
        assert msg_withdraw.validator_address == "akashvaloper1test"

    def test_set_withdraw_address_protobuf_compatibility(self):
        """Test MsgSetWithdrawAddress protobuf field compatibility."""
        msg_set_address = dist_tx.MsgSetWithdrawAddress()

        required_fields = ['delegator_address', 'withdraw_address']
        for field in required_fields:
            assert hasattr(msg_set_address, field), f"MsgSetWithdrawAddress missing field: {field}"
        msg_set_address.delegator_address = "akash1delegator"
        msg_set_address.withdraw_address = "akash1withdraw"

        assert msg_set_address.delegator_address == "akash1delegator"
        assert msg_set_address.withdraw_address == "akash1withdraw"


class TestDistributionQueryParameters:
    """Test distribution query parameter compatibility."""

    def test_rewards_query_request_structures(self):
        """Test rewards query request structures."""
        delegation_rewards_req = dist_query.QueryDelegationRewardsRequest()
        assert hasattr(delegation_rewards_req,
                       'delegator_address'), "QueryDelegationRewardsRequest missing delegator_address field"
        assert hasattr(delegation_rewards_req,
                       'validator_address'), "QueryDelegationRewardsRequest missing validator_address field"

        total_rewards_req = dist_query.QueryDelegationTotalRewardsRequest()
        assert hasattr(total_rewards_req,
                       'delegator_address'), "QueryDelegationTotalRewardsRequest missing delegator_address field"

    def test_validator_query_request_structures(self):
        """Test validator-related query request structures."""
        commission_req = dist_query.QueryValidatorCommissionRequest()
        assert hasattr(commission_req,
                       'validator_address'), "QueryValidatorCommissionRequest missing validator_address field"

        outstanding_req = dist_query.QueryValidatorOutstandingRewardsRequest()
        assert hasattr(outstanding_req,
                       'validator_address'), "QueryValidatorOutstandingRewardsRequest missing validator_address field"

        slashes_req = dist_query.QueryValidatorSlashesRequest()
        assert hasattr(slashes_req, 'validator_address'), "QueryValidatorSlashesRequest missing validator_address field"
        assert hasattr(slashes_req, 'starting_height'), "QueryValidatorSlashesRequest missing starting_height field"
        assert hasattr(slashes_req, 'ending_height'), "QueryValidatorSlashesRequest missing ending_height field"

    def test_address_query_request_structures(self):
        """Test address-related query request structures."""
        withdraw_addr_req = dist_query.QueryDelegatorWithdrawAddressRequest()
        assert hasattr(withdraw_addr_req,
                       'delegator_address'), "QueryDelegatorWithdrawAddressRequest missing delegator_address field"

        delegator_validators_req = dist_query.QueryDelegatorValidatorsRequest()
        assert hasattr(delegator_validators_req,
                       'delegator_address'), "QueryDelegatorValidatorsRequest missing delegator_address field"


class TestDistributionTransactionMessages:
    """Test distribution transaction message structures."""

    def test_all_distribution_message_types_exist(self):
        """Test all expected distribution message types exist."""
        expected_messages = [
            'MsgWithdrawDelegatorReward', 'MsgSetWithdrawAddress',
            'MsgWithdrawValidatorCommission', 'MsgFundCommunityPool'
        ]

        for msg_name in expected_messages:
            assert hasattr(dist_tx, msg_name), f"Missing distribution message type: {msg_name}"

            msg_class = getattr(dist_tx, msg_name)
            msg_instance = msg_class()
            assert msg_instance is not None

    def test_distribution_message_response_types_exist(self):
        """Test distribution message response types exist."""
        expected_responses = [
            'MsgWithdrawDelegatorRewardResponse', 'MsgSetWithdrawAddressResponse',
            'MsgWithdrawValidatorCommissionResponse', 'MsgFundCommunityPoolResponse'
        ]

        for response_name in expected_responses:
            assert hasattr(dist_tx, response_name), f"Missing distribution response type: {response_name}"

            response_class = getattr(dist_tx, response_name)
            response_instance = response_class()
            assert response_instance is not None

    def test_withdraw_message_consistency(self):
        """Test withdraw message field consistency."""
        msg_withdraw_reward = dist_tx.MsgWithdrawDelegatorReward()
        msg_withdraw_commission = dist_tx.MsgWithdrawValidatorCommission()
        msg_set_address = dist_tx.MsgSetWithdrawAddress()

        assert hasattr(msg_withdraw_reward, 'delegator_address'), "MsgWithdrawDelegatorReward missing delegator_address"
        assert hasattr(msg_withdraw_reward, 'validator_address'), "MsgWithdrawDelegatorReward missing validator_address"
        assert hasattr(msg_withdraw_commission,
                       'validator_address'), "MsgWithdrawValidatorCommission missing validator_address"
        assert hasattr(msg_set_address, 'delegator_address'), "MsgSetWithdrawAddress missing delegator_address"
        assert hasattr(msg_set_address, 'withdraw_address'), "MsgSetWithdrawAddress missing withdraw_address"


class TestDistributionErrorPatterns:
    """Test common distribution error patterns and edge cases."""

    def test_empty_rewards_response_handling(self):
        """Test handling of empty rewards responses."""
        response = dist_query.QueryDelegationRewardsResponse()

        assert len(response.rewards) == 0, "Empty response should have no rewards"

    def test_empty_community_pool_response_handling(self):
        """Test handling of empty community pool response."""
        response = dist_query.QueryCommunityPoolResponse()

        assert len(response.pool) == 0, "Empty response should have no pool coins"

    def test_zero_rewards_handling(self):
        """Test handling of zero rewards."""
        reward = dist_pb.DelegationDelegatorReward()
        reward.validator_address = "akashvaloper1validator"

        coin = coin_pb2.DecCoin()
        coin.denom = "uakt"
        coin.amount = "0.000000000000000000"
        reward.reward.append(coin)

        assert len(reward.reward) == 1
        assert reward.reward[0].amount == "0.000000000000000000"

    def test_decimal_precision_handling(self):
        """Test handling of decimal precision in rewards."""
        coin = coin_pb2.DecCoin()
        coin.denom = "uakt"
        coin.amount = "123.456789012345678900"

        assert coin.amount == "123.456789012345678900"
        assert coin.denom == "uakt"


class TestDistributionModuleIntegration:
    """Test distribution module integration and consistency."""

    def test_distribution_converter_coverage(self):
        """Test all distribution messages have converters in tx registry."""
        from akash.tx import _MESSAGE_CONVERTERS, _initialize_message_converters

        if not _MESSAGE_CONVERTERS:
            _initialize_message_converters()

        expected_converters = ['MsgWithdrawDelegatorReward', 'MsgSetWithdrawAddress']
        for msg_class in expected_converters:
            converter_key = f"/cosmos.distribution.v1beta1.{msg_class}"
            assert converter_key in _MESSAGE_CONVERTERS, f"Missing converter for: {msg_class}"

    def test_distribution_query_consistency(self):
        """Test distribution query response consistency."""
        delegation_rewards_response = dist_query.QueryDelegationRewardsResponse()
        total_rewards_response = dist_query.QueryDelegationTotalRewardsResponse()

        assert hasattr(delegation_rewards_response, 'rewards'), "Delegation rewards response missing rewards"
        assert hasattr(total_rewards_response, 'rewards'), "Total rewards response missing rewards"
        assert hasattr(total_rewards_response, 'total'), "Total rewards response missing total"

    def test_address_consistency(self):
        """Test address handling consistency across distribution structures."""
        msg_withdraw = dist_tx.MsgWithdrawDelegatorReward()
        msg_set_address = dist_tx.MsgSetWithdrawAddress()

        test_delegator = "akash1delegator123"
        test_validator = "akashvaloper1validator123"
        test_withdraw = "akash1withdraw123"

        msg_withdraw.delegator_address = test_delegator
        msg_withdraw.validator_address = test_validator

        msg_set_address.delegator_address = test_delegator
        msg_set_address.withdraw_address = test_withdraw

        assert msg_withdraw.delegator_address == test_delegator
        assert msg_withdraw.validator_address == test_validator
        assert msg_set_address.delegator_address == test_delegator
        assert msg_set_address.withdraw_address == test_withdraw

    def test_decimal_coin_consistency(self):
        """Test decimal coin handling consistency across distribution structures."""
        reward = dist_pb.DelegationDelegatorReward()
        outstanding = dist_pb.ValidatorOutstandingRewards()
        fee_pool = dist_pb.FeePool()

        test_denom = "uakt"
        test_amount = "1234.567890123456789000"

        structures = [
            (reward, 'reward'),
            (outstanding, 'rewards'),
            (fee_pool, 'community_pool')
        ]

        for structure, field_name in structures:
            coin = coin_pb2.DecCoin()
            coin.denom = test_denom
            coin.amount = test_amount

            field = getattr(structure, field_name)
            field.append(coin)

            assert len(field) == 1, f"DecCoin addition failed for {type(structure).__name__}.{field_name}"
            assert field[0].denom == test_denom, f"Denom inconsistent in {type(structure).__name__}.{field_name}"
            assert field[0].amount == test_amount, f"Amount inconsistent in {type(structure).__name__}.{field_name}"

    def test_validator_address_consistency(self):
        """Test validator address consistency across distribution operations."""
        msg_withdraw_reward = dist_tx.MsgWithdrawDelegatorReward()
        msg_withdraw_commission = dist_tx.MsgWithdrawValidatorCommission()
        delegation_reward = dist_pb.DelegationDelegatorReward()

        test_validator = "akashvaloper1test123456"

        msg_withdraw_reward.validator_address = test_validator
        msg_withdraw_commission.validator_address = test_validator
        delegation_reward.validator_address = test_validator

        assert msg_withdraw_reward.validator_address == test_validator
        assert msg_withdraw_commission.validator_address == test_validator
        assert delegation_reward.validator_address == test_validator


from unittest.mock import Mock, patch
import base64


class TestDistributionClientInitialization:
    """Test DistributionClient initialization and basic functionality."""

    def setup_method(self):
        self.mock_akash_client = Mock()
        self.mock_akash_client.abci_query = Mock()

    def test_distribution_client_creation(self):
        """Test that DistributionClient can be instantiated properly."""
        from akash.modules.distribution.client import DistributionClient

        client = DistributionClient(self.mock_akash_client)
        assert client.akash_client == self.mock_akash_client

    def test_distribution_client_inheritance(self):
        """Test DistributionClient inherits from all required mixins."""
        from akash.modules.distribution.client import DistributionClient
        from akash.modules.distribution.query import DistributionQuery
        from akash.modules.distribution.tx import DistributionTx

        client = DistributionClient(self.mock_akash_client)

        assert isinstance(client, DistributionQuery)
        assert isinstance(client, DistributionTx)

        assert hasattr(client, 'get_delegator_rewards')
        assert hasattr(client, 'withdraw_delegator_reward')

    def test_client_initialization_logging(self):
        """Test client initialization includes proper logging."""
        from akash.modules.distribution.client import DistributionClient

        with patch('akash.modules.distribution.client.logger.info') as mock_log:
            client = DistributionClient(self.mock_akash_client)
            mock_log.assert_called_once_with("Initialized DistributionClient")


class TestDistributionQueryOperations:
    """Test DistributionQuery operations with mocked responses."""

    def setup_method(self):
        self.mock_akash_client = Mock()
        self.mock_akash_client.abci_query = Mock()

        from akash.modules.distribution.client import DistributionClient
        self.client = DistributionClient(self.mock_akash_client)

    def test_get_delegator_rewards_success(self):
        """Test successful delegator rewards query."""
        mock_response = {
            "response": {
                "code": 0,
                "value": base64.b64encode(b"mock_rewards_data").decode()
            }
        }
        self.mock_akash_client.abci_query.return_value = mock_response

        with patch('akash.proto.cosmos.distribution.v1beta1.query_pb2.QueryDelegationRewardsResponse') as MockResponse:
            mock_response_obj = Mock()
            mock_reward = Mock()
            mock_reward.amount = "1000000"
            mock_reward.denom = "uakt"
            mock_response_obj.rewards = [mock_reward]
            MockResponse.return_value = mock_response_obj

            result = self.client.get_delegator_rewards(
                "akash1delegator",
                "akashvaloper1validator"
            )
            assert isinstance(result, list)

    def test_get_delegator_total_rewards(self):
        """Test delegator total rewards query."""
        mock_response = {
            "response": {
                "code": 0,
                "value": base64.b64encode(b"mock_total_rewards").decode()
            }
        }
        self.mock_akash_client.abci_query.return_value = mock_response

        with patch('akash.proto.cosmos.distribution.v1beta1.query_pb2.QueryDelegationTotalRewardsResponse'):
            result = self.client.get_delegator_rewards("akash1delegator")
            self.mock_akash_client.abci_query.assert_called_once()

    def test_get_validator_commission(self):
        """Test validator commission query."""
        mock_response = {
            "response": {
                "code": 0,
                "value": base64.b64encode(b"mock_commission_data").decode()
            }
        }
        self.mock_akash_client.abci_query.return_value = mock_response

        if hasattr(self.client, 'get_validator_commission'):
            with patch('akash.proto.cosmos.distribution.v1beta1.query_pb2.QueryValidatorCommissionResponse'):
                result = self.client.get_validator_commission("akashvaloper1validator")
                self.mock_akash_client.abci_query.assert_called_once()

    def test_query_error_handling(self):
        """Test query error handling."""
        self.mock_akash_client.abci_query.side_effect = Exception("Network error")

        with pytest.raises(Exception) as exc_info:
            self.client.get_delegator_rewards("akash1delegator")

        assert "Network error" in str(exc_info.value)

    def test_query_empty_response(self):
        """Test handling of empty query responses."""
        mock_response = {
            "response": {
                "code": 0,
                "value": None
            }
        }
        self.mock_akash_client.abci_query.return_value = mock_response

        with pytest.raises(Exception) as exc_info:
            self.client.get_delegator_rewards("akash1delegator")

        assert "Empty or invalid response" in str(exc_info.value)


class TestDistributionTransactionOperations:
    """Test DistributionTx operations (method existence checks)."""

    def setup_method(self):
        self.mock_akash_client = Mock()

        from akash.modules.distribution.client import DistributionClient
        self.client = DistributionClient(self.mock_akash_client)

    def test_transaction_methods_exist(self):
        """Test that all required transaction methods exist."""
        assert hasattr(self.client, 'withdraw_delegator_reward')
        assert hasattr(self.client, 'set_withdraw_address')

        assert callable(getattr(self.client, 'withdraw_delegator_reward'))
        if hasattr(self.client, 'set_withdraw_address'):
            assert callable(getattr(self.client, 'set_withdraw_address'))

    def test_withdraw_delegator_reward_signature(self):
        """Test withdraw_delegator_reward method signature."""
        import inspect

        sig = inspect.signature(self.client.withdraw_delegator_reward)
        required_params = ['wallet', 'validator_address']
        for param in required_params:
            assert param in sig.parameters

    def test_transaction_method_parameters(self):
        """Test transaction methods have correct parameters."""
        import inspect

        sig = inspect.signature(self.client.withdraw_delegator_reward)
        param_names = list(sig.parameters.keys())

        assert 'wallet' in param_names
        assert 'validator_address' in param_names


class TestDistributionUtilityFunctions:
    """Test DistributionUtils utility functions."""

    def setup_method(self):
        self.mock_akash_client = Mock()

        from akash.modules.distribution.client import DistributionClient
        self.client = DistributionClient(self.mock_akash_client)

    def test_distribution_constants(self):
        """Test distribution module constants."""
        if hasattr(self.client, 'get_distribution_params'):
            self.mock_akash_client.abci_query.return_value = None
            with pytest.raises(Exception):
                self.client.get_distribution_params()

    def test_reward_calculation_helpers(self):
        """Test reward calculation helper functions."""
        if hasattr(self.client, 'calculate_rewards'):
            rewards = [{"amount": "1000000", "denom": "uakt"}]
            total = self.client.calculate_rewards(rewards)
            assert isinstance(total, (int, float, str))


class TestDistributionErrorHandlingScenarios:
    """Test DistributionClient error handling in various scenarios."""

    def setup_method(self):
        self.mock_akash_client = Mock()

        from akash.modules.distribution.client import DistributionClient
        self.client = DistributionClient(self.mock_akash_client)

    def test_query_network_failure(self):
        """Test handling of network failures during queries."""
        self.mock_akash_client.abci_query.side_effect = Exception("Connection timeout")

        with pytest.raises(Exception) as exc_info:
            self.client.get_delegator_rewards("akash1delegator")

        assert "Connection timeout" in str(exc_info.value)

    def test_invalid_addresses(self):
        """Test handling of invalid addresses."""
        mock_response = {
            "response": {
                "code": 1,
                "value": None
            }
        }
        self.mock_akash_client.abci_query.return_value = mock_response

        with pytest.raises(Exception):
            self.client.get_delegator_rewards("invalid_address")

    def test_protobuf_parsing_errors(self):
        """Test handling of protobuf parsing errors."""
        mock_response = {
            "response": {
                "code": 0,
                "value": base64.b64encode(b"invalid_protobuf_data").decode()
            }
        }
        self.mock_akash_client.abci_query.return_value = mock_response

        with pytest.raises(Exception):
            self.client.get_delegator_rewards("akash1delegator")

    def test_missing_response_fields(self):
        """Test handling of missing response fields."""
        self.mock_akash_client.abci_query.return_value = {"invalid": "response"}

        with pytest.raises(Exception):
            self.client.get_delegator_rewards("akash1delegator")

    def test_basic_parameter_validation(self):
        """Test basic parameter validation."""
        with pytest.raises(Exception):
            self.client.get_delegator_rewards("invalid_format")


class TestDistributionQueryMissingCoverage:
    """Test previously uncovered distribution query functions."""

    def test_query_validator_outstanding_rewards_response_structure(self):
        """Test QueryValidatorOutstandingRewardsResponse structure."""
        response = dist_query.QueryValidatorOutstandingRewardsResponse()

        assert hasattr(response, 'rewards'), "QueryValidatorOutstandingRewardsResponse missing rewards field"

    def test_query_community_pool_response_structure(self):
        """Test QueryCommunityPoolResponse structure."""
        response = dist_query.QueryCommunityPoolResponse()

        assert hasattr(response, 'pool'), "QueryCommunityPoolResponse missing pool field"

    def test_query_validator_slashes_response_structure(self):
        """Test QueryValidatorSlashesResponse structure."""
        response = dist_query.QueryValidatorSlashesResponse()

        assert hasattr(response, 'slashes'), "QueryValidatorSlashesResponse missing slashes field"
        assert hasattr(response, 'pagination'), "QueryValidatorSlashesResponse missing pagination field"


if __name__ == '__main__':
    print("Running distribution module validation tests")
    print("=" * 70)
    print()
    print("Testing protobuf structures, message converters, query responses,")
    print("parameter compatibility, and rewards/commission patterns.")
    print()
    print("These tests catch breaking changes without blockchain interactions.")
    print()

    pytest.main([__file__, '-v'])
