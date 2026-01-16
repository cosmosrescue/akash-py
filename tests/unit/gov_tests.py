#!/usr/bin/env python3
"""
Validation tests for Cosmos Gov module.

These tests validate protobuf message structures, field access patterns,
converter compatibility, and query parameter support without requiring
blockchain interactions. 

Run: python run_validation_tests.py gov
"""

import os

os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from akash.proto.cosmos.gov.v1beta1 import gov_pb2 as gov_pb
from akash.proto.cosmos.gov.v1beta1 import tx_pb2 as gov_tx
from akash.proto.cosmos.gov.v1beta1 import query_pb2 as gov_query
from akash.proto.cosmos.base.v1beta1 import coin_pb2


class TestGovMessageStructures:
    """Test gov protobuf message structures and field access."""

    def test_msg_submit_proposal_structure(self):
        """Test MsgSubmitProposal message structure and field access."""
        msg_submit = gov_tx.MsgSubmitProposal()

        required_fields = ['content', 'initial_deposit', 'proposer']
        for field in required_fields:
            assert hasattr(msg_submit, field), f"MsgSubmitProposal missing field: {field}"
        msg_submit.proposer = "akash1proposer"

        assert msg_submit.proposer == "akash1proposer"

        assert hasattr(msg_submit.content, 'type_url'), "Content missing type_url field"
        assert hasattr(msg_submit.content, 'value'), "Content missing value field"

        coin = coin_pb2.Coin()
        coin.denom = "uakt"
        coin.amount = "1000000"
        msg_submit.initial_deposit.append(coin)

        assert len(msg_submit.initial_deposit) == 1
        assert msg_submit.initial_deposit[0].denom == "uakt"

    def test_msg_deposit_structure(self):
        """Test MsgDeposit message structure and field access."""
        msg_deposit = gov_tx.MsgDeposit()

        required_fields = ['proposal_id', 'depositor', 'amount']
        for field in required_fields:
            assert hasattr(msg_deposit, field), f"MsgDeposit missing field: {field}"
        msg_deposit.proposal_id = 1
        msg_deposit.depositor = "akash1depositor"

        assert msg_deposit.proposal_id == 1
        assert msg_deposit.depositor == "akash1depositor"

        coin = coin_pb2.Coin()
        coin.denom = "uakt"
        coin.amount = "500000"
        msg_deposit.amount.append(coin)

        assert len(msg_deposit.amount) == 1

    def test_msg_vote_structure(self):
        """Test MsgVote message structure and field access."""
        msg_vote = gov_tx.MsgVote()

        required_fields = ['proposal_id', 'voter', 'option']
        for field in required_fields:
            assert hasattr(msg_vote, field), f"MsgVote missing field: {field}"
        msg_vote.proposal_id = 1
        msg_vote.voter = "akash1voter"
        msg_vote.option = gov_pb.VOTE_OPTION_YES

        assert msg_vote.proposal_id == 1
        assert msg_vote.voter == "akash1voter"
        assert msg_vote.option == gov_pb.VOTE_OPTION_YES

    def test_proposal_structure(self):
        """Test Proposal message structure and field access."""
        proposal = gov_pb.Proposal()

        required_fields = ['proposal_id', 'content', 'status', 'final_tally_result', 'submit_time', 'deposit_end_time',
                           'total_deposit', 'voting_start_time', 'voting_end_time']
        for field in required_fields:
            assert hasattr(proposal, field), f"Proposal missing field: {field}"
        proposal.proposal_id = 1
        proposal.status = gov_pb.PROPOSAL_STATUS_VOTING_PERIOD

        assert proposal.proposal_id == 1
        assert proposal.status == gov_pb.PROPOSAL_STATUS_VOTING_PERIOD

    def test_text_proposal_structure(self):
        """Test TextProposal message structure."""
        text_proposal = gov_pb.TextProposal()

        required_fields = ['title', 'description']
        for field in required_fields:
            assert hasattr(text_proposal, field), f"TextProposal missing field: {field}"
        text_proposal.title = "Test Proposal"
        text_proposal.description = "This is a test proposal description"

        assert text_proposal.title == "Test Proposal"
        assert text_proposal.description == "This is a test proposal description"

    def test_tally_result_structure(self):
        """Test TallyResult message structure."""
        tally = gov_pb.TallyResult()

        required_fields = ['yes', 'abstain', 'no', 'no_with_veto']
        for field in required_fields:
            assert hasattr(tally, field), f"TallyResult missing field: {field}"
        tally.yes = "1000000"
        tally.abstain = "500000"
        tally.no = "250000"
        tally.no_with_veto = "100000"

        assert tally.yes == "1000000"
        assert tally.abstain == "500000"
        assert tally.no == "250000"
        assert tally.no_with_veto == "100000"


class TestGovQueryResponses:
    """Test gov query response structures."""

    def test_query_proposal_response_structure(self):
        """Test QueryProposalResponse structure."""
        response = gov_query.QueryProposalResponse()

        assert hasattr(response, 'proposal'), "QueryProposalResponse missing proposal field"
        proposal = gov_pb.Proposal()
        proposal.proposal_id = 1
        proposal.status = gov_pb.PROPOSAL_STATUS_VOTING_PERIOD
        response.proposal.CopyFrom(proposal)

        assert response.proposal.proposal_id == 1
        assert response.proposal.status == gov_pb.PROPOSAL_STATUS_VOTING_PERIOD

    def test_query_proposals_response_structure(self):
        """Test QueryProposalsResponse structure."""
        response = gov_query.QueryProposalsResponse()

        assert hasattr(response, 'proposals'), "QueryProposalsResponse missing proposals field"
        assert hasattr(response, 'pagination'), "QueryProposalsResponse missing pagination field"
        proposal = gov_pb.Proposal()
        proposal.proposal_id = 1
        response.proposals.append(proposal)

        assert len(response.proposals) == 1
        assert response.proposals[0].proposal_id == 1

    def test_query_deposits_response_structure(self):
        """Test QueryDepositsResponse structure."""
        response = gov_query.QueryDepositsResponse()

        assert hasattr(response, 'deposits'), "QueryDepositsResponse missing deposits field"
        assert hasattr(response, 'pagination'), "QueryDepositsResponse missing pagination field"
        deposit = gov_pb.Deposit()
        deposit.proposal_id = 1
        deposit.depositor = "akash1depositor"
        response.deposits.append(deposit)

        assert len(response.deposits) == 1
        assert response.deposits[0].proposal_id == 1
        assert response.deposits[0].depositor == "akash1depositor"

    def test_query_votes_response_structure(self):
        """Test QueryVotesResponse structure."""
        response = gov_query.QueryVotesResponse()

        assert hasattr(response, 'votes'), "QueryVotesResponse missing votes field"
        assert hasattr(response, 'pagination'), "QueryVotesResponse missing pagination field"
        vote = gov_pb.Vote()
        vote.proposal_id = 1
        vote.voter = "akash1voter"
        response.votes.append(vote)

        assert len(response.votes) == 1
        assert response.votes[0].proposal_id == 1


class TestGovMessageConverters:
    """Test gov message converters for transaction compatibility."""

    def test_all_gov_converters_registered(self):
        """Test that all gov message converters are registered."""
        from akash.tx import _MESSAGE_CONVERTERS, _initialize_message_converters

        if not _MESSAGE_CONVERTERS:
            _initialize_message_converters()

        required_converters = [
            "/cosmos.gov.v1beta1.MsgSubmitProposal",
            "/cosmos.gov.v1beta1.MsgDeposit",
            "/cosmos.gov.v1beta1.MsgVote"
        ]

        for msg_type in required_converters:
            converter = _MESSAGE_CONVERTERS.get(msg_type)
            assert converter is not None, f"Missing converter for {msg_type}"
            assert callable(converter), f"Converter for {msg_type} is not callable"

    def test_msg_submit_proposal_protobuf_compatibility(self):
        """Test MsgSubmitProposal protobuf field compatibility."""
        pb_msg = gov_tx.MsgSubmitProposal()

        required_fields = ['content', 'initial_deposit', 'proposer']
        for field in required_fields:
            assert hasattr(pb_msg, field), f"MsgSubmitProposal missing field: {field}"
        pb_msg.proposer = "akash1test"

        assert pb_msg.proposer == "akash1test"

    def test_msg_deposit_protobuf_compatibility(self):
        """Test MsgDeposit protobuf field compatibility."""
        pb_msg = gov_tx.MsgDeposit()

        required_fields = ['proposal_id', 'depositor', 'amount']
        for field in required_fields:
            assert hasattr(pb_msg, field), f"MsgDeposit missing field: {field}"

    def test_msg_vote_protobuf_compatibility(self):
        """Test MsgVote protobuf field compatibility."""
        pb_msg = gov_tx.MsgVote()

        required_fields = ['proposal_id', 'voter', 'option']
        for field in required_fields:
            assert hasattr(pb_msg, field), f"MsgVote missing field: {field}"


class TestGovQueryParameters:
    """Test gov query parameter compatibility."""

    def test_proposal_query_request_structures(self):
        """Test proposal query request structures."""
        proposal_req = gov_query.QueryProposalRequest()
        assert hasattr(proposal_req, 'proposal_id'), "QueryProposalRequest missing proposal_id field"

        proposals_req = gov_query.QueryProposalsRequest()
        assert hasattr(proposals_req, 'proposal_status'), "QueryProposalsRequest missing proposal_status field"
        assert hasattr(proposals_req, 'voter'), "QueryProposalsRequest missing voter field"
        assert hasattr(proposals_req, 'depositor'), "QueryProposalsRequest missing depositor field"
        assert hasattr(proposals_req, 'pagination'), "QueryProposalsRequest missing pagination field"

    def test_deposit_query_request_structures(self):
        """Test deposit query request structures."""
        deposit_req = gov_query.QueryDepositRequest()
        assert hasattr(deposit_req, 'proposal_id'), "QueryDepositRequest missing proposal_id field"
        assert hasattr(deposit_req, 'depositor'), "QueryDepositRequest missing depositor field"

        deposits_req = gov_query.QueryDepositsRequest()
        assert hasattr(deposits_req, 'proposal_id'), "QueryDepositsRequest missing proposal_id field"
        assert hasattr(deposits_req, 'pagination'), "QueryDepositsRequest missing pagination field"

    def test_vote_query_request_structures(self):
        """Test vote query request structures."""
        vote_req = gov_query.QueryVoteRequest()
        assert hasattr(vote_req, 'proposal_id'), "QueryVoteRequest missing proposal_id field"
        assert hasattr(vote_req, 'voter'), "QueryVoteRequest missing voter field"

        votes_req = gov_query.QueryVotesRequest()
        assert hasattr(votes_req, 'proposal_id'), "QueryVotesRequest missing proposal_id field"
        assert hasattr(votes_req, 'pagination'), "QueryVotesRequest missing pagination field"


class TestGovTransactionMessages:
    """Test gov transaction message structures."""

    def test_all_gov_message_types_exist(self):
        """Test all expected gov message types exist."""
        expected_messages = [
            'MsgSubmitProposal', 'MsgDeposit', 'MsgVote'
        ]

        for msg_name in expected_messages:
            assert hasattr(gov_tx, msg_name), f"Missing gov message type: {msg_name}"

            msg_class = getattr(gov_tx, msg_name)
            msg_instance = msg_class()
            assert msg_instance is not None

    def test_proposal_lifecycle_consistency(self):
        """Test proposal lifecycle message consistency."""
        msg_submit = gov_tx.MsgSubmitProposal()
        msg_deposit = gov_tx.MsgDeposit()
        msg_vote = gov_tx.MsgVote()

        assert hasattr(msg_submit, 'proposer'), "MsgSubmitProposal missing proposer"
        assert hasattr(msg_deposit, 'proposal_id'), "MsgDeposit missing proposal_id"
        assert hasattr(msg_vote, 'proposal_id'), "MsgVote missing proposal_id"


class TestGovErrorPatterns:
    """Test common gov error patterns and edge cases."""

    def test_empty_proposals_response_handling(self):
        """Test handling of empty proposals response."""
        response = gov_query.QueryProposalsResponse()

        assert len(response.proposals) == 0, "Empty response should have no proposals"
        assert hasattr(response, 'pagination'), "Empty response missing pagination"

    def test_empty_deposit_handling(self):
        """Test handling of empty deposits."""
        msg_deposit = gov_tx.MsgDeposit()

        assert len(msg_deposit.amount) == 0, "MsgDeposit should start with empty amount list"

        coin = coin_pb2.Coin()
        coin.denom = "uakt"
        coin.amount = "1000000"
        msg_deposit.amount.append(coin)

        assert len(msg_deposit.amount) == 1

    def test_vote_option_enum_handling(self):
        """Test vote option enum handling."""
        msg_vote = gov_tx.MsgVote()

        vote_options = [
            gov_pb.VOTE_OPTION_UNSPECIFIED,
            gov_pb.VOTE_OPTION_YES,
            gov_pb.VOTE_OPTION_ABSTAIN,
            gov_pb.VOTE_OPTION_NO,
            gov_pb.VOTE_OPTION_NO_WITH_VETO
        ]

        for option in vote_options:
            msg_vote.option = option
            assert msg_vote.option == option, f"Vote option assignment failed for {option}"

    def test_proposal_status_enum_handling(self):
        """Test proposal status enum handling."""
        proposal = gov_pb.Proposal()

        status_values = [
            gov_pb.PROPOSAL_STATUS_UNSPECIFIED,
            gov_pb.PROPOSAL_STATUS_DEPOSIT_PERIOD,
            gov_pb.PROPOSAL_STATUS_VOTING_PERIOD,
            gov_pb.PROPOSAL_STATUS_PASSED,
            gov_pb.PROPOSAL_STATUS_REJECTED,
            gov_pb.PROPOSAL_STATUS_FAILED
        ]

        for status in status_values:
            proposal.status = status
            assert proposal.status == status, f"Proposal status assignment failed for {status}"


class TestGovModuleIntegration:
    """Test gov module integration and consistency."""

    def test_gov_converter_coverage(self):
        """Test all gov messages have converters in tx registry."""
        from akash.tx import _MESSAGE_CONVERTERS, _initialize_message_converters

        if not _MESSAGE_CONVERTERS:
            _initialize_message_converters()

        expected_converters = ['MsgSubmitProposal', 'MsgDeposit', 'MsgVote']
        for msg_class in expected_converters:
            converter_key = f"/cosmos.gov.v1beta1.{msg_class}"
            assert converter_key in _MESSAGE_CONVERTERS, f"Missing converter for: {msg_class}"

    def test_gov_query_consistency(self):
        """Test gov query response consistency."""
        proposal_response = gov_query.QueryProposalResponse()
        proposals_response = gov_query.QueryProposalsResponse()
        deposit_response = gov_query.QueryDepositResponse()
        deposits_response = gov_query.QueryDepositsResponse()

        assert hasattr(proposal_response, 'proposal'), "Single proposal response missing proposal"
        assert hasattr(proposals_response, 'proposals'), "Multiple proposals response missing proposals"
        assert hasattr(deposit_response, 'deposit'), "Single deposit response missing deposit"
        assert hasattr(deposits_response, 'deposits'), "Multiple deposits response missing deposits"

    def test_proposal_id_consistency(self):
        """Test proposal ID consistency across messages."""
        msg_deposit = gov_tx.MsgDeposit()
        msg_vote = gov_tx.MsgVote()
        proposal = gov_pb.Proposal()
        deposit = gov_pb.Deposit()
        vote = gov_pb.Vote()

        test_proposal_id = 42

        msg_deposit.proposal_id = test_proposal_id
        msg_vote.proposal_id = test_proposal_id
        proposal.proposal_id = test_proposal_id
        deposit.proposal_id = test_proposal_id
        vote.proposal_id = test_proposal_id

        assert msg_deposit.proposal_id == test_proposal_id
        assert msg_vote.proposal_id == test_proposal_id
        assert proposal.proposal_id == test_proposal_id
        assert deposit.proposal_id == test_proposal_id
        assert vote.proposal_id == test_proposal_id

    def test_address_consistency(self):
        """Test address handling consistency across gov structures."""
        msg_submit = gov_tx.MsgSubmitProposal()
        msg_deposit = gov_tx.MsgDeposit()
        msg_vote = gov_tx.MsgVote()
        deposit = gov_pb.Deposit()
        vote = gov_pb.Vote()

        test_address = "akash1test123456789"

        msg_submit.proposer = test_address
        msg_deposit.depositor = test_address
        msg_vote.voter = test_address
        deposit.depositor = test_address
        vote.voter = test_address

        assert msg_submit.proposer == test_address
        assert msg_deposit.depositor == test_address
        assert msg_vote.voter == test_address
        assert deposit.depositor == test_address
        assert vote.voter == test_address

    def test_coin_amount_consistency(self):
        """Test coin amount consistency in gov messages."""
        msg_submit = gov_tx.MsgSubmitProposal()
        msg_deposit = gov_tx.MsgDeposit()
        deposit = gov_pb.Deposit()

        test_denom = "uakt"
        test_amount = "1000000"

        structures = [
            (msg_submit, 'initial_deposit'),
            (msg_deposit, 'amount'),
            (deposit, 'amount')
        ]

        for structure, field_name in structures:
            coin = coin_pb2.Coin()
            coin.denom = test_denom
            coin.amount = test_amount

            field = getattr(structure, field_name)
            field.append(coin)

            assert len(field) == 1, f"Coin addition failed for {type(structure).__name__}.{field_name}"
            assert field[0].denom == test_denom, f"Denom inconsistent in {type(structure).__name__}.{field_name}"
            assert field[0].amount == test_amount, f"Amount inconsistent in {type(structure).__name__}.{field_name}"


class TestGovernanceClientFunctionality:
    """Test governance client functional behavior with mocked responses."""

    def test_governance_client_creation(self):
        """Test governance client initialization."""
        from akash.modules.governance.client import GovernanceClient
        from unittest.mock import Mock

        mock_client = Mock()
        client = GovernanceClient(mock_client)

        assert hasattr(client, 'akash_client')
        assert client.akash_client == mock_client
        assert hasattr(client, 'get_proposals')
        assert hasattr(client, 'submit_text_proposal')
        assert hasattr(client, 'vote')

    def test_get_proposals_method_structure(self):
        """Test get_proposals method accepts correct parameters."""
        from akash.modules.governance.client import GovernanceClient
        from unittest.mock import Mock

        mock_client = Mock()
        mock_client.abci_query.return_value = {'response': {'code': 0, 'value': None}}

        client = GovernanceClient(mock_client)

        result = client.get_proposals(status="voting_period")

        assert isinstance(result, list)
        mock_client.abci_query.assert_called_once()

    def test_get_proposal_method(self):
        """Test get_proposal method structure."""
        from akash.modules.governance.client import GovernanceClient
        from unittest.mock import Mock

        mock_client = Mock()
        mock_client.abci_query.return_value = {'response': {'code': 0, 'value': None}}

        client = GovernanceClient(mock_client)

        result = client.get_proposal(proposal_id=1)

        assert isinstance(result, dict)
        mock_client.abci_query.assert_called_once()

    def test_get_proposal_votes_method(self):
        """Test get_proposal_votes method structure."""
        from akash.modules.governance.client import GovernanceClient
        from unittest.mock import Mock

        mock_client = Mock()
        mock_client.abci_query.return_value = {'response': {'code': 0, 'value': None}}

        client = GovernanceClient(mock_client)

        result = client.get_proposal_votes(proposal_id=1)

        assert isinstance(result, list)
        mock_client.abci_query.assert_called_once()

    def test_get_vote_method(self):
        """Test get_vote method structure."""
        from akash.modules.governance.client import GovernanceClient
        from unittest.mock import Mock

        mock_client = Mock()
        mock_client.abci_query.return_value = {'response': {'code': 0, 'value': None}}

        client = GovernanceClient(mock_client)

        result = client.get_vote(proposal_id=1, voter_address="akash1voter")

        assert isinstance(result, dict)
        mock_client.abci_query.assert_called_once()

    def test_get_proposal_deposits_method(self):
        """Test get_proposal_deposits method structure."""
        from akash.modules.governance.client import GovernanceClient
        from unittest.mock import Mock

        mock_client = Mock()
        mock_client.abci_query.return_value = {'response': {'code': 0, 'value': None}}

        client = GovernanceClient(mock_client)

        result = client.get_proposal_deposits(proposal_id=1)

        assert isinstance(result, list)
        mock_client.abci_query.assert_called_once()

    def test_get_proposal_tally_method(self):
        """Test get_proposal_tally method structure."""
        from akash.modules.governance.client import GovernanceClient
        from unittest.mock import Mock

        mock_client = Mock()
        mock_client.abci_query.return_value = {'response': {'code': 0, 'value': None}}

        client = GovernanceClient(mock_client)

        result = client.get_proposal_tally(proposal_id=1)

        assert isinstance(result, dict)
        mock_client.abci_query.assert_called_once()

    def test_transaction_methods_exist(self):
        """Test governance transaction methods exist and are callable."""
        from akash.modules.governance.client import GovernanceClient
        from unittest.mock import Mock

        mock_client = Mock()
        client = GovernanceClient(mock_client)

        assert hasattr(client, 'submit_text_proposal')
        assert hasattr(client, 'submit_parameter_change_proposal')
        assert hasattr(client, 'submit_software_upgrade_proposal')
        assert hasattr(client, 'vote')
        assert hasattr(client, 'deposit')

        assert callable(client.submit_text_proposal)
        assert callable(client.vote)
        assert callable(client.deposit)

    def test_utility_methods_exist(self):
        """Test governance utility methods exist and are callable."""
        from akash.modules.governance.client import GovernanceClient
        from unittest.mock import Mock

        mock_client = Mock()
        client = GovernanceClient(mock_client)

        assert hasattr(client, 'get_proposal')
        assert hasattr(client, 'get_proposal_votes')
        assert hasattr(client, 'get_proposal_deposits')

        assert callable(client.get_proposal)

    def test_abci_query_path_usage(self):
        """Test that methods use correct ABCI query paths."""
        from akash.modules.governance.client import GovernanceClient
        from unittest.mock import Mock

        mock_client = Mock()
        mock_client.abci_query.return_value = {'response': {'code': 0, 'value': None}}

        client = GovernanceClient(mock_client)

        client.get_proposals()
        args, kwargs = mock_client.abci_query.call_args
        expected_path = '/cosmos.gov.v1beta1.Query/Proposals'
        assert args[0] == expected_path or kwargs.get('path') == expected_path

        mock_client.abci_query.reset_mock()

        client.get_proposal(1)
        args, kwargs = mock_client.abci_query.call_args
        expected_path = '/cosmos.gov.v1beta1.Query/Proposal'
        assert args[0] == expected_path or kwargs.get('path') == expected_path


class TestGovernanceTransactionFunctionality:
    """Test governance transaction functionality."""

    def test_submit_text_proposal_structure(self):
        """Test submit_text_proposal method exists and has correct signature."""
        from akash.modules.governance.client import GovernanceClient
        from unittest.mock import Mock
        import inspect

        mock_client = Mock()
        client = GovernanceClient(mock_client)

        assert hasattr(client, 'submit_text_proposal')
        assert callable(client.submit_text_proposal)

        sig = inspect.signature(client.submit_text_proposal)
        required_params = ['wallet', 'title', 'description']

        for param in required_params:
            assert param in sig.parameters, f"Missing parameter: {param}"

    def test_vote_transaction_structure(self):
        """Test vote method exists and has correct signature."""
        from akash.modules.governance.client import GovernanceClient
        from unittest.mock import Mock
        import inspect

        mock_client = Mock()
        client = GovernanceClient(mock_client)

        assert hasattr(client, 'vote')
        assert callable(client.vote)

        sig = inspect.signature(client.vote)
        required_params = ['wallet', 'proposal_id', 'option']

        for param in required_params:
            assert param in sig.parameters, f"Missing parameter: {param}"

    def test_deposit_transaction_structure(self):
        """Test deposit method exists and has correct signature."""
        from akash.modules.governance.client import GovernanceClient
        from unittest.mock import Mock
        import inspect

        mock_client = Mock()
        client = GovernanceClient(mock_client)

        assert hasattr(client, 'deposit')
        assert callable(client.deposit)

        sig = inspect.signature(client.deposit)
        required_params = ['wallet', 'proposal_id']

        for param in required_params:
            assert param in sig.parameters, f"Missing parameter: {param}"


class TestGovernanceErrorScenarios:
    """Test governance error handling and edge cases."""

    def test_network_timeout_handling(self):
        """Test handling of network timeouts."""
        from akash.modules.governance.client import GovernanceClient
        from unittest.mock import Mock

        mock_client = Mock()
        mock_client.abci_query.return_value = None

        client = GovernanceClient(mock_client)

        with pytest.raises(Exception):
            client.get_proposals()

    def test_invalid_response_handling(self):
        """Test handling of invalid API responses."""
        from akash.modules.governance.client import GovernanceClient
        from unittest.mock import Mock

        mock_client = Mock()
        mock_client.abci_query.return_value = {'invalid': 'response'}

        client = GovernanceClient(mock_client)

        with pytest.raises(Exception):
            client.get_proposal(1)

    def test_error_code_handling(self):
        """Test handling of error codes from ABCI query."""
        from akash.modules.governance.client import GovernanceClient
        from unittest.mock import Mock

        mock_client = Mock()
        mock_client.abci_query.return_value = {
            'response': {
                'code': 1,
                'log': 'Proposal not found'
            }
        }

        client = GovernanceClient(mock_client)

        with pytest.raises(Exception) as exc_info:
            client.get_proposal(1)

        assert "returned code 1" in str(exc_info.value)

    def test_empty_proposals_handling(self):
        """Test handling when no proposals exist."""
        from akash.modules.governance.client import GovernanceClient
        from unittest.mock import Mock

        mock_client = Mock()
        mock_client.abci_query.return_value = {
            'response': {
                'code': 0,
                'value': None
            }
        }

        client = GovernanceClient(mock_client)

        result = client.get_proposals()
        assert result == []

    def test_proposal_parameter_validation(self):
        """Test governance parameter validation."""


class TestGovernanceQueryMissingCoverage:
    """Test previously uncovered governance query functions."""

    def test_query_params_response_structure(self):
        """Test QueryParamsResponse structure for get_governance_params."""
        response = gov_query.QueryParamsResponse()

        assert hasattr(response, 'voting_params'), "QueryParamsResponse missing voting_params field"
        assert hasattr(response, 'deposit_params'), "QueryParamsResponse missing deposit_params field"
        assert hasattr(response, 'tally_params'), "QueryParamsResponse missing tally_params field"


if __name__ == '__main__':
    print("✅ Running gov module validation tests")
    print("=" * 70)
    print()
    print("Testing protobuf structures, message converters, query responses,")
    print("parameter compatibility, governance proposal/voting patterns,")
    print("and functional governance client behavior.")
    print()
    print("These tests catch breaking changes without blockchain interactions.")
    print()

    pytest.main([__file__, '-v'])
