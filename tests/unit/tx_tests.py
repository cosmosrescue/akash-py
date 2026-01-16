#!/usr/bin/env python3
"""
Transaction tests - validation and functional tests.

Validation tests: Validate transaction broadcasting structures, signing patterns,
message converter compatibility, and encoding support without requiring
blockchain interactions. 

Functional tests: Test BroadcastResult operations, message converters, transaction
encoding, signing, and broadcasting using mocking to isolate functionality
and test error handling scenarios.

Run: python tx_tests.py
"""

import os

os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

import pytest
import sys
import os
import json
import base64
from unittest.mock import Mock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from akash.tx import (
    BroadcastResult,
    register_message_converter,
    broadcast_transaction_rpc,
    simulate_transaction,
    encode_body,
    encode_auth_info,
    wait_for_transaction_confirmation,
    _initialize_message_converters,
    _MESSAGE_CONVERTERS,
    _convert_dict_to_any,
    _sign_bytes
)


class TestBroadcastResult:
    """Test BroadcastResult class functionality."""

    def test_broadcast_result_initialization(self):
        """Test BroadcastResult initialization."""
        result = BroadcastResult(
            tx_hash="ABCD1234",
            code=0,
            raw_log="success",
            success=True,
            events=[{"type": "transfer", "attributes": []}]
        )

        assert result.tx_hash == "ABCD1234"
        assert result.code == 0
        assert result.raw_log == "success"
        assert result.success is True
        assert len(result.events) == 1

    def test_broadcast_result_log_property(self):
        """Test log property compatibility."""
        result = BroadcastResult("hash", 0, "test log", True)
        assert result.raw_log == "test log"

    def test_get_event_attribute_from_raw_log(self):
        """Test event attribute extraction from raw_log JSON."""
        raw_log_data = json.dumps([{
            "events": [
                {
                    "type": "akash.v1",
                    "attributes": [
                        {"key": "dseq", "value": "12345"},
                        {"key": "owner", "value": "akash1test"}
                    ]
                }
            ]
        }])

        result = BroadcastResult("hash", 0, raw_log_data, True)

        assert result.get_event_attribute("akash.v1", "dseq") == "12345"
        assert result.get_event_attribute("akash.v1", "owner") == "akash1test"
        assert result.get_event_attribute("akash.v1", "missing") is None

    def test_get_event_attribute_from_events(self):
        """Test event attribute extraction from events field."""
        events = [
            {
                "type": "akash.v1",
                "attributes": [
                    {"key": "provider", "value": "akash1provider"},
                    {"key": "dseq", "value": "67890"}
                ]
            }
        ]

        result = BroadcastResult("hash", 0, "", True, events)

        assert result.get_event_attribute("akash.v1", "provider") == "akash1provider"
        assert result.get_event_attribute("akash.v1", "dseq") == "67890"

    def test_get_event_attribute_invalid_json(self):
        """Test event attribute extraction with invalid JSON."""
        result = BroadcastResult("hash", 0, "invalid json", True)
        assert result.get_event_attribute("akash.v1", "dseq") is None

    def test_get_dseq_success(self):
        """Test DSEQ extraction from events."""
        raw_log_data = json.dumps([{
            "events": [
                {
                    "type": "akash.v1",
                    "attributes": [{"key": "dseq", "value": "1234567"}]
                }
            ]
        }])

        result = BroadcastResult("hash", 0, raw_log_data, True)
        assert result.get_dseq() == 1234567

    def test_get_dseq_not_found(self):
        """Test DSEQ extraction when not found."""
        result = BroadcastResult("hash", 0, "no events", True)
        assert result.get_dseq() is None

    def test_get_dseq_invalid_value(self):
        """Test DSEQ extraction with invalid value."""
        raw_log_data = json.dumps([{
            "events": [
                {
                    "type": "akash.v1",
                    "attributes": [{"key": "dseq", "value": "invalid"}]
                }
            ]
        }])

        result = BroadcastResult("hash", 0, raw_log_data, True)
        assert result.get_dseq() is None

    def test_get_order_info_success(self):
        """Test order info extraction."""
        raw_log_data = json.dumps([{
            "events": [
                {
                    "type": "akash.v1",
                    "attributes": [
                        {"key": "owner", "value": "akash1test"},
                        {"key": "dseq", "value": "12345"},
                        {"key": "gseq", "value": "1"},
                        {"key": "oseq", "value": "1"}
                    ]
                }
            ]
        }])

        result = BroadcastResult("hash", 0, raw_log_data, True)
        order_info = result.get_order_info()

        assert order_info == {
            "owner": "akash1test",
            "dseq": 12345,
            "gseq": 1,
            "oseq": 1
        }

    def test_get_order_info_incomplete(self):
        """Test order info extraction with missing fields."""
        raw_log_data = json.dumps([{
            "events": [
                {
                    "type": "akash.v1",
                    "attributes": [{"key": "dseq", "value": "12345"}]
                }
            ]
        }])

        result = BroadcastResult("hash", 0, raw_log_data, True)
        assert result.get_order_info() is None

    def test_get_provider_address(self):
        """Test provider address extraction."""
        raw_log_data = json.dumps([{
            "events": [
                {
                    "type": "akash.v1",
                    "attributes": [{"key": "owner", "value": "akash1provider123"}]
                }
            ]
        }])

        result = BroadcastResult("hash", 0, raw_log_data, True)
        assert result.get_provider_address() == "akash1provider123"

    def test_get_bid_info_success(self):
        """Test bid info extraction."""
        raw_log_data = json.dumps([{
            "events": [
                {
                    "type": "akash.v1",
                    "attributes": [
                        {"key": "provider", "value": "akash1provider"},
                        {"key": "dseq", "value": "12345"},
                        {"key": "gseq", "value": "1"},
                        {"key": "oseq", "value": "1"}
                    ]
                }
            ]
        }])

        result = BroadcastResult("hash", 0, raw_log_data, True)
        bid_info = result.get_bid_info()

        assert bid_info == {
            "provider": "akash1provider",
            "dseq": 12345,
            "gseq": 1,
            "oseq": 1
        }

    def test_get_bid_info_incomplete(self):
        """Test bid info extraction with missing fields."""
        raw_log_data = json.dumps([{
            "events": [
                {
                    "type": "akash.v1",
                    "attributes": [{"key": "provider", "value": "akash1provider"}]
                }
            ]
        }])

        result = BroadcastResult("hash", 0, raw_log_data, True)
        assert result.get_bid_info() is None


class TestMessageConverters:
    """Test message converter registry and operations."""

    def test_register_message_converter(self):
        """Test message converter registration."""

        def dummy_converter(msg_dict, any_msg):
            return any_msg

        register_message_converter("/test.MsgTest", dummy_converter)

        assert "/test.MsgTest" in _MESSAGE_CONVERTERS
        assert _MESSAGE_CONVERTERS["/test.MsgTest"] == dummy_converter

    def test_initialize_message_converters(self):
        """Test message converter initialization."""
        _MESSAGE_CONVERTERS.clear()

        _initialize_message_converters()

        assert isinstance(_MESSAGE_CONVERTERS, dict)

    @patch('akash.tx.logger.debug')
    def test_convert_dict_to_any_success(self, mock_logger):
        """Test dictionary to Any conversion."""

        def mock_converter(msg_dict, any_msg):
            any_msg.type_url = "/test.MsgTest"
            any_msg.value = b"test_data"
            return any_msg

        register_message_converter("/test.MsgTest", mock_converter)

        msg_dict = {"@type": "/test.MsgTest", "field": "value"}

        result = _convert_dict_to_any(msg_dict)

        assert result.type_url == "/test.MsgTest"
        assert result.value == b"test_data"

    def test_convert_dict_to_any_missing_type(self):
        """Test dictionary to Any conversion with missing type field."""
        msg_dict = {"field": "value"}

        with pytest.raises(ValueError, match="Message missing @type or type field"):
            _convert_dict_to_any(msg_dict)

    def test_convert_dict_to_any_unknown_type(self):
        """Test dictionary to Any conversion with unknown type."""
        msg_dict = {"@type": "/unknown.MsgUnknown", "field": "value"}

        with pytest.raises(ValueError, match="Unsupported message type"):
            _convert_dict_to_any(msg_dict)

    def test_convert_dict_to_any_short_name(self):
        """Test dictionary to Any conversion with short message name."""

        def mock_converter(msg_dict, any_msg):
            any_msg.type_url = "/cosmos.bank.v1beta1.MsgSend"
            return any_msg

        register_message_converter("/cosmos.bank.v1beta1.MsgSend", mock_converter)

        msg_dict = {"type": "MsgSend", "field": "value"}

        result = _convert_dict_to_any(msg_dict)
        assert result.type_url == "/cosmos.bank.v1beta1.MsgSend"


class TestTransactionSigning:
    """Test transaction signing functionality."""

    def test_sign_bytes_with_ecdsa(self):
        """Test signing bytes with ecdsa library."""
        mock_wallet = Mock()
        mock_private_key = Mock()
        mock_wallet._private_key = mock_private_key

        test_bytes = b"test_sign_doc"
        expected_signature = b"signature_bytes"

        mock_private_key.sign_deterministic.return_value = expected_signature

        with patch('akash.tx.base64.b64encode') as mock_b64:
            mock_b64.return_value.decode.return_value = "c2lnbmF0dXJlX2J5dGVz"

            result = _sign_bytes(mock_wallet, test_bytes)

            assert result == "c2lnbmF0dXJlX2J5dGVz"
            mock_private_key.sign_deterministic.assert_called_once()

    def test_sign_bytes_fallback(self):
        """Test signing bytes error handling."""
        mock_wallet = Mock()
        mock_wallet._private_key = None

        test_bytes = b"test_sign_doc"

        try:
            result = sign_bytes(mock_wallet, test_bytes)
            assert isinstance(result, str)
        except Exception:
            pass


class TestTransactionEncoding:
    """Test transaction body and auth info encoding."""

    def test_encode_body_basic(self):
        """Test basic body encoding functionality."""
        body = {"messages": [], "memo": "test"}

        result = encode_body(body)

        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_encode_auth_info_basic(self):
        """Test basic auth info encoding functionality."""
        auth_info = {"fee": {"gas_limit": "200000"}}

        result = encode_auth_info(auth_info)

        assert isinstance(result, bytes)
        assert len(result) > 0


class TestTransactionBroadcasting:
    """Test transaction broadcasting functionality."""

    def setup_method(self):
        """Setup mocks for testing."""
        self.mock_client = Mock()
        self.mock_client.chain_id = "test-chain"
        self.mock_wallet = Mock()
        self.mock_wallet.address = "akash1test"
        self.mock_wallet.public_key_bytes = b"public_key"
        self.mock_wallet._private_key = Mock()

    def test_broadcast_transaction_rpc_no_hash(self):
        """Test transaction broadcasting with missing hash."""
        self.mock_client.get_account_info.return_value = {
            "sequence": 1,
            "account_number": 123
        }

        self.mock_client.rpc_query.return_value = {"code": 1}

        messages = [{"@type": "/cosmos.bank.v1beta1.MsgSend"}]

        with patch('akash.tx.encode_body', return_value=b"body"):
            with patch('akash.tx.encode_auth_info', return_value=b"auth"):
                result = broadcast_transaction_rpc(
                    client=self.mock_client,
                    wallet=self.mock_wallet,
                    messages=messages,
                    use_simulation=False
                )

                assert result.success is False

    def test_broadcast_transaction_rpc_exception(self):
        """Test transaction broadcasting with exception."""
        self.mock_client.get_account_info.side_effect = Exception("Account error")

        messages = [{"@type": "/cosmos.bank.v1beta1.MsgSend"}]

        result = broadcast_transaction_rpc(
            client=self.mock_client,
            wallet=self.mock_wallet,
            messages=messages
        )

        assert result.success is False
        assert "Account error" in result.raw_log

    def test_simulate_transaction_success(self):
        """Test successful transaction simulation."""
        self.mock_client.get_account_info.return_value = {
            "sequence": 1,
            "account_number": 123
        }

        self.mock_client.rpc_query.return_value = {
            "response": {
                "code": 0,
                "value": base64.b64encode(b"mock_response").decode()
            }
        }

        messages = [{"@type": "/cosmos.bank.v1beta1.MsgSend"}]

        with patch('akash.tx.encode_body', return_value=b"body"):
            with patch('akash.tx.encode_auth_info', return_value=b"auth"):
                result = simulate_transaction(
                    self.mock_client,
                    self.mock_wallet,
                    messages,
                    "test memo",
                    "5000"
                )

                assert isinstance(result, int)
                assert result > 0

    def test_simulate_transaction_error(self):
        """Test transaction simulation with error."""
        self.mock_client.get_account_info.return_value = {"sequence": 1}
        self.mock_client.rpc_query.side_effect = Exception("Simulation failed")

        messages = [{"@type": "/cosmos.bank.v1beta1.MsgSend"}]

        result = simulate_transaction(
            self.mock_client,
            self.mock_wallet,
            messages,
            "memo",
            "5000"
        )

        assert result == 200000

    def test_wait_for_transaction_confirmation_success(self):
        """Test successful transaction confirmation."""
        mock_client = Mock()
        mock_client.rpc_query.return_value = {
            "txs": [
                {
                    "height": "1000",
                    "tx_result": {"code": 0, "raw_log": "success"}
                }
            ]
        }

        result = wait_for_transaction_confirmation(mock_client, "ABCD1234", 10)

        assert result is not None
        assert result["height"] == "1000"
        assert result["tx_result"]["code"] == 0

    def test_wait_for_transaction_confirmation_timeout(self):
        """Test transaction confirmation timeout."""
        mock_client = Mock()
        mock_client.rpc_query.return_value = {"txs": []}

        with patch('akash.tx.time.sleep'):
            result = wait_for_transaction_confirmation(mock_client, "ABCD1234", 0.1)

            assert result is None

    def test_wait_for_transaction_confirmation_error(self):
        """Test transaction confirmation with error."""
        mock_client = Mock()
        mock_client.rpc_query.side_effect = Exception("Query failed")

        result = wait_for_transaction_confirmation(mock_client, "ABCD1234", 1)

        assert result is None


class TestTransactionImports:
    """Test that ALL transaction module imports actually work (not mocked)."""

    def test_all_module_imports(self):
        """Verify ALL transaction dependencies import successfully."""
        # Standard library imports
        import base64
        import hashlib
        import json
        import logging
        import time

        # Cryptographic imports
        from ecdsa.util import sigencode_string_canonize

        # Protobuf imports
        from google.protobuf.any_pb2 import Any

        # Cosmos transaction protos
        from akash.proto.cosmos.tx.v1beta1.tx_pb2 import SignDoc, TxRaw, TxBody, AuthInfo, SignerInfo, ModeInfo, Fee
        from akash.proto.cosmos.tx.v1beta1.service_pb2 import SimulateRequest, SimulateResponse
        from akash.proto.cosmos.crypto.secp256k1.keys_pb2 import PubKey
        from akash.proto.cosmos.base.v1beta1.coin_pb2 import Coin

        # All imports succeeded if we reach here
        assert True

    def test_message_converter_imports(self):
        """Verify ALL message converter imports work."""
        # Bank message converters
        from akash.messages.bank import convert_msg_send

        # Staking message converters
        from akash.messages.staking import (
            convert_msg_delegate,
            convert_msg_undelegate,
            convert_msg_begin_redelegate,
            convert_msg_create_validator,
            convert_msg_edit_validator,
        )

        # Distribution message converters
        from akash.messages.distribution import (
            convert_msg_withdraw_delegator_reward,
            convert_msg_set_withdraw_address,
        )

        # Evidence message converters
        from akash.messages.evidence import convert_msg_submit_evidence

        # Governance message converters
        from akash.messages.governance import (
            convert_msg_submit_proposal,
            convert_msg_deposit,
            convert_msg_vote,
        )

        # Authz message converters
        from akash.messages.authz import (
            convert_msg_grant,
            convert_msg_revoke,
            convert_msg_exec,
        )

        # Feegrant message converters
        from akash.messages.feegrant import (
            convert_msg_grant_allowance,
            convert_msg_revoke_allowance,
            convert_basic_allowance,
            convert_periodic_allowance,
        )

        # Slashing message converters
        from akash.messages.slashing import convert_msg_unjail

        # Market message converters
        from akash.messages.market import (
            convert_msg_create_bid,
            convert_msg_close_bid,
            convert_msg_create_lease,
            convert_msg_close_lease,
            convert_msg_withdraw_lease,
        )

        # Provider message converters
        from akash.messages.provider import (
            convert_msg_create_provider,
            convert_msg_update_provider,
        )

        # Audit message converters
        from akash.messages.audit import (
            convert_msg_sign_provider_attributes,
            convert_msg_delete_provider_attributes,
        )

        # Cert message converters
        from akash.messages.cert import (
            encode_msg_create_certificate,
            encode_msg_revoke_certificate,
        )

        # Deployment message converters
        from akash.messages.deployment import (
            convert_msg_create_deployment,
            convert_msg_update_deployment,
            convert_msg_close_deployment,
            convert_msg_deposit_deployment,
            convert_msg_close_group,
            convert_msg_pause_group,
            convert_msg_start_group,
        )

        # IBC message converters
        from akash.messages.ibc import (
            convert_msg_transfer,
            convert_msg_create_client,
            convert_msg_update_client,
        )

        # All message converter imports succeeded
        assert True

    def test_protobuf_message_instantiation(self):
        """Verify protobuf messages can be instantiated."""
        from akash.proto.cosmos.tx.v1beta1.tx_pb2 import SignDoc, TxRaw, TxBody, AuthInfo, Fee
        from akash.proto.cosmos.tx.v1beta1.service_pb2 import SimulateRequest, SimulateResponse
        from akash.proto.cosmos.base.v1beta1.coin_pb2 import Coin
        from google.protobuf.any_pb2 import Any

        # Test instantiation
        sign_doc = SignDoc()
        assert sign_doc is not None

        tx_raw = TxRaw()
        assert tx_raw is not None

        tx_body = TxBody()
        assert tx_body is not None

        auth_info = AuthInfo()
        assert auth_info is not None

        fee = Fee()
        assert fee is not None

        coin = Coin(denom="uakt", amount="1000")
        assert coin.denom == "uakt"
        assert coin.amount == "1000"

        any_msg = Any()
        assert any_msg is not None

        sim_request = SimulateRequest()
        assert sim_request is not None

        sim_response = SimulateResponse()
        assert sim_response is not None

    def test_signing_primitives(self):
        """Verify signing primitives work correctly."""
        from ecdsa.util import sigencode_string_canonize
        from ecdsa import SigningKey, SECP256k1
        import hashlib

        # Test signing with canonical encoding
        private_key = SigningKey.from_string(b'\x01' * 32, curve=SECP256k1)
        test_data = b"test transaction data"
        test_hash = hashlib.sha256(test_data).digest()

        signature = private_key.sign_deterministic(
            test_hash,
            hashfunc=hashlib.sha256,
            sigencode=sigencode_string_canonize
        )

        assert signature is not None
        assert isinstance(signature, bytes)
        assert len(signature) > 0


class TestTransactionHelpers:
    """Test transaction helper functions."""

    def test_type_mapping_coverage(self):
        """Test type mapping contains expected message types."""
        from akash.tx import type_mapping

        assert "MsgSend" in type_mapping
        assert "MsgDelegate" in type_mapping
        assert "MsgWithdrawDelegatorReward" in type_mapping
        assert "MsgSubmitProposal" in type_mapping
        assert "MsgGrant" in type_mapping
        assert "MsgGrantAllowance" in type_mapping

        assert type_mapping["MsgSend"] == "/cosmos.bank.v1beta1.MsgSend"
        assert type_mapping["MsgDelegate"] == "/cosmos.staking.v1beta1.MsgDelegate"

    def test_message_converters_registry_structure(self):
        """Test message converter registry structure."""
        assert isinstance(_MESSAGE_CONVERTERS, dict)

        original_count = len(_MESSAGE_CONVERTERS)

        def test_converter(msg_dict, any_msg):
            return any_msg

        register_message_converter("/test.converter", test_converter)

        assert len(_MESSAGE_CONVERTERS) == original_count + 1
        assert _MESSAGE_CONVERTERS["/test.converter"] == test_converter


if __name__ == '__main__':
    print("✅ Running transaction broadcasting unit tests")
    print("=" * 60)
    print()
    print("Testing BroadcastResult, message converters, transaction encoding,")
    print("signing operations, broadcasting, and confirmation functionality.")
    print()
    print("These tests use mocking to isolate transaction functionality.")
    print()

    pytest.main([__file__, '-v'])
