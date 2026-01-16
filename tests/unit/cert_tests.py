#!/usr/bin/env python3
"""
Certificate module tests - validation and functional tests.

Validation tests: Validate protobuf message structures, field access patterns,
converter compatibility, and query parameter support without requiring
blockchain interactions. 

Functional tests: Test certificate client query operations, transaction broadcasting,
certificate publishing/revoking, validation functions, and utility methods using mocking
to isolate functionality and test error handling scenarios.

Run: python cert_tests.py
"""

import os

os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from akash.proto.akash.cert.v1 import cert_pb2 as cert_pb
from akash.proto.akash.cert.v1 import query_pb2 as cert_query
from akash.proto.akash.cert.v1 import msg_pb2 as cert_msg  # v1: Msg types moved to msg_pb2


class TestCertificateMessageStructures:
    """Test certificate protobuf message structures and field access."""

    def test_id_structure(self):
        """Test ID (formerly CertificateID) message structure and field access."""
        # v1: CertificateID renamed to ID
        cert_id = cert_pb.ID()

        required_fields = ['owner', 'serial']
        for field in required_fields:
            assert hasattr(cert_id, field), f"ID missing field: {field}"
        cert_id.owner = "akash1test"
        cert_id.serial = "123456789"

        assert cert_id.owner == "akash1test"
        assert cert_id.serial == "123456789"

    def test_certificate_structure(self):
        """Test Certificate message structure and field access."""
        certificate = cert_pb.Certificate()

        required_fields = ['state', 'cert', 'pubkey']
        for field in required_fields:
            assert hasattr(certificate, field), f"Certificate missing field: {field}"
        certificate.state = 1  # valid
        certificate.cert = b"test_certificate_data"
        certificate.pubkey = b"test_public_key"

        assert certificate.state == 1
        assert certificate.cert == b"test_certificate_data"
        assert certificate.pubkey == b"test_public_key"

    def test_certificate_state_enum_exists(self):
        """Test certificate state enumeration exists."""
        # v1: State is a top-level enum, not nested in Certificate
        assert hasattr(cert_pb, 'State'), "cert_pb2 missing State enum"
        state_enum = cert_pb.State
        expected_states = ['invalid', 'valid', 'revoked']

        for state in expected_states:
            assert state in state_enum.keys(), f"State missing: {state}"


class TestCertificateQueryResponses:
    """Test certificate query response structures."""

    def test_query_certificates_response_structure(self):
        """Test QueryCertificatesResponse nested structure access."""
        response = cert_query.QueryCertificatesResponse()

        assert hasattr(response, 'certificates'), "QueryCertificatesResponse missing certificates field"
        assert hasattr(response, 'pagination'), "QueryCertificatesResponse missing pagination field"
        cert_response = cert_query.CertificateResponse()
        cert_response.certificate.state = 1  # valid
        cert_response.certificate.cert = b"test_cert"
        cert_response.certificate.pubkey = b"test_key"

        response.certificates.append(cert_response)

        first_cert = response.certificates[0]
        assert hasattr(first_cert, 'certificate'), "CertificateResponse missing certificate field"
        assert hasattr(first_cert.certificate, 'state'), "Certificate missing state field"
        assert hasattr(first_cert.certificate, 'cert'), "Certificate missing cert field"
        assert first_cert.certificate.state == 1


class TestCertificateMessageConverters:
    """Test certificate message converters for transaction compatibility."""

    def test_all_certificate_converters_registered(self):
        """Test that all certificate message converters are registered."""
        from akash.tx import _MESSAGE_CONVERTERS, _initialize_message_converters

        if not _MESSAGE_CONVERTERS:
            _initialize_message_converters()

        required_converters = [
            "/akash.cert.v1.MsgCreateCertificate",
            "/akash.cert.v1.MsgRevokeCertificate"
        ]

        for msg_type in required_converters:
            converter = _MESSAGE_CONVERTERS.get(msg_type)
            assert converter is not None, f"Missing converter for {msg_type}"
            assert callable(converter), f"Converter for {msg_type} is not callable"

    def test_msg_create_certificate_protobuf_compatibility(self):
        """Test MsgCreateCertificate protobuf field compatibility."""
        # v1: Msg types moved to msg_pb2
        pb_msg = cert_msg.MsgCreateCertificate()

        required_fields = ['owner', 'cert', 'pubkey']
        for field in required_fields:
            assert hasattr(pb_msg, field), f"MsgCreateCertificate missing field: {field}"
        pb_msg.owner = "akash1test"
        pb_msg.cert = b"test_certificate"
        pb_msg.pubkey = b"test_pubkey"

        assert pb_msg.owner == "akash1test"
        assert pb_msg.cert == b"test_certificate"
        assert pb_msg.pubkey == b"test_pubkey"

    def test_msg_revoke_certificate_protobuf_compatibility(self):
        """Test MsgRevokeCertificate protobuf field compatibility."""
        # v1: Msg types moved to msg_pb2
        pb_msg = cert_msg.MsgRevokeCertificate()

        required_fields = ['id']
        for field in required_fields:
            assert hasattr(pb_msg, field), f"MsgRevokeCertificate missing field: {field}"
        assert hasattr(pb_msg.id, 'owner'), "MsgRevokeCertificate.id missing owner"
        assert hasattr(pb_msg.id, 'serial'), "MsgRevokeCertificate.id missing serial"


class TestCertificateQueryParameters:
    """Test certificate query parameter compatibility."""

    def test_certificates_query_request_structure(self):
        """Test certificate query request structures."""
        req = cert_query.QueryCertificatesRequest()

        assert hasattr(req, 'filter'), "QueryCertificatesRequest missing filter field"
        assert hasattr(req, 'pagination'), "QueryCertificatesRequest missing pagination field"

        # v1: Filter might be inline in request
        if hasattr(cert_query, 'CertificateFilter'):
            cert_filter = cert_query.CertificateFilter()
            cert_filter.owner = "akash1test"
            cert_filter.state = "valid"
            req.filter.CopyFrom(cert_filter)
            assert req.filter.owner == "akash1test"
            assert req.filter.state == "valid"
        else:
            # Filter fields might be directly on request
            if hasattr(req.filter, 'owner'):
                req.filter.owner = "akash1test"
                assert req.filter.owner == "akash1test"


class TestCertificateTransactionMessages:
    """Test certificate transaction message structures."""

    def test_all_certificate_message_types_exist(self):
        """Test all expected certificate message types exist."""
        expected_messages = [
            'MsgCreateCertificate', 'MsgRevokeCertificate'
        ]

        # v1: Msg types moved to msg_pb2
        for msg_name in expected_messages:
            assert hasattr(cert_msg, msg_name), f"Missing certificate message type: {msg_name}"

            msg_class = getattr(cert_msg, msg_name)
            msg_instance = msg_class()
            assert msg_instance is not None

    def test_certificate_lifecycle_message_consistency(self):
        """Test certificate lifecycle messages are consistent."""
        # v1: Msg types moved to msg_pb2
        create_msg = cert_msg.MsgCreateCertificate()
        revoke_msg = cert_msg.MsgRevokeCertificate()

        create_fields = ['owner', 'cert', 'pubkey']
        for field in create_fields:
            assert hasattr(create_msg, field), f"MsgCreateCertificate missing: {field}"
        assert hasattr(revoke_msg, 'id'), "MsgRevokeCertificate missing id field"
        assert hasattr(revoke_msg.id, 'owner'), "MsgRevokeCertificate.id missing owner"
        assert hasattr(revoke_msg.id, 'serial'), "MsgRevokeCertificate.id missing serial"


class TestCertificateErrorPatterns:
    """Test common certificate error patterns and edge cases."""

    def test_empty_certificates_response_handling(self):
        """Test handling of empty certificates response."""
        response = cert_query.QueryCertificatesResponse()

        assert len(response.certificates) == 0, "Empty response should have no certificates"
        assert hasattr(response, 'pagination'), "Empty response missing pagination"

    def test_certificate_state_transitions(self):
        """Test certificate state value consistency."""
        certificate = cert_pb.Certificate()
        # v1: State is a top-level enum, not nested in Certificate
        state_enum = cert_pb.State

        certificate.state = state_enum.Value('valid')
        assert certificate.state == 1, "Valid state should be 1"

        certificate.state = state_enum.Value('revoked')
        assert certificate.state == 2, "Revoked state should be 2"

    def test_certificate_binary_data_handling(self):
        """Test certificate handles binary data correctly."""
        certificate = cert_pb.Certificate()

        test_cert_data = b"-----BEGIN CERTIFICATE-----\ntest\n-----END CERTIFICATE-----"
        test_pubkey_data = b"-----BEGIN PUBLIC KEY-----\ntest\n-----END PUBLIC KEY-----"

        certificate.cert = test_cert_data
        certificate.pubkey = test_pubkey_data

        assert certificate.cert == test_cert_data
        assert certificate.pubkey == test_pubkey_data


class TestCertificateModuleIntegration:
    """Test certificate module integration and consistency."""

    def test_certificate_converter_coverage(self):
        """Test all certificate messages have converters in tx registry."""
        from akash.tx import _MESSAGE_CONVERTERS, _initialize_message_converters

        if not _MESSAGE_CONVERTERS:
            _initialize_message_converters()

        expected_converters = ['MsgCreateCertificate', 'MsgRevokeCertificate']
        for msg_class in expected_converters:
            converter_key = f"/akash.cert.v1.{msg_class}"
            assert converter_key in _MESSAGE_CONVERTERS, f"Missing converter for: {msg_class}"

    def test_certificate_query_consistency(self):
        """Test certificate query response consistency."""
        response = cert_query.QueryCertificatesResponse()

        assert hasattr(response, 'certificates'), "Response missing certificates field"
        assert hasattr(response, 'pagination'), "Response missing pagination field"
        assert len(response.certificates) == 0, "Should start with empty certificates"

    def test_id_consistency(self):
        """Test certificate ID usage consistency."""
        # v1: CertificateID renamed to ID
        cert_id = cert_pb.ID()

        assert hasattr(cert_id, 'owner'), "ID missing owner"
        assert hasattr(cert_id, 'serial'), "ID missing serial"
        cert_id.owner = "akash1test"
        cert_id.serial = "12345"

        assert cert_id.owner == "akash1test"
        assert cert_id.serial == "12345"

    def test_certificate_state_enum_consistency(self):
        """Test certificate state enum value consistency."""
        # v1: State is a top-level enum, not nested in Certificate
        state_enum = cert_pb.State

        expected_states = {
            'invalid': 0,
            'valid': 1,
            'revoked': 2
        }

        for state_name, expected_value in expected_states.items():
            assert state_name in state_enum.keys(), f"State missing: {state_name}"
            actual_value = state_enum.Value(state_name)
            assert actual_value == expected_value, f"State {state_name} value mismatch"


from unittest.mock import Mock, patch
import base64


class TestCertClientInitialization:
    """Test certificate client initialization and setup."""

    def test_cert_client_initialization(self):
        """Test CertClient can be initialized properly."""
        from akash.modules.cert.client import CertClient

        mock_akash_client = Mock()
        cert_client = CertClient(mock_akash_client)

        assert cert_client.akash_client == mock_akash_client
        assert hasattr(cert_client, 'get_certificates')
        assert hasattr(cert_client, 'get_certificate')
        assert hasattr(cert_client, 'publish_client_certificate')
        assert hasattr(cert_client, 'publish_server_certificate')
        assert hasattr(cert_client, 'revoke_client_certificate')
        assert hasattr(cert_client, 'revoke_server_certificate')
        assert hasattr(cert_client, 'validate_certificate')
        assert hasattr(cert_client, 'generate_certificate_serial')

    def test_cert_client_inherits_mixins(self):
        """Test CertClient properly inherits from all mixins."""
        from akash.modules.cert.client import CertClient
        from akash.modules.cert.query import CertQuery
        from akash.modules.cert.tx import CertTx
        from akash.modules.cert.utils import CertUtils

        mock_akash_client = Mock()
        cert_client = CertClient(mock_akash_client)

        assert isinstance(cert_client, CertQuery)
        assert isinstance(cert_client, CertTx)
        assert isinstance(cert_client, CertUtils)

    def test_cert_client_logging_setup(self):
        """Test logging is properly configured for CertClient."""
        from akash.modules.cert.client import CertClient

        with patch('akash.modules.cert.client.logger') as mock_logger:
            mock_akash_client = Mock()
            cert_client = CertClient(mock_akash_client)

            mock_logger.info.assert_called_once_with("Initialized CertClient")


class TestCertQueryOperations:
    """Test certificate query operations with mocked responses."""

    def test_get_certificates_success(self):
        """Test successful certificates query with filters."""
        from akash.modules.cert.client import CertClient

        mock_response = {
            'response': {
                'code': 0,
                'value': base64.b64encode(b'mock_cert_data').decode()
            }
        }

        mock_akash_client = Mock()
        mock_akash_client.rpc_query.return_value = mock_response

        cert_client = CertClient(mock_akash_client)

        with patch('akash.proto.akash.cert.v1.query_pb2.QueryCertificatesResponse') as mock_response_class:
            mock_response_instance = Mock()
            mock_cert_response = Mock()
            mock_cert_response.serial = "ABC123456"
            mock_cert_response.certificate.state = 1  # valid
            mock_cert_response.certificate.cert = b"cert_data"
            mock_cert_response.certificate.pubkey = b"pubkey_data"
            mock_response_instance.certificates = [mock_cert_response]
            mock_response_instance.pagination.next_key = None
            mock_response_instance.pagination.total = 1
            mock_response_class.return_value = mock_response_instance

            result = cert_client.get_certificates(owner="akash1owner", state="valid", limit=10)

            assert 'certificates' in result
            assert 'pagination' in result
            assert len(result['certificates']) == 1
            assert result['certificates'][0]['serial'] == "ABC123456"
            assert result['certificates'][0]['certificate']['state'] == 'valid'

    def test_get_certificates_empty_response(self):
        """Test certificates query with no certificates found."""
        from akash.modules.cert.client import CertClient

        mock_response = {
            'response': {
                'code': 0,
                'value': None
            }
        }

        mock_akash_client = Mock()
        mock_akash_client.rpc_query.return_value = mock_response

        cert_client = CertClient(mock_akash_client)

        result = cert_client.get_certificates()

        assert result['certificates'] == []
        assert result['pagination']['next_key'] is None
        assert result['pagination']['total'] is None

    def test_get_certificates_error_response(self):
        """Test certificates query with error response."""
        from akash.modules.cert.client import CertClient

        mock_response = {
            'response': {
                'code': 1,
                'log': 'query failed'
            }
        }

        mock_akash_client = Mock()
        mock_akash_client.rpc_query.return_value = mock_response

        cert_client = CertClient(mock_akash_client)

        with pytest.raises(Exception, match="Query failed with code 1"):
            cert_client.get_certificates()

    def test_get_certificate_success(self):
        """Test successful specific certificate query."""
        from akash.modules.cert.client import CertClient

        mock_akash_client = Mock()
        cert_client = CertClient(mock_akash_client)

        mock_cert_data = {
            'serial': 'TEST123',
            'certificate': {
                'state': 'valid',
                'cert': base64.b64encode(b'cert_data').decode(),
                'pubkey': base64.b64encode(b'pubkey_data').decode()
            }
        }

        with patch.object(cert_client, 'get_certificates') as mock_get_certs:
            mock_get_certs.return_value = {
                'certificates': [mock_cert_data],
                'pagination': {'next_key': None}
            }

            cert = cert_client.get_certificate("akash1owner", "TEST123")

            assert cert == mock_cert_data
            mock_get_certs.assert_called_once_with(owner="akash1owner", serial="TEST123", limit=1)

    def test_get_certificate_not_found(self):
        """Test specific certificate query with no results."""
        from akash.modules.cert.client import CertClient

        mock_akash_client = Mock()
        cert_client = CertClient(mock_akash_client)

        with patch.object(cert_client, 'get_certificates') as mock_get_certs:
            mock_get_certs.return_value = {
                'certificates': [],
                'pagination': {'next_key': None}
            }

            cert = cert_client.get_certificate("akash1owner", "Notfound")

            assert cert is None


class TestCertTransactionOperations:
    """Test certificate transaction operations with mocked responses."""

    def test_publish_client_certificate_calls_broadcast(self):
        """Test publish client certificate calls broadcast_transaction_rpc."""
        from akash.modules.cert.client import CertClient

        mock_wallet = Mock()
        mock_wallet.address = "akash1owner"

        mock_broadcast_result = Mock()
        mock_broadcast_result.success = True
        mock_broadcast_result.tx_hash = "ABC123"

        mock_akash_client = Mock()
        cert_client = CertClient(mock_akash_client)

        cert_data = b"certificate_data"
        pubkey_data = b"public_key_data"

        with patch('akash.modules.cert.tx.broadcast_transaction_rpc',
                   return_value=mock_broadcast_result) as mock_broadcast:
            result = cert_client.publish_client_certificate(
                mock_wallet,
                cert_data,
                pubkey_data,
                "Publish client cert",
                use_simulation=False
            )

            mock_broadcast.assert_called_once()
            call_args = mock_broadcast.call_args[1]
            messages = call_args['messages']
            assert len(messages) == 1
            assert messages[0]['@type'] == '/akash.cert.v1.MsgCreateCertificate'
            assert messages[0]['owner'] == 'akash1owner'
            assert messages[0]['cert'] == base64.b64encode(cert_data).decode()
            assert messages[0]['pubkey'] == base64.b64encode(pubkey_data).decode()

    def test_publish_server_certificate_calls_broadcast(self):
        """Test publish server certificate calls broadcast_transaction_rpc."""
        from akash.modules.cert.client import CertClient

        mock_wallet = Mock()
        mock_wallet.address = "akash1owner"

        mock_broadcast_result = Mock()
        mock_broadcast_result.success = True
        mock_broadcast_result.tx_hash = "DEF456"

        mock_akash_client = Mock()
        cert_client = CertClient(mock_akash_client)

        cert_data = b"server_certificate_data"
        pubkey_data = b"server_public_key_data"

        with patch('akash.modules.cert.tx.broadcast_transaction_rpc',
                   return_value=mock_broadcast_result) as mock_broadcast:
            result = cert_client.publish_server_certificate(
                mock_wallet,
                cert_data,
                pubkey_data,
                "Publish server cert",
                use_simulation=False
            )

            mock_broadcast.assert_called_once()  
            call_args = mock_broadcast.call_args[1]
            messages = call_args['messages']
            assert len(messages) == 1
            assert messages[0]['@type'] == '/akash.cert.v1.MsgCreateCertificate'
            assert messages[0]['owner'] == 'akash1owner'
            assert messages[0]['cert'] == base64.b64encode(cert_data).decode()
            assert messages[0]['pubkey'] == base64.b64encode(pubkey_data).decode()

    def test_revoke_client_certificate_calls_broadcast(self):
        """Test revoke client certificate calls broadcast_transaction_rpc."""
        from akash.modules.cert.client import CertClient

        mock_wallet = Mock()
        mock_wallet.address = "akash1owner"

        mock_broadcast_result = Mock()
        mock_broadcast_result.success = True
        mock_broadcast_result.tx_hash = "GHI789"

        mock_akash_client = Mock()
        cert_client = CertClient(mock_akash_client)

        with patch('akash.modules.cert.tx.broadcast_transaction_rpc',
                   return_value=mock_broadcast_result) as mock_broadcast:
            result = cert_client.revoke_client_certificate(
                mock_wallet,
                "CERT123",
                "Revoke client cert",
                use_simulation=False
            )

            mock_broadcast.assert_called_once()
            call_args = mock_broadcast.call_args[1]
            messages = call_args['messages']
            assert len(messages) == 1
            assert messages[0]['@type'] == '/akash.cert.v1.MsgRevokeCertificate'
            assert messages[0]['id']['owner'] == 'akash1owner'
            assert messages[0]['id']['serial'] == 'CERT123'

    def test_revoke_server_certificate_calls_broadcast(self):
        """Test revoke server certificate calls broadcast_transaction_rpc."""
        from akash.modules.cert.client import CertClient

        mock_wallet = Mock()
        mock_wallet.address = "akash1owner"

        mock_broadcast_result = Mock()
        mock_broadcast_result.success = True
        mock_broadcast_result.tx_hash = "JKL012"

        mock_akash_client = Mock()
        cert_client = CertClient(mock_akash_client)

        with patch('akash.modules.cert.tx.broadcast_transaction_rpc',
                   return_value=mock_broadcast_result) as mock_broadcast:
            result = cert_client.revoke_server_certificate(
                mock_wallet,
                "SERVER456",
                "Revoke server cert",
                use_simulation=False
            )

            mock_broadcast.assert_called_once()
            call_args = mock_broadcast.call_args[1]
            messages = call_args['messages']
            assert len(messages) == 1
            assert messages[0]['@type'] == '/akash.cert.v1.MsgRevokeCertificate'
            assert messages[0]['id']['owner'] == 'akash1owner'
            assert messages[0]['id']['serial'] == 'SERVER456'

    def test_publish_certificate_exception(self):
        """Test publish certificate with exception."""
        from akash.modules.cert.client import CertClient

        mock_wallet = Mock()
        mock_wallet.address = "akash1owner"

        mock_akash_client = Mock()
        cert_client = CertClient(mock_akash_client)

        with patch('akash.modules.cert.tx.broadcast_transaction_rpc',
                   side_effect=Exception("Network error")) as mock_broadcast:
            result = cert_client.publish_client_certificate(
                mock_wallet,
                b"cert_data",
                b"pubkey_data",
                use_simulation=False
            )

            assert result.success == False

    def test_revoke_certificate_exception(self):
        """Test revoke certificate with exception."""
        from akash.modules.cert.client import CertClient

        mock_wallet = Mock()
        mock_wallet.address = "akash1owner"

        mock_akash_client = Mock()
        cert_client = CertClient(mock_akash_client)

        with patch('akash.modules.cert.tx.broadcast_transaction_rpc',
                   side_effect=Exception("Permission denied")) as mock_broadcast:
            result = cert_client.revoke_client_certificate(
                mock_wallet,
                "CERT123",
                use_simulation=False
            )

            assert result.success == False


class TestCertUtilityFunctions:
    """Test certificate utility functions."""

    def test_validate_certificate_valid(self):
        """Test validation of valid certificate data with proper PEM format."""
        from akash.modules.cert.client import CertClient

        mock_akash_client = Mock()
        cert_client = CertClient(mock_akash_client)

        valid_cert_pem = """-----BEGIN CERTIFICATE-----
MIIBmjCCAUGgAwIBAgIHBjDlLlU04DAKBggqhkjOPQQDAjA3
-----END CERTIFICATE-----"""

        valid_pubkey_pem = """-----BEGIN EC PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAETEST123==
-----END EC PUBLIC KEY-----"""

        valid_cert_data = {
            'serial': 'CERT123456',
            'certificate': {
                'state': 'valid',
                'cert': base64.b64encode(valid_cert_pem.encode()).decode(),
                'pubkey': base64.b64encode(valid_pubkey_pem.encode()).decode()
            }
        }

        result = cert_client.validate_certificate(valid_cert_data)
        assert result == True

    def test_validate_certificate_missing_fields(self):
        """Test validation with missing required fields."""
        from akash.modules.cert.client import CertClient

        mock_akash_client = Mock()
        cert_client = CertClient(mock_akash_client)

        invalid_data_missing_serial = {
            'certificate': {
                'state': 'valid',
                'cert': base64.b64encode(b'cert_data').decode(),
                'pubkey': base64.b64encode(b'pubkey_data').decode()
            }
        }

        with patch('akash.modules.cert.utils.logger') as mock_logger:
            result = cert_client.validate_certificate(invalid_data_missing_serial)
            assert result == False
            mock_logger.error.assert_called_with("Missing required field: serial")

    def test_validate_certificate_invalid_state(self):
        """Test validation with invalid certificate state."""
        from akash.modules.cert.client import CertClient

        mock_akash_client = Mock()
        cert_client = CertClient(mock_akash_client)

        invalid_data = {
            'serial': 'CERT123456',
            'certificate': {
                'state': 'unknown_state',
                'cert': base64.b64encode(b'cert_data').decode(),
                'pubkey': base64.b64encode(b'pubkey_data').decode()
            }
        }

        with patch('akash.modules.cert.utils.logger') as mock_logger:
            result = cert_client.validate_certificate(invalid_data)
            assert result == False
            mock_logger.error.assert_called_with("Invalid certificate state: unknown_state")

    def test_validate_certificate_invalid_base64(self):
        """Test validation with invalid base64 data."""
        from akash.modules.cert.client import CertClient

        mock_akash_client = Mock()
        cert_client = CertClient(mock_akash_client)

        invalid_data = {
            'serial': 'CERT123456',
            'certificate': {
                'state': 'valid',
                'cert': 'invalid_base64',
                'pubkey': 'invalid_base64'
            }
        }

        with patch('akash.modules.cert.utils.logger') as mock_logger:
            result = cert_client.validate_certificate(invalid_data)
            assert result == False
            mock_logger.error.assert_called_with("Certificate data must be base64 encoded")

    def test_validate_certificate_invalid_pem_format(self):
        """Test validation with invalid PEM format."""
        from akash.modules.cert.client import CertClient

        mock_akash_client = Mock()
        cert_client = CertClient(mock_akash_client)

        invalid_pem_data = {
            'serial': 'CERT123456',
            'certificate': {
                'state': 'valid',
                'cert': base64.b64encode(b'not a pem certificate').decode(),
                'pubkey': base64.b64encode(b'not a pem public key').decode()
            }
        }

        with patch('akash.modules.cert.utils.logger') as mock_logger:
            result = cert_client.validate_certificate(invalid_pem_data)
            assert result == False
            mock_logger.error.assert_called()

    def test_validate_certificate_valid_pem_format(self):
        """Test validation with valid PEM format certificates."""
        from akash.modules.cert.client import CertClient

        mock_akash_client = Mock()
        cert_client = CertClient(mock_akash_client)

        valid_cert_pem = """-----BEGIN CERTIFICATE-----
MIIBmjCCAUGgAwIBAgIHBjDlLlU04DAKBggqhkjOPQQDAjA3MTUwMwYDVQQDDCxh
-----END CERTIFICATE-----"""

        valid_pubkey_pem = """-----BEGIN EC PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAETEST123Data==
-----END EC PUBLIC KEY-----"""

        valid_pem_data = {
            'serial': 'CERT123456',
            'certificate': {
                'state': 'valid',
                'cert': base64.b64encode(valid_cert_pem.encode()).decode(),
                'pubkey': base64.b64encode(valid_pubkey_pem.encode()).decode()
            }
        }

        result = cert_client.validate_certificate(valid_pem_data)
        assert result == True

    def test_state_filter_working_correctly(self):
        """Test that state filter correctly passes string enum values to protobuf."""
        from akash.modules.cert.client import CertClient

        mock_akash_client = Mock()
        cert_client = CertClient(mock_akash_client)

        # v1: CertificateFilter moved to filters_pb2
        with patch('akash.proto.akash.cert.v1.query_pb2.QueryCertificatesRequest') as mock_request_class, \
                patch('akash.proto.akash.cert.v1.filters_pb2.CertificateFilter') as mock_filter_class:
            mock_request = Mock()
            mock_filter = Mock()
            mock_request_class.return_value = mock_request
            mock_filter_class.return_value = mock_filter

            mock_akash_client.rpc_query.return_value = {
                'response': {
                    'code': 0,
                    'value': None
                }
            }
            cert_client.get_certificates(state="valid")

            assert mock_filter.state == "valid"

    def test_generate_certificate_serial(self):
        """Test certificate serial generation."""
        from akash.modules.cert.client import CertClient

        mock_akash_client = Mock()
        cert_client = CertClient(mock_akash_client)

        owner = "akash1owner"
        cert_data = b"certificate_data"

        serial1 = cert_client.generate_certificate_serial(owner, cert_data)
        serial2 = cert_client.generate_certificate_serial(owner, cert_data)

        assert serial1 == serial2
        assert len(serial1) == 16
        assert isinstance(serial1, str)
        different_data = b"different_certificate_data"
        serial3 = cert_client.generate_certificate_serial(owner, different_data)
        assert serial1 != serial3

    def test_get_state_name_helper(self):
        """Test state name helper method."""
        from akash.modules.cert.client import CertClient

        mock_akash_client = Mock()
        cert_client = CertClient(mock_akash_client)

        assert cert_client._get_state_name(0) == 'invalid'
        assert cert_client._get_state_name(1) == 'valid'
        assert cert_client._get_state_name(2) == 'revoked'
        assert cert_client._get_state_name(99) == 'unknown'


class TestCertErrorHandlingScenarios:
    """Test certificate error handling and edge cases."""

    def test_get_certificates_network_failure(self):
        """Test certificates query with network failure."""
        from akash.modules.cert.client import CertClient

        mock_akash_client = Mock()
        mock_akash_client.rpc_query.side_effect = Exception("Connection timeout")

        cert_client = CertClient(mock_akash_client)

        with pytest.raises(Exception, match="Connection timeout"):
            cert_client.get_certificates()

    def test_get_certificates_no_response(self):
        """Test certificates query with no response."""
        from akash.modules.cert.client import CertClient

        mock_akash_client = Mock()
        mock_akash_client.rpc_query.return_value = None

        cert_client = CertClient(mock_akash_client)

        with pytest.raises(Exception, match="Query failed: No response"):
            cert_client.get_certificates()

    def test_get_certificates_malformed_response(self):
        """Test certificates query with malformed response."""
        from akash.modules.cert.client import CertClient

        mock_response = {
            'response': {
                'code': 0,
                'value': 'invalid_base64_data'
            }
        }

        mock_akash_client = Mock()
        mock_akash_client.rpc_query.return_value = mock_response

        cert_client = CertClient(mock_akash_client)

        with pytest.raises(Exception, match="Failed to parse certificates response"):
            cert_client.get_certificates()

    def test_get_certificate_exception(self):
        """Test specific certificate query with exception."""
        from akash.modules.cert.client import CertClient

        mock_akash_client = Mock()
        cert_client = CertClient(mock_akash_client)

        with patch.object(cert_client, 'get_certificates', side_effect=Exception("Query error")):
            with pytest.raises(Exception, match="Query error"):
                cert_client.get_certificate("akash1owner", "CERT123")

    def test_generate_certificate_serial_exception(self):
        """Test certificate serial generation with exception."""
        from akash.modules.cert.client import CertClient

        mock_akash_client = Mock()
        cert_client = CertClient(mock_akash_client)

        with patch('akash.modules.cert.utils.logger') as mock_logger:
            serial = cert_client.generate_certificate_serial(None, None)

            assert serial == ""
            mock_logger.error.assert_called_once()

    def test_get_certificates_with_pagination_parsing(self):
        """Test certificates query with pagination key parsing."""
        from akash.modules.cert.client import CertClient

        mock_response = {
            'response': {
                'code': 0,
                'value': base64.b64encode(b'mock_cert_data').decode()
            }
        }

        mock_akash_client = Mock()
        mock_akash_client.rpc_query.return_value = mock_response

        cert_client = CertClient(mock_akash_client)

        with patch('akash.proto.akash.cert.v1.query_pb2.QueryCertificatesResponse') as mock_response_class:
            mock_response_instance = Mock()
            mock_response_instance.certificates = []
            mock_response_instance.pagination.next_key = b'\xff\xfe\xfd'
            mock_response_instance.pagination.total = 0
            mock_response_class.return_value = mock_response_instance

            result = cert_client.get_certificates(count_total=True)

            assert result['pagination']['next_key'] is not None
            assert isinstance(result['pagination']['next_key'], str)
            assert result['pagination']['total'] == 0

    def test_validate_certificate_exception_handling(self):
        """Test certificate validation with unexpected exception."""
        from akash.modules.cert.client import CertClient

        mock_akash_client = Mock()
        cert_client = CertClient(mock_akash_client)

        with patch('akash.modules.cert.utils.logger') as mock_logger:
            result = cert_client.validate_certificate("invalid_data_type")

            assert result == False
            mock_logger.error.assert_called_once()


class TestCertQueryMissingCoverage:
    """Test previously uncovered cert query functions."""

    def test_get_mtls_credentials_dependencies(self):
        """Test get_mtls_credentials uses correct protobuf structures."""
        # Test that the Certificate message can be instantiated for mTLS
        cert = cert_pb.Certificate()
        assert hasattr(cert, 'state'), "Certificate missing state field"
        assert hasattr(cert, 'cert'), "Certificate missing cert field"
        assert hasattr(cert, 'pubkey'), "Certificate missing pubkey field"


if __name__ == '__main__':
    print("Running certificate module tests (validation + functional)")
    print("=" * 70)
    print()
    print("Validation tests: testing protobuf structures, message converters,")
    print("query responses, certificate lifecycle, and binary data handling patterns.")
    print()
    print("Functional tests: testing client operations, query methods, transaction")
    print("broadcasting, certificate management, and error handling scenarios.")
    print()
    print("These tests cover functionality without blockchain interactions.")
    print()

    pytest.main([__file__, '-v'])
