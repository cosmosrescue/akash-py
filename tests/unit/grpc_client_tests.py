#!/usr/bin/env python3
"""
gRPC Client Infrastructure tests - validation and functional tests.

Validation tests: Validate ProviderGRPCClient class structures, connection patterns,
stub management compatibility, and mTLS configuration support without requiring
blockchain interactions. 

Functional tests: Test gRPC client connection management, retry logic, mTLS authentication,
error handling, and secure provider communication using mocking to isolate functionality
and test error handling scenarios.

Run: python grpc_client_tests.py
"""

import os

os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

import pytest
import sys
from unittest.mock import Mock, patch
import grpc
import ssl
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from akash.grpc_client import ProviderGRPCClient

_original_sleep = time.sleep

def mock_sleep(duration):
    pass

time.sleep = mock_sleep

class TestProviderGRPCClientInitialization:
    """Test ProviderGRPCClient initialization and configuration."""

    def test_grpc_client_initialization_success(self):
        """Test successful gRPC client initialization."""
        mock_akash_client = Mock()

        client = ProviderGRPCClient(mock_akash_client)

        assert client.akash_client == mock_akash_client
        assert client.timeout == 30
        assert client.retries == 3
        assert client.logger is not None

    def test_grpc_client_initialization_custom_params(self):
        """Test gRPC client initialization with custom parameters."""
        mock_akash_client = Mock()

        client = ProviderGRPCClient(mock_akash_client, timeout=60, retries=5)

        assert client.timeout == 60
        assert client.retries == 5

    def test_grpc_client_initialization_logging(self):
        """Test gRPC client logging setup."""
        mock_akash_client = Mock()

        with patch('akash.grpc_client.logger') as mock_logger:
            client = ProviderGRPCClient(mock_akash_client)

            mock_logger.info.assert_called_with("Initialized ProviderGRPCClient with connection pooling")

class TestGRPCChannelManagement:
    """Test gRPC channel creation and management."""

    def test_create_secure_channel_with_mtls(self):
        """Test secure gRPC channel creation with mTLS."""
        mock_akash_client = Mock()
        client = ProviderGRPCClient(mock_akash_client)

        mock_credentials = Mock()
        mock_channel = Mock()
        mock_file_ca = Mock()
        mock_file_ca.__enter__ = Mock(return_value=Mock(read=Mock(return_value=b'ca_cert_data')))
        mock_file_ca.__exit__ = Mock(return_value=None)

        mock_file_cert = Mock()
        mock_file_cert.__enter__ = Mock(return_value=Mock(read=Mock(return_value=b'client_cert_data')))
        mock_file_cert.__exit__ = Mock(return_value=None)

        mock_file_key = Mock()
        mock_file_key.__enter__ = Mock(return_value=Mock(read=Mock(return_value=b'client_key_data')))
        mock_file_key.__exit__ = Mock(return_value=None)

        with patch('akash.grpc_client.grpc.ssl_channel_credentials', return_value=mock_credentials) as mock_creds, \
                patch('akash.grpc_client.grpc.secure_channel', return_value=mock_channel) as mock_secure_channel, \
                patch('builtins.open', side_effect=[mock_file_ca, mock_file_cert, mock_file_key]), \
                patch('os.path.exists', return_value=True):
            channel = client._create_secure_channel("provider.example.com:8443", "akash1owner", use_mtls=True)

            mock_creds.assert_called_once_with(
                root_certificates=b'ca_cert_data',
                private_key=b'client_key_data',
                certificate_chain=b'client_cert_data'
            )
            mock_secure_channel.assert_called_once_with("provider.example.com:8443", mock_credentials)

            assert channel == mock_channel

    def test_create_secure_channel_without_mtls(self):
        """Test secure gRPC channel creation without mTLS (server-side TLS only)."""
        mock_akash_client = Mock()
        client = ProviderGRPCClient(mock_akash_client)

        mock_credentials = Mock()
        mock_channel = Mock()
        mock_file_ca = Mock()
        mock_file_ca.__enter__ = Mock(return_value=Mock(read=Mock(return_value=b'ca_cert_data')))
        mock_file_ca.__exit__ = Mock(return_value=None)

        with patch('akash.grpc_client.grpc.ssl_channel_credentials', return_value=mock_credentials) as mock_creds, \
                patch('akash.grpc_client.grpc.secure_channel', return_value=mock_channel) as mock_secure_channel, \
                patch('builtins.open', return_value=mock_file_ca), \
                patch('os.path.exists', return_value=True):
            channel = client._create_secure_channel("provider.example.com:8443", "akash1owner", use_mtls=False)

            mock_creds.assert_called_once_with(
                root_certificates=b'ca_cert_data',
                private_key=None,
                certificate_chain=None
            )
            mock_secure_channel.assert_called_once_with("provider.example.com:8443", mock_credentials)

            assert channel == mock_channel

    def test_create_secure_channel_missing_certs(self):
        """Test secure channel creation with missing certificates."""
        mock_akash_client = Mock()
        client = ProviderGRPCClient(mock_akash_client)

        with patch('os.path.exists', return_value=False):
            with pytest.raises(Exception, match="mTLS requested but certificate files not found"):
                client._create_secure_channel("provider.example.com:8443", "akash1owner")

    def test_create_secure_channel_ssl_error(self):
        """Test secure channel creation with SSL configuration error."""
        mock_akash_client = Mock()
        client = ProviderGRPCClient(mock_akash_client)

        mock_file_ca = Mock()
        mock_file_ca.__enter__ = Mock(return_value=Mock(read=Mock(return_value=b'ca_cert_data')))
        mock_file_ca.__exit__ = Mock(return_value=None)

        with patch('os.path.exists', return_value=True), \
                patch('builtins.open', return_value=mock_file_ca), \
                patch('akash.grpc_client.grpc.ssl_channel_credentials', side_effect=ssl.SSLError("SSL error")):
            with pytest.raises(Exception, match="SSL error"):
                client._create_secure_channel("provider.example.com:8443", "akash1owner", use_mtls=False)

    def test_create_secure_channel_grpc_error(self):
        """Test secure channel creation with gRPC error."""
        mock_akash_client = Mock()
        client = ProviderGRPCClient(mock_akash_client)

        mock_file_ca = Mock()
        mock_file_ca.__enter__ = Mock(return_value=Mock(read=Mock(return_value=b'ca_cert_data')))
        mock_file_ca.__exit__ = Mock(return_value=None)

        with patch('os.path.exists', return_value=True), \
                patch('builtins.open', return_value=mock_file_ca), \
                patch('akash.grpc_client.grpc.ssl_channel_credentials'), \
                patch('akash.grpc_client.grpc.secure_channel', side_effect=grpc.RpcError("gRPC error")):
            with pytest.raises(Exception, match="Failed to create secure gRPC channel"):
                client._create_secure_channel("provider.example.com:8443", "akash1owner", use_mtls=False)

class TestGRPCStubManagement:
    """Test gRPC stub creation and caching."""

    def test_get_lease_stub_success(self):
        """Test successful lease stub creation."""
        mock_akash_client = Mock()
        client = ProviderGRPCClient(mock_akash_client)

        mock_channel = Mock()
        mock_stub = Mock()

        with patch.object(client, '_create_secure_channel', return_value=mock_channel), \
                patch('akash.grpc_client.LeaseRPCStub', return_value=mock_stub) as mock_stub_class:
            stub = client._get_lease_stub("provider.example.com:8443", "akash1owner")

            mock_stub_class.assert_called_once_with(mock_channel)
            assert stub == mock_stub

    def test_stub_creation_channel_error(self):
        """Test stub creation with channel creation error."""
        mock_akash_client = Mock()
        client = ProviderGRPCClient(mock_akash_client)

        with patch.object(client, '_create_secure_channel', side_effect=Exception("Channel error")):
            with pytest.raises(Exception, match="Channel error"):
                client._get_lease_stub("provider.example.com:8443", "akash1owner")

class TestGRPCRetryLogic:
    """Test gRPC retry logic and error handling."""

    def test_call_with_retry_success_first_attempt(self):
        """Test successful gRPC call on first attempt."""
        mock_akash_client = Mock()
        client = ProviderGRPCClient(mock_akash_client)

        mock_stub = Mock()
        mock_method = Mock(return_value="success_response")
        mock_stub.SendManifest = mock_method
        mock_request = Mock()

        def stub_factory(endpoint, owner, use_mtls, insecure):
            return mock_stub

        result = client.call_with_retry(stub_factory, "SendManifest", mock_request)

        assert result["status"] == "success"
        assert result["response"] == "success_response"
        mock_method.assert_called_once_with(mock_request, timeout=30)

    def test_call_with_retry_success_after_retries(self):
        """Test successful gRPC call after retries."""
        mock_akash_client = Mock()
        client = ProviderGRPCClient(mock_akash_client)

        mock_stub = Mock()
        error1 = grpc.RpcError("Temporary error")
        error1.code = Mock(return_value=grpc.StatusCode.UNAVAILABLE)
        error1.details = Mock(return_value="Temporary error")
        error2 = grpc.RpcError("Another error")
        error2.code = Mock(return_value=grpc.StatusCode.UNAVAILABLE)
        error2.details = Mock(return_value="Another error")

        mock_method = Mock(side_effect=[error1, error2, "success_response"])
        mock_stub.SendManifest = mock_method
        mock_request = Mock()

        def stub_factory(endpoint, owner, use_mtls, insecure):
            return mock_stub

        result = client.call_with_retry(stub_factory, "SendManifest", mock_request, retries=3)

        assert result["status"] == "success"
        assert result["response"] == "success_response"
        assert mock_method.call_count == 3

    def test_call_with_retry_exhausted_retries(self):
        """Test gRPC call with exhausted retries."""
        mock_akash_client = Mock()
        client = ProviderGRPCClient(mock_akash_client)

        mock_stub = Mock()

        def raise_persistent_error(*args, **kwargs):
            error = grpc.RpcError("Persistent error")
            error.code = Mock(return_value=grpc.StatusCode.UNAVAILABLE)
            error.details = Mock(return_value="Persistent error")
            raise error

        mock_method = Mock(side_effect=raise_persistent_error)
        mock_stub.SendManifest = mock_method
        mock_request = Mock()

        def stub_factory(endpoint, owner, use_mtls, insecure):
            return mock_stub

        result = client.call_with_retry(stub_factory, "SendManifest", mock_request, retries=2)

        assert result["status"] == "error"
        assert "UNAVAILABLE" in result["error"] or "Persistent error" in result["error"]
        assert mock_method.call_count == 3

    def test_call_with_retry_timeout_error(self):
        """Test gRPC call with timeout error."""
        mock_akash_client = Mock()
        client = ProviderGRPCClient(mock_akash_client)

        mock_stub = Mock()
        mock_method = Mock(side_effect=grpc.RpcError("DEADLINE_EXCEEDED"))
        mock_stub.SendManifest = mock_method
        mock_request = Mock()

        def stub_factory(endpoint, owner, use_mtls, insecure):
            return mock_stub

        result = client.call_with_retry(stub_factory, "SendManifest", mock_request, timeout=10)

        assert result["status"] == "error"
        assert "DEADLINE_EXCEEDED" in result["error"]
        mock_method.assert_called_with(mock_request, timeout=10)

    def test_call_with_retry_general_exception(self):
        """Test gRPC call with general exception."""
        mock_akash_client = Mock()
        client = ProviderGRPCClient(mock_akash_client)

        mock_stub = Mock()
        mock_method = Mock(side_effect=Exception("General error"))
        mock_stub.SendManifest = mock_method
        mock_request = Mock()

        def stub_factory(endpoint, owner, use_mtls, insecure):
            return mock_stub

        result = client.call_with_retry(stub_factory, "SendManifest", mock_request)

        assert result["status"] == "error"
        assert "General error" in result["error"]

    def test_call_with_retry_custom_timeout(self):
        """Test gRPC call with custom timeout."""
        mock_akash_client = Mock()
        client = ProviderGRPCClient(mock_akash_client)

        mock_stub = Mock()
        mock_method = Mock(return_value="success_response")
        mock_stub.SendManifest = mock_method
        mock_request = Mock()

        def stub_factory(endpoint, owner, use_mtls, insecure):
            return mock_stub

        result = client.call_with_retry(stub_factory, "SendManifest", mock_request, timeout=60)

        assert result["status"] == "success"
        mock_method.assert_called_once_with(mock_request, timeout=60)

class TestGRPCErrorHandling:
    """Test complete gRPC error handling."""

    def test_grpc_unavailable_error(self):
        """Test handling of Unavailable gRPC error."""
        mock_akash_client = Mock()
        client = ProviderGRPCClient(mock_akash_client)

        grpc_error = grpc.RpcError("Service unavailable")
        grpc_error.code = Mock(return_value=grpc.StatusCode.UNAVAILABLE)
        grpc_error.details = Mock(return_value="Service unavailable")

        mock_stub = Mock()
        mock_method = Mock(side_effect=grpc_error)
        mock_stub.SendManifest = mock_method
        mock_request = Mock()

        def stub_factory(endpoint, owner, use_mtls, insecure):
            return mock_stub

        result = client.call_with_retry(stub_factory, "SendManifest", mock_request, retries=1)

        assert result["status"] == "error"
        assert "UNAVAILABLE" in result["error"] or "Service unavailable" in result["error"]

    def test_grpc_unauthenticated_error(self):
        """Test handling of Unauthenticated gRPC error."""
        mock_akash_client = Mock()
        client = ProviderGRPCClient(mock_akash_client)

        grpc_error = grpc.RpcError("Authentication required")
        grpc_error.code = Mock(return_value=grpc.StatusCode.UNAUTHENTICATED)
        grpc_error.details = Mock(return_value="Authentication required")

        mock_stub = Mock()
        mock_method = Mock(side_effect=grpc_error)
        mock_stub.SendManifest = mock_method
        mock_request = Mock()

        def stub_factory(endpoint, owner, use_mtls, insecure):
            return mock_stub

        result = client.call_with_retry(stub_factory, "SendManifest", mock_request, retries=0)

        assert result["status"] == "error"
        assert "UNAUTHENTICATED" in result["error"] or "Authentication required" in result["error"]

    def test_grpc_deadline_exceeded_error(self):
        """Test handling of DEADLINE_EXCEEDED gRPC error."""
        mock_akash_client = Mock()
        client = ProviderGRPCClient(mock_akash_client)

        grpc_error = grpc.RpcError("Request timed out")
        grpc_error.code = Mock(return_value=grpc.StatusCode.DEADLINE_EXCEEDED)
        grpc_error.details = Mock(return_value="Request timed out")

        mock_stub = Mock()
        mock_method = Mock(side_effect=grpc_error)
        mock_stub.SendManifest = mock_method
        mock_request = Mock()

        def stub_factory(endpoint, owner, use_mtls, insecure):
            return mock_stub

        result = client.call_with_retry(stub_factory, "SendManifest", mock_request, retries=1)

        assert result["status"] == "error"
        assert "DEADLINE_EXCEEDED" in result["error"]
        assert "Request timed out" in result["error"]

    def test_grpc_unknown_error(self):
        """Test handling of unknown gRPC error."""
        mock_akash_client = Mock()
        client = ProviderGRPCClient(mock_akash_client)

        grpc_error = grpc.RpcError("Unknown error occurred")
        grpc_error.code = Mock(return_value=grpc.StatusCode.UNKNOWN)
        grpc_error.details = Mock(return_value="Unknown error occurred")

        mock_stub = Mock()
        mock_method = Mock(side_effect=grpc_error)
        mock_stub.SendManifest = mock_method
        mock_request = Mock()

        def stub_factory(endpoint, owner, use_mtls, insecure):
            return mock_stub

        result = client.call_with_retry(stub_factory, "SendManifest", mock_request, retries=1)

        assert result["status"] == "error"
        assert "UNKNOWN" in result["error"] or "Unknown error occurred" in result["error"]

    def test_non_grpc_error(self):
        """Test handling of non-gRPC exceptions."""
        mock_akash_client = Mock()
        client = ProviderGRPCClient(mock_akash_client)

        mock_stub = Mock()
        mock_method = Mock(side_effect=ValueError("Invalid value"))
        mock_stub.SendManifest = mock_method
        mock_request = Mock()

        def stub_factory(endpoint, owner, use_mtls, insecure):
            return mock_stub

        result = client.call_with_retry(stub_factory, "SendManifest", mock_request)

        assert result["status"] == "error"
        assert "Invalid value" in result["error"]

class TestGRPCConnectionManagement:
    """Test gRPC connection lifecycle management."""

    def test_connection_cleanup(self):
        """Test proper connection cleanup."""
        mock_akash_client = Mock()
        client = ProviderGRPCClient(mock_akash_client)

        mock_channel = Mock()
        client._channels = {"test_endpoint": mock_channel}

        client.cleanup_connections()

        mock_channel.close.assert_called_once()
        assert len(client._channels) == 0

    def test_connection_cleanup_with_error(self):
        """Test connection cleanup with channel close error."""
        mock_akash_client = Mock()
        client = ProviderGRPCClient(mock_akash_client)

        mock_channel = Mock()
        mock_channel.close.side_effect = Exception("Close error")
        client._channels = {"test_endpoint": mock_channel}

        with patch('akash.grpc_client.logger') as mock_logger:
            client.cleanup_connections()

            mock_logger.error.assert_called_once()
            assert len(client._channels) == 0

    def test_context_manager_usage(self):
        """Test gRPC client as context manager."""
        mock_akash_client = Mock()

        with patch.object(ProviderGRPCClient, 'cleanup_connections') as mock_cleanup:
            with ProviderGRPCClient(mock_akash_client) as client:
                assert isinstance(client, ProviderGRPCClient)

            mock_cleanup.assert_called_once()

class TestGRPCStubFactories:
    """Test gRPC stub factory methods."""

    def test_all_stub_factories_exist(self):
        """Test that all required stub factory methods exist."""
        mock_akash_client = Mock()
        client = ProviderGRPCClient(mock_akash_client)

        required_methods = [
            '_get_lease_stub'
        ]

        for method_name in required_methods:
            assert hasattr(client, method_name)
            assert callable(getattr(client, method_name))

    def test_stub_factory_parameter_handling(self):
        """Test stub factory parameter validation."""
        mock_akash_client = Mock()
        client = ProviderGRPCClient(mock_akash_client)

        with patch.object(client, '_create_secure_channel', return_value=Mock()):
            with patch('akash.grpc_client.LeaseRPCStub'):
                stub = client._get_lease_stub("provider.example.com:8443", "akash1owner")
                assert stub is not None

            with pytest.raises(Exception):
                client._get_lease_stub("", "akash1owner")

            with pytest.raises(Exception):
                client._get_lease_stub("provider.example.com:8443", "")

class TestGRPCIntegrationScenarios:
    """Test complete gRPC integration scenarios."""

    def test_full_grpc_workflow_success(self):
        """Test complete gRPC workflow from connection to response."""
        mock_akash_client = Mock()
        client = ProviderGRPCClient(mock_akash_client)

        mock_channel = Mock()
        mock_stub = Mock()
        mock_response = {"status": "active", "available_resources": {}}
        mock_method = Mock(return_value=mock_response)
        mock_stub.SendManifest = mock_method
        mock_request = Mock()

        with patch.object(client, '_create_secure_channel', return_value=mock_channel), \
                patch('akash.grpc_client.LeaseRPCStub', return_value=mock_stub):
            def stub_factory(endpoint, owner, use_mtls, insecure):
                return client._get_lease_stub(endpoint, owner, use_mtls)

            result = client.call_with_retry(stub_factory, "SendManifest", mock_request)

            assert result["status"] == "success"
            assert result["response"] == mock_response

    def test_grpc_workflow_with_failover(self):
        """Test gRPC workflow with failover after retry."""
        mock_akash_client = Mock()
        client = ProviderGRPCClient(mock_akash_client)

        mock_channel = Mock()
        mock_stub = Mock()

        error = grpc.RpcError("Temporary failure")
        error.code = Mock(return_value=grpc.StatusCode.UNAVAILABLE)
        error.details = Mock(return_value="Temporary failure")

        mock_response = {"status": "active"}
        mock_method = Mock(side_effect=[
            error,
            mock_response
        ])
        mock_stub.SendManifest = mock_method
        mock_request = Mock()

        with patch.object(client, '_create_secure_channel', return_value=mock_channel), \
                patch('akash.grpc_client.LeaseRPCStub', return_value=mock_stub):
            def stub_factory(endpoint, owner, use_mtls, insecure):
                return client._get_lease_stub(endpoint, owner, use_mtls)

            result = client.call_with_retry(stub_factory, "SendManifest", mock_request, retries=2)

            assert result["status"] == "success"
            assert result["response"] == mock_response
            assert mock_method.call_count == 2

    def test_grpc_workflow_complete_failure(self):
        """Test gRPC workflow with complete failure."""
        mock_akash_client = Mock()
        client = ProviderGRPCClient(mock_akash_client)

        mock_channel = Mock()
        mock_stub = Mock()
        mock_method = Mock(side_effect=grpc.RpcError("Persistent failure"))
        mock_stub.SendManifest = mock_method
        mock_request = Mock()

        with patch.object(client, '_create_secure_channel', return_value=mock_channel), \
                patch('akash.grpc_client.LeaseRPCStub', return_value=mock_stub):
            def stub_factory(endpoint, owner, use_mtls, insecure):
                return client._get_lease_stub(endpoint, owner, use_mtls)

            result = client.call_with_retry(stub_factory, "SendManifest", mock_request, retries=1)

            assert result["status"] == "error"
            assert "Persistent failure" in result["error"]

class TestProviderGRPCClientImports:
    """Test that ALL gRPC client module imports actually work (not mocked)."""

    def test_all_module_imports(self):
        """Verify ALL gRPC client dependencies import successfully."""
        # Standard library imports
        import grpc
        import logging
        import requests
        import socket
        import time
        import ssl
        import os
        from typing import Dict, Any, Optional, Callable

        # Provider gRPC service stubs
        from akash.proto.akash.provider.lease.v1.service_pb2_grpc import LeaseRPCStub
        from akash.proto.akash.provider.v1.service_pb2_grpc import ProviderRPCStub

        # Provider protobuf messages
        from akash.proto.akash.provider.v1.status_pb2 import Status

        # Google protobuf utilities
        from google.protobuf.empty_pb2 import Empty
        from google.protobuf.json_format import MessageToDict

        # All imports succeeded if we reach here
        assert True

    def test_grpc_stub_instantiation(self):
        """Verify gRPC stubs can be instantiated."""
        import grpc
        from akash.proto.akash.provider.lease.v1.service_pb2_grpc import LeaseRPCStub
        from akash.proto.akash.provider.v1.service_pb2_grpc import ProviderRPCStub

        # Create a mock channel
        mock_channel = Mock()

        # Test LeaseRPCStub instantiation
        lease_stub = LeaseRPCStub(mock_channel)
        assert lease_stub is not None
        assert hasattr(lease_stub, 'SendManifest')
        assert hasattr(lease_stub, 'ServiceStatus')
        assert hasattr(lease_stub, 'ServiceLogs')
        assert hasattr(lease_stub, 'StreamServiceLogs')

        # Test ProviderRPCStub instantiation
        provider_stub = ProviderRPCStub(mock_channel)
        assert provider_stub is not None
        assert hasattr(provider_stub, 'GetStatus')

    def test_protobuf_message_instantiation(self):
        """Verify protobuf messages can be instantiated."""
        from akash.proto.akash.provider.v1.status_pb2 import Status
        from google.protobuf.empty_pb2 import Empty

        # Test Status message
        status = Status()
        assert status is not None

        # Test Empty message
        empty = Empty()
        assert empty is not None

    def test_protobuf_json_conversion(self):
        """Verify protobuf JSON conversion works."""
        from akash.proto.akash.provider.v1.status_pb2 import Status
        from google.protobuf.json_format import MessageToDict
        from google.protobuf.empty_pb2 import Empty

        # Test Empty message to dict conversion
        empty = Empty()
        empty_dict = MessageToDict(empty)
        assert isinstance(empty_dict, dict)

    def test_grpc_channel_primitives(self):
        """Verify gRPC channel creation primitives work."""
        import grpc
        import ssl

        # Test gRPC channel options
        options = [
            ('grpc.keepalive_time_ms', 60000),
            ('grpc.keepalive_timeout_ms', 20000),
        ]
        assert isinstance(options, list)

        # Test SSL constants access
        assert hasattr(ssl, 'CERT_REQUIRED')
        assert hasattr(ssl, 'PROTOCOL_TLS')


class TestGRPCPerformanceAndLogging:
    """Test gRPC performance monitoring and logging."""

    def test_call_timing_logging(self):
        """Test that gRPC calls are timed and logged."""
        mock_akash_client = Mock()
        client = ProviderGRPCClient(mock_akash_client)

        mock_stub = Mock()
        mock_method = Mock(return_value="success")
        mock_stub.SendManifest = mock_method
        mock_request = Mock()

        def stub_factory(endpoint, owner, use_mtls, insecure):
            return mock_stub

        with patch('akash.grpc_client.logger') as mock_logger:
            result = client.call_with_retry(stub_factory, "SendManifest", mock_request)

            mock_logger.debug.assert_called()

    def test_retry_attempt_logging(self):
        """Test that retry attempts are logged."""
        mock_akash_client = Mock()
        client = ProviderGRPCClient(mock_akash_client)

        mock_stub = Mock()
        mock_method = Mock(side_effect=[
            grpc.RpcError("First failure"),
            "success"
        ])
        mock_stub.SendManifest = mock_method
        mock_request = Mock()

        def stub_factory(endpoint, owner, use_mtls, insecure):
            return mock_stub

        with patch('akash.grpc_client.logger') as mock_logger:
            result = client.call_with_retry(stub_factory, "SendManifest", mock_request, retries=2)

            mock_logger.warning.assert_called()

if __name__ == '__main__':
    print("✅ Running gRPC client infrastructure tests")
    print("=" * 70)
    print()
    print("gRPC tests: testing provider gRPC client infrastructure, connection")
    print("management, retry logic, mTLS authentication, and error handling.")
    print()
    print("These tests cover secure provider communication functionality.")
    print()

    pytest.main([__file__, '-v'])
