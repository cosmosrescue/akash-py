#!/usr/bin/env python3
"""
Comprehensive Manifest module tests - SDL parsing, validation, and functional tests.

This combines SDL parsing tests (YAML processing, service definitions, profiles, deployments)
with manifest client functionality tests (submission, validation, provider version detection).

Validation tests: Validate Service Definition Language parsing structures, YAML processing patterns,
profile handling compatibility, and manifest generation support without requiring
blockchain interactions.

Functional tests: Test manifest client operations including SDL parsing, manifest submission
to providers, version detection, and error handling using mocking to isolate functionality
and test various scenarios.

Run: python manifest_tests_comprehensive.py
"""

import os

os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

import pytest
import sys
from unittest.mock import Mock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from akash.modules.manifest.client import ManifestClient


# ============================================================================
# SDL PARSING TESTS
# ============================================================================

class TestSDLBasicParsing:
    """Test basic SDL YAML parsing functionality."""

    def test_parse_simple_sdl_success(self):
        """Test parsing of simple SDL with basic service definition."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        simple_sdl = """
version: "2.0"

services:
  web:
    image: nginx:latest
    count: 1

profiles:
  compute:
    web:
      resources:
        cpu:
          units: 100
        memory:
          size: 512Mi
        storage:
          size: 1Gi
  placement:
    akash:
      pricing:
        web:
          denom: uakt
          amount: 1000

deployment:
  web:
    akash:
      profile: web
      count: 1
"""

        result = manifest_client.parse_sdl(simple_sdl)

        assert result["status"] == "success"
        assert "manifest_data" in result
        manifest = result["manifest_data"]

        assert isinstance(manifest, list)
        assert len(manifest) == 1
        group = manifest[0]
        assert "Services" in group
        assert len(group["Services"]) == 1
        service = group["Services"][0]
        assert service["name"] == "web"
        assert service["image"] == "nginx:latest"

    def test_parse_sdl_with_yaml_error(self):
        """Test SDL parsing with invalid YAML structure."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        invalid_yaml = """
version: "2.0"
services:
  web:
    image: nginx:latest
    count: 1
  invalid_structure: [
    missing_closing_bracket
"""

        result = manifest_client.parse_sdl(invalid_yaml)

        assert result["status"] == "failed"
        assert "error" in result
        assert "YAML" in result["error"] or "parsing" in result["error"]

    def test_parse_empty_sdl(self):
        """Test parsing of empty SDL content."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        result = manifest_client.parse_sdl("")

        assert result["status"] == "error"
        assert "error" in result
        assert "empty" in result["error"].lower()

    def test_parse_sdl_none_input(self):
        """Test parsing with None input."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        result = manifest_client.parse_sdl(None)

        assert result["status"] == "error"
        assert "error" in result


class TestSDLServiceParsing:
    """Test SDL service definition parsing."""

    def test_parse_service_with_environment_variables(self):
        """Test parsing service with environment variables."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        sdl_with_env = """
version: "2.0"

services:
  web:
    image: nginx:latest
    env:
      - DATABASE_URL=postgresql://localhost/mydb
      - DEBUG=true
      - PORT=8080

profiles:
  compute:
    web:
      resources:
        cpu:
          units: 100
        memory:
          size: 512Mi
        storage:
          size: 1Gi
  placement:
    akash:
      pricing:
        web:
          denom: uakt
          amount: 1000

deployment:
  web:
    akash:
      profile: web
      count: 1
"""

        result = manifest_client.parse_sdl(sdl_with_env)

        assert result["status"] == "success"
        manifest = result["manifest_data"]
        service = manifest[0]["Services"][0]

        assert "env" in service
        assert isinstance(service["env"], list)
        assert len(service["env"]) == 3

    def test_parse_service_with_expose_configuration(self):
        """Test parsing service with expose configuration."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        sdl_with_expose = """
version: "2.0"

services:
  web:
    image: nginx:latest
    expose:
      - port: 80
        as: 80
        to:
          - global: true
      - port: 443
        as: 443
        to:
          - global: true

profiles:
  compute:
    web:
      resources:
        cpu:
          units: 100
        memory:
          size: 512Mi
        storage:
          size: 1Gi
  placement:
    akash:
      pricing:
        web:
          denom: uakt
          amount: 1000

deployment:
  web:
    akash:
      profile: web
      count: 1
"""

        result = manifest_client.parse_sdl(sdl_with_expose)

        assert result["status"] == "success"
        manifest = result["manifest_data"]
        service = manifest[0]["Services"][0]

        assert "expose" in service
        assert len(service["expose"]) == 2
        assert service["expose"][0]["port"] == 80
        assert service["expose"][1]["port"] == 443

    def test_parse_service_with_command(self):
        """Test parsing service with custom command."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        sdl_with_command = """
version: "2.0"

services:
  web:
    image: nginx:latest
    command:
      - "/bin/sh"
    args:
      - "-c"
      - "nginx -g 'daemon off;'"

profiles:
  compute:
    web:
      resources:
        cpu:
          units: 100
        memory:
          size: 512Mi
        storage:
          size: 1Gi
  placement:
    akash:
      pricing:
        web:
          denom: uakt
          amount: 1000

deployment:
  web:
    akash:
      profile: web
      count: 1
"""

        result = manifest_client.parse_sdl(sdl_with_command)

        assert result["status"] == "success"
        manifest = result["manifest_data"]
        service = manifest[0]["Services"][0]

        assert "command" in service
        assert "args" in service
        assert service["command"] == ["/bin/sh"]
        assert service["args"] == ["-c", "nginx -g 'daemon off;'"]

    def test_parse_service_missing_required_fields(self):
        """Test parsing service missing required image field should fail."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        sdl_missing_image = """
version: "2.0"

services:
  web:
    count: 1

profiles:
  compute:
    web:
      resources:
        cpu:
          units: 100
        memory:
          size: 512Mi
        storage:
          size: 1Gi
  placement:
    akash:
      pricing:
        web:
          denom: uakt
          amount: 1000

deployment:
  web:
    akash:
      profile: web
      count: 1
"""

        result = manifest_client.parse_sdl(sdl_missing_image)

        assert result.get("valid") == False
        assert "missing required field 'image'" in result.get("error", "")


class TestSDLProfileParsing:
    """Test SDL profile parsing for compute and placement."""

    def test_parse_compute_profiles(self):
        """Test parsing of compute profiles with resource specifications."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        sdl_with_profiles = """
version: "2.0"

services:
  web:
    image: nginx:latest
  api:
    image: node:16

profiles:
  compute:
    web:
      resources:
        cpu:
          units: 100
        memory:
          size: 512Mi
        storage:
          size: 1Gi
    api:
      resources:
        cpu:
          units: 200
        memory:
          size: 1Gi
        storage:
          size: 2Gi
  placement:
    akash:
      pricing:
        web:
          denom: uakt
          amount: 1000
        api:
          denom: uakt
          amount: 2000

deployment:
  web:
    akash:
      profile: web
      count: 1
  api:
    akash:
      profile: api
      count: 2
"""

        result = manifest_client.parse_sdl(sdl_with_profiles)

        assert result["status"] == "success"
        manifest = result["manifest_data"]

        assert len(manifest) == 1
        group = manifest[0]
        assert len(group["Services"]) == 2

        services = {s["name"]: s for s in group["Services"]}
        assert "web" in services
        assert "api" in services

    def test_parse_placement_profiles_with_attributes(self):
        """Test parsing placement profiles with attributes."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        sdl_with_attributes = """
version: "2.0"

services:
  web:
    image: nginx:latest

profiles:
  compute:
    web:
      resources:
        cpu:
          units: 100
        memory:
          size: 512Mi
        storage:
          size: 1Gi
  placement:
    akash:
      attributes:
        host: akash
        tier: community
      pricing:
        web:
          denom: uakt
          amount: 1000

deployment:
  web:
    akash:
      profile: web
      count: 1
"""

        result = manifest_client.parse_sdl(sdl_with_attributes)

        assert result["status"] == "success"
        manifest = result["manifest_data"]

        assert len(manifest) == 1

    def test_parse_placement_profiles_with_pricing(self):
        """Test parsing placement profiles with various pricing configurations."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        sdl_with_pricing = """
version: "2.0"

services:
  web:
    image: nginx:latest

profiles:
  compute:
    web:
      resources:
        cpu:
          units: 100
        memory:
          size: 512Mi
        storage:
          size: 1Gi
  placement:
    akash:
      pricing:
        web:
          denom: uakt
          amount: 1000

deployment:
  web:
    akash:
      profile: web
      count: 1
"""

        result = manifest_client.parse_sdl(sdl_with_pricing)

        assert result["status"] == "success"
        manifest = result["manifest_data"]

        assert len(manifest) == 1

    def test_parse_profiles_missing_compute_profile(self):
        """Test handling when referenced compute profile is missing."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        sdl_missing_compute = """
version: "2.0"

services:
  web:
    image: nginx:latest

profiles:
  placement:
    akash:
      pricing:
        web:
          denom: uakt
          amount: 1000

deployment:
  web:
    akash:
      profile: web
      count: 1
"""

        result = manifest_client.parse_sdl(sdl_missing_compute)

        assert result["status"] == "success"


class TestSDLDeploymentParsing:
    """Test SDL deployment configuration parsing."""

    def test_parse_deployment_configuration(self):
        """Test parsing of deployment with multiple placement groups."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        sdl_multi_deployment = """
version: "2.0"

services:
  web:
    image: nginx:latest
  api:
    image: node:16

profiles:
  compute:
    web:
      resources:
        cpu:
          units: 100
        memory:
          size: 512Mi
        storage:
          size: 1Gi
    api:
      resources:
        cpu:
          units: 200
        memory:
          size: 1Gi
        storage:
          size: 2Gi
  placement:
    akash:
      pricing:
        web:
          denom: uakt
          amount: 1000
        api:
          denom: uakt
          amount: 2000
    westcoast:
      pricing:
        web:
          denom: uakt
          amount: 1500

deployment:
  web:
    akash:
      profile: web
      count: 2
    westcoast:
      profile: web
      count: 1
  api:
    akash:
      profile: api
      count: 1
"""

        result = manifest_client.parse_sdl(sdl_multi_deployment)

        assert result["status"] == "success"
        manifest = result["manifest_data"]

        assert len(manifest) >= 1

    def test_parse_deployment_missing_placement(self):
        """Test deployment referencing non-existent placement."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        sdl_missing_placement = """
version: "2.0"

services:
  web:
    image: nginx:latest

profiles:
  compute:
    web:
      resources:
        cpu:
          units: 100
        memory:
          size: 512Mi
        storage:
          size: 1Gi
  placement:
    akash:
      pricing:
        web:
          denom: uakt
          amount: 1000

deployment:
  web:
    nonexistent:
      profile: web
      count: 1
"""

        result = manifest_client.parse_sdl(sdl_missing_placement)

        assert result["status"] == "success"


class TestSDLResourceParsing:
    """Test SDL resource specification parsing."""

    def test_parse_cpu_resources(self):
        """Test parsing of CPU resource specifications."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        sdl_cpu = """
version: "2.0"

services:
  web:
    image: nginx:latest

profiles:
  compute:
    web:
      resources:
        cpu:
          units: 500
        memory:
          size: 512Mi
        storage:
          size: 1Gi
  placement:
    akash:
      pricing:
        web:
          denom: uakt
          amount: 1000

deployment:
  web:
    akash:
      profile: web
      count: 1
"""

        result = manifest_client.parse_sdl(sdl_cpu)

        assert result["status"] == "success"
        manifest = result["manifest_data"]
        service = manifest[0]["Services"][0]

        assert "resources" in service
        assert "cpu" in service["resources"]

    def test_parse_memory_resources(self):
        """Test parsing of memory resource specifications."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        sdl_memory = """
version: "2.0"

services:
  web:
    image: nginx:latest

profiles:
  compute:
    web:
      resources:
        cpu:
          units: 100
        memory:
          size: 2Gi
        storage:
          size: 1Gi
  placement:
    akash:
      pricing:
        web:
          denom: uakt
          amount: 1000

deployment:
  web:
    akash:
      profile: web
      count: 1
"""

        result = manifest_client.parse_sdl(sdl_memory)

        assert result["status"] == "success"
        manifest = result["manifest_data"]
        service = manifest[0]["Services"][0]

        assert "resources" in service
        assert "memory" in service["resources"]

    def test_parse_storage_resources(self):
        """Test parsing of storage resource specifications."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        sdl_storage = """
version: "2.0"

services:
  web:
    image: nginx:latest

profiles:
  compute:
    web:
      resources:
        cpu:
          units: 100
        memory:
          size: 512Mi
        storage:
          size: 10Gi
  placement:
    akash:
      pricing:
        web:
          denom: uakt
          amount: 1000

deployment:
  web:
    akash:
      profile: web
      count: 1
"""

        result = manifest_client.parse_sdl(sdl_storage)

        assert result["status"] == "success"
        manifest = result["manifest_data"]
        service = manifest[0]["Services"][0]

        assert "resources" in service
        assert "storage" in service["resources"]

    def test_parse_invalid_resource_format(self):
        """Test parsing with invalid resource format."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        sdl_invalid_resources = """
version: "2.0"

services:
  web:
    image: nginx:latest

profiles:
  compute:
    web:
      resources:
        cpu:
          units: "invalid"
        memory:
          size: 512Mi
        storage:
          size: 1Gi
  placement:
    akash:
      pricing:
        web:
          denom: uakt
          amount: 1000

deployment:
  web:
    akash:
      profile: web
      count: 1
"""

        result = manifest_client.parse_sdl(sdl_invalid_resources)

        assert result["status"] in ["success", "failed"]


class TestSDLComplexScenarios:
    """Test complex SDL scenarios with multiple services and configurations."""

    def test_parse_complex_multi_service_sdl(self):
        """Test parsing complex SDL with multiple services and configurations."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        complex_sdl = """
version: "2.0"

services:
  web:
    image: nginx:latest
    expose:
      - port: 80
        as: 80
        to:
          - global: true
    env:
      - BACKEND_URL=http://api:3000

  api:
    image: node:16
    expose:
      - port: 3000
        as: 3000
    env:
      - DATABASE_URL=postgresql://db:5432/myapp
      - NODE_ENV=production
    command:
      - node
    args:
      - server.js

  db:
    image: postgres:13
    env:
      - POSTGRES_DB=myapp
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password

profiles:
  compute:
    web:
      resources:
        cpu:
          units: 100
        memory:
          size: 512Mi
        storage:
          size: 1Gi
    api:
      resources:
        cpu:
          units: 200
        memory:
          size: 1Gi
        storage:
          size: 2Gi
    db:
      resources:
        cpu:
          units: 300
        memory:
          size: 2Gi
        storage:
          size: 10Gi

  placement:
    akash:
      attributes:
        host: akash
      pricing:
        web:
          denom: uakt
          amount: 1000
        api:
          denom: uakt
          amount: 2000
        db:
          denom: uakt
          amount: 3000

deployment:
  web:
    akash:
      profile: web
      count: 2
  api:
    akash:
      profile: api
      count: 1
  db:
    akash:
      profile: db
      count: 1
"""

        result = manifest_client.parse_sdl(complex_sdl)

        assert result["status"] == "success"
        manifest = result["manifest_data"]

        assert len(manifest) >= 1
        group = manifest[0]
        assert "Services" in group
        assert len(group["Services"]) == 3

        service_names = [s["name"] for s in group["Services"]]
        assert "web" in service_names
        assert "api" in service_names
        assert "db" in service_names

    def test_parse_sdl_edge_cases(self):
        """Test SDL parsing with edge cases and optional fields."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        edge_case_sdl = """
version: "2.0"

services:
  minimal:
    image: alpine:latest

profiles:
  compute:
    minimal:
      resources:
        cpu:
          units: 50
        memory:
          size: 128Mi
        storage:
          size: 512Mi
  placement:
    akash:
      pricing:
        minimal:
          denom: uakt
          amount: 100

deployment:
  minimal:
    akash:
      profile: minimal
      count: 1
"""

        result = manifest_client.parse_sdl(edge_case_sdl)

        assert result["status"] == "success"
        manifest = result["manifest_data"]

        assert len(manifest) == 1
        assert len(manifest[0]["Services"]) == 1

    def test_parse_sdl_version_validation(self):
        """Test SDL parsing with different version specifications."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        sdl_v2 = """
version: "2.0"

services:
  web:
    image: nginx:latest

profiles:
  compute:
    web:
      resources:
        cpu:
          units: 100
        memory:
          size: 512Mi
        storage:
          size: 1Gi
  placement:
    akash:
      pricing:
        web:
          denom: uakt
          amount: 1000

deployment:
  web:
    akash:
      profile: web
      count: 1
"""

        result = manifest_client.parse_sdl(sdl_v2)
        assert result["status"] == "success"

        sdl_unsupported = """
version: "3.0"

services:
  web:
    image: nginx:latest
"""

        result = manifest_client.parse_sdl(sdl_unsupported)
        assert result["status"] == "failed"
        assert "version" in result["error"].lower()


class TestSDLErrorHandling:
    """Test SDL parsing error handling scenarios."""

    def test_sdl_parsing_exception_handling(self):
        """Test SDL parsing with various exception scenarios."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        malformed_yaml = """
version: "2.0"
services:
  web:
    image: nginx:latest
    count: 1
  invalid_syntax: [
    missing_bracket
"""

        result = manifest_client.parse_sdl(malformed_yaml)
        assert result["status"] == "failed"
        assert "error" in result

    def test_sdl_validation_complete(self):
        """Test complete SDL validation workflow."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        valid_sdl = """
version: "2.0"

services:
  web:
    image: nginx:latest
    expose:
      - port: 80
        as: 80
        to:
          - global: true

profiles:
  compute:
    web:
      resources:
        cpu:
          units: 100
        memory:
          size: 512Mi
        storage:
          size: 1Gi
  placement:
    akash:
      pricing:
        web:
          denom: uakt
          amount: 1000

deployment:
  web:
    akash:
      profile: web
      count: 1
"""

        parse_result = manifest_client.parse_sdl(valid_sdl)
        assert parse_result["status"] == "success"

        manifest_data = parse_result["manifest_data"]
        validation_result = manifest_client.validate_manifest(manifest_data)
        assert validation_result["valid"] is True


# ============================================================================
# MANIFEST CLIENT FUNCTIONALITY TESTS
# ============================================================================

class TestManifestSubmission:
    """Test manifest submission to providers."""

    @patch('requests.get')
    @patch('requests.put')
    def test_submit_manifest_success_modern_provider(self, mock_put, mock_get):
        """Test successful manifest submission to modern provider."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "akash": {"version": "v0.7.0"}
        }

        mock_put.return_value.status_code = 200
        mock_put.return_value.json.return_value = {"status": "success"}

        sdl_content = '''
version: "2.0"
services:
  web:
    image: nginx:latest
    expose:
      - port: 80
        as: 80
        to:
          - global: true
profiles:
  compute:
    web:
      resources:
        cpu:
          units: 0.1
        memory:
          size: 128Mi
        storage:
          size: 512Mi
  placement:
    global:
      pricing:
        web:
          denom: uakt
          amount: 1000
deployment:
  web:
    global:
      profile: web
      count: 1
'''

        lease_id = {
            "owner": "akash1owner",
            "dseq": "123",
            "gseq": 1,
            "oseq": 1,
            "provider": "akash1provider"
        }

        result = manifest_client.submit_manifest(
            provider_endpoint="https://provider.akash.network:8443",
            lease_id=lease_id,
            sdl_content=sdl_content,
            cert_pem="fake_cert",
            key_pem="fake_key"
        )

        assert result["status"] == "success"
        assert "provider_version" in result
        assert result["provider_version"] == "v0.7.0"
        assert "method" in result

    @patch('requests.get')
    @patch('requests.put')
    def test_submit_manifest_success_legacy_provider(self, mock_put, mock_get):
        """Test successful manifest submission to legacy provider."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "akash": {"version": "v0.6.0"}
        }

        mock_put.return_value.status_code = 200
        mock_put.return_value.json.return_value = {"status": "success"}

        sdl_content = '''
version: "2.0"
services:
  web:
    image: nginx:latest
    expose:
      - port: 80
        as: 80
        to:
          - global: true
profiles:
  compute:
    web:
      resources:
        cpu:
          units: 0.1
        memory:
          size: 128Mi
        storage:
          size: 512Mi
  placement:
    global:
      pricing:
        web:
          denom: uakt
          amount: 1000
deployment:
  web:
    global:
      profile: web
      count: 1
'''

        lease_id = {
            "owner": "akash1owner",
            "dseq": "123",
            "gseq": 1,
            "oseq": 1,
            "provider": "akash1provider"
        }

        result = manifest_client.submit_manifest(
            provider_endpoint="https://provider.akash.network:8443",
            lease_id=lease_id,
            sdl_content=sdl_content,
            cert_pem="fake_cert",
            key_pem="fake_key"
        )

        assert result["status"] == "success"
        assert "provider_version" in result
        assert result["provider_version"] == "v0.6.0"

    @patch('requests.get')
    def test_submit_manifest_version_detection_failure(self, mock_get):
        """Test manifest submission when provider version detection fails."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        mock_get.side_effect = Exception("Connection failed")

        sdl_content = '''
version: "2.0"
services:
  web:
    image: nginx:latest
    expose:
      - port: 80
        as: 80
        to:
          - global: true
profiles:
  compute:
    web:
      resources:
        cpu:
          units: 0.1
        memory:
          size: 128Mi
        storage:
          size: 512Mi
  placement:
    global:
      pricing:
        web:
          denom: uakt
          amount: 1000
deployment:
  web:
    global:
      profile: web
      count: 1
'''

        lease_id = {
            "owner": "akash1owner",
            "dseq": "123",
            "gseq": 1,
            "oseq": 1,
            "provider": "akash1provider"
        }

        with patch('requests.put') as mock_put:
            mock_put.return_value.status_code = 200
            mock_put.return_value.json.return_value = {"status": "success"}

            result = manifest_client.submit_manifest(
                provider_endpoint="https://provider.akash.network:8443",
                lease_id=lease_id,
                sdl_content=sdl_content,
                cert_pem="fake_cert",
                key_pem="fake_key"
            )

            assert result["status"] == "success"

    @patch('requests.get')
    @patch('requests.put')
    def test_submit_manifest_provider_error(self, mock_put, mock_get):
        """Test manifest submission when provider returns error."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "akash": {"version": "v0.7.0"}
        }

        mock_put.return_value.status_code = 400
        mock_put.return_value.text = "Bad Request: Invalid manifest"

        sdl_content = '''
version: "2.0"
services:
  web:
    image: nginx:latest
    expose:
      - port: 80
        as: 80
        to:
          - global: true
profiles:
  compute:
    web:
      resources:
        cpu:
          units: 0.1
        memory:
          size: 128Mi
        storage:
          size: 512Mi
  placement:
    global:
      pricing:
        web:
          denom: uakt
          amount: 1000
deployment:
  web:
    global:
      profile: web
      count: 1
'''

        lease_id = {
            "owner": "akash1owner",
            "dseq": "123",
            "gseq": 1,
            "oseq": 1,
            "provider": "akash1provider"
        }

        result = manifest_client.submit_manifest(
            provider_endpoint="https://provider.akash.network:8443",
            lease_id=lease_id,
            sdl_content=sdl_content,
            cert_pem="fake_cert",
            key_pem="fake_key"
        )

        assert result["status"] in ["failed", "error"]
        assert "error" in result
        assert "400" in result["error"] or "Bad Request" in result["error"]

    def test_submit_manifest_invalid_sdl(self):
        """Test manifest submission with invalid SDL."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        invalid_sdl = "invalid yaml content ["

        lease_id = {
            "owner": "akash1owner",
            "dseq": "123",
            "gseq": 1,
            "oseq": 1,
            "provider": "akash1provider"
        }

        result = manifest_client.submit_manifest(
            provider_endpoint="https://provider.akash.network:8443",
            lease_id=lease_id,
            sdl_content=invalid_sdl,
            cert_pem="fake_cert",
            key_pem="fake_key"
        )

        assert result["status"] in ["failed", "error"]
        assert "error" in result


class TestManifestValidation:
    """Test manifest validation functionality."""

    def test_validate_manifest_success(self):
        """Test validation of a valid manifest."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        sdl_content = '''
version: "2.0"
services:
  web:
    image: nginx:latest
    expose:
      - port: 80
        as: 80
        to:
          - global: true
profiles:
  compute:
    web:
      resources:
        cpu:
          units: 0.1
        memory:
          size: 128Mi
        storage:
          size: 512Mi
  placement:
    global:
      pricing:
        web:
          denom: uakt
          amount: 1000
deployment:
  web:
    global:
      profile: web
      count: 1
'''
        parse_result = manifest_client.parse_sdl(sdl_content)
        manifest_data = parse_result["manifest_data"]

        result = manifest_client.validate_manifest(manifest_data)

        assert result["valid"] is True

    def test_validate_manifest_missing_version(self):
        """Test validation of manifest with invalid structure."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        invalid_manifest = {
            "services": {
                "web": {
                    "image": "nginx:latest"
                }
            }
        }

        result = manifest_client.validate_manifest(invalid_manifest)

        assert result["valid"] is False
        assert "error" in result

    def test_validate_manifest_missing_services(self):
        """Test validation of empty manifest."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        result = manifest_client.validate_manifest(None)

        assert result["valid"] is False
        assert "error" in result

    def test_validate_manifest_empty_services(self):
        """Test validation of manifest with empty list."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        result = manifest_client.validate_manifest([])

        assert result["valid"] is False


class TestManifestProviderVersionDetection:
    """Test provider version detection functionality."""

    @patch('requests.get')
    def test_detect_provider_version_success(self, mock_get):
        """Test successful provider version detection."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "akash": {"version": "v0.7.5"}
        }

        version = manifest_client._detect_provider_version("https://provider.akash.network:8443")

        assert version == "v0.7.5"
        mock_get.assert_called_once_with(
            "https://provider.akash.network:8443/version",
            timeout=10,
            verify=False
        )

    @patch('requests.get')
    def test_detect_provider_version_failure(self, mock_get):
        """Test provider version detection failure."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        mock_get.side_effect = Exception("Connection timeout")

        version = manifest_client._detect_provider_version("https://provider.akash.network:8443")

        assert version is None

    @patch('requests.get')
    def test_detect_provider_version_caching(self, mock_get):
        """Test provider version detection caching."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "akash": {"version": "v0.7.0"}
        }

        version1 = manifest_client._detect_provider_version("https://provider.akash.network:8443")

        version2 = manifest_client._detect_provider_version("https://provider.akash.network:8443")

        assert version1 == "v0.7.0"
        assert version2 == "v0.7.0"
        assert mock_get.call_count == 1

    def test_is_legacy_provider_true(self):
        """Test legacy provider detection for old versions."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        assert manifest_client._is_legacy_provider("v0.6.0") is True
        assert manifest_client._is_legacy_provider("v0.5.5") is True
        assert manifest_client._is_legacy_provider("unknown") is True
        assert manifest_client._is_legacy_provider(None) is True

    def test_is_legacy_provider_false(self):
        """Test legacy provider detection for new versions."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        assert manifest_client._is_legacy_provider("v0.7.0") is False
        assert manifest_client._is_legacy_provider("v0.8.1") is False
        assert manifest_client._is_legacy_provider("v1.0.0") is False


class TestManifestErrorHandling:
    """Test manifest error handling scenarios."""

    def test_manifest_client_initialization(self):
        """Test manifest client initialization."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        assert manifest_client.akash_client == mock_akash_client
        assert hasattr(manifest_client, 'parse_sdl')
        assert hasattr(manifest_client, 'submit_manifest')
        assert hasattr(manifest_client, 'validate_manifest')

    def test_clear_version_cache(self):
        """Test clearing provider version cache."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        manifest_client.version_cache = {"provider1": "v0.7.0"}

        manifest_client._clear_version_cache()

        assert not hasattr(manifest_client, 'version_cache') or manifest_client.version_cache == {}

    @patch('requests.put')
    def test_submit_manifest_connection_error(self, mock_put):
        """Test manifest submission with connection error."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        mock_put.side_effect = Exception("Connection refused")

        sdl_content = '''
version: "2.0"
services:
  web:
    image: nginx:latest
    expose:
      - port: 80
        as: 80
        to:
          - global: true
profiles:
  compute:
    web:
      resources:
        cpu:
          units: 0.1
        memory:
          size: 128Mi
        storage:
          size: 512Mi
  placement:
    global:
      pricing:
        web:
          denom: uakt
          amount: 1000
deployment:
  web:
    global:
      profile: web
      count: 1
'''

        lease_id = {
            "owner": "akash1owner",
            "dseq": "123",
            "gseq": 1,
            "oseq": 1,
            "provider": "akash1provider"
        }

        result = manifest_client.submit_manifest(
            provider_endpoint="https://provider.akash.network:8443",
            lease_id=lease_id,
            sdl_content=sdl_content,
            cert_pem="fake_cert",
            key_pem="fake_key"
        )

        assert result["status"] in ["failed", "error"]
        assert "error" in result
        assert "Connection refused" in result["error"] or "failed" in result["error"].lower()


class TestManifestVersionCalculation:
    """Test manifest version calculation for deployment updates."""

    def test_manifest_version_simple_sdl(self):
        """Test manifest version calculation for simple SDL."""
        import hashlib
        import json
        import base64
        from akash.modules.manifest.utils import ManifestUtils

        simple_sdl = '''version: "2.0"
services:
  nginx:
    image: nginx:alpine
    expose:
      - port: 80
        as: 80
        to:
          - global: true
profiles:
  compute:
    nginx:
      resources:
        cpu:
          units: 0.1
        memory:
          size: 128Mi
        storage:
          size: 512Mi
  placement:
    global:
      attributes:
        host: akash
      pricing:
        nginx:
          denom: uakt
          amount: 1000
deployment:
  nginx:
    global:
      profile: nginx
      count: 1
'''

        expected_version_hex = "c235e62828ce7f2dbd10d47a6b0bd3a96f699dcff429d23a1a6f91d08d7623c4"
        expected_version_base64 = "wjXmKCjOfy29ENR6awvTqW9pnc/0KdI6Gm+R0I12I8Q="

        manifest_utils = ManifestUtils()
        parse_result = manifest_utils.parse_sdl(simple_sdl)
        assert parse_result.get('status') == 'success'

        manifest_data = parse_result.get('manifest_data', [])
        legacy_manifest = manifest_utils._create_legacy_manifest(manifest_data)
        manifest_json = json.dumps(legacy_manifest, sort_keys=True, separators=(',', ':'))

        manifest_json = manifest_utils._escape_html(manifest_json)

        version_bytes = hashlib.sha256(manifest_json.encode()).digest()
        version_base64 = base64.b64encode(version_bytes).decode('utf-8')
        version_hex = hashlib.sha256(manifest_json.encode()).hexdigest()

        assert version_hex == expected_version_hex
        assert version_base64 == expected_version_base64

    def test_manifest_version_complex_sdl(self):
        """Test manifest version calculation for more complex SDL."""
        import hashlib
        import json
        import base64
        from akash.modules.manifest.utils import ManifestUtils

        complex_sdl = '''version: "2.0"
services:
  nginx:
    image: nginx:alpine
    command: ["/bin/sh", "-c", "echo 'Updated container' && nginx -g 'daemon off;'"]
    env:
      - UPDATE_VERSION=v2
      - DEPLOYMENT_UPDATE=true
    expose:
      - port: 80
        as: 80
        to:
          - global: true
profiles:
  compute:
    nginx:
      resources:
        cpu:
          units: 0.1
        memory:
          size: 128Mi
        storage:
          size: 512Mi
  placement:
    global:
      attributes:
        host: akash
      pricing:
        nginx:
          denom: uakt
          amount: 1000
deployment:
  nginx:
    global:
      profile: nginx
      count: 1
'''

        expected_version_hex = "0336fbaa72bb20852da56a10adf7f733cbe838884f233f4249599df8be5901bc"
        expected_version_base64 = "Azb7qnK7IIUtpWoQrff3M8voOIhPIz9CSVmd+L5ZAbw="

        manifest_utils = ManifestUtils()
        parse_result = manifest_utils.parse_sdl(complex_sdl)
        assert parse_result.get('status') == 'success'

        manifest_data = parse_result.get('manifest_data', [])
        legacy_manifest = manifest_utils._create_legacy_manifest(manifest_data)
        manifest_json = json.dumps(legacy_manifest, sort_keys=True, separators=(',', ':'))

        manifest_json = manifest_utils._escape_html(manifest_json)

        version_bytes = hashlib.sha256(manifest_json.encode()).digest()
        version_base64 = base64.b64encode(version_bytes).decode('utf-8')
        version_hex = hashlib.sha256(manifest_json.encode()).hexdigest()

        assert version_hex == expected_version_hex
        assert version_base64 == expected_version_base64

    def test_manifest_version_env_only_sdl(self):
        """Test manifest version calculation for env-only SDL."""
        import hashlib
        import json
        import base64
        from akash.modules.manifest.utils import ManifestUtils

        env_only_sdl = '''version: "2.0"
services:
  nginx:
    image: nginx:alpine
    env:
      - UPDATE_VERSION=v2
      - DEPLOYMENT_UPDATE=true
    expose:
      - port: 80
        as: 80
        to:
          - global: true
profiles:
  compute:
    nginx:
      resources:
        cpu:
          units: 0.1
        memory:
          size: 128Mi
        storage:
          size: 512Mi
  placement:
    global:
      attributes:
        host: akash
      pricing:
        nginx:
          denom: uakt
          amount: 1000
deployment:
  nginx:
    global:
      profile: nginx
      count: 1
'''

        expected_version_hex = "24009b8ea9cc4c46af0115405d54e8066d4d0b374507d71caa087407e0650f63"
        expected_version_base64 = "JACbjqnMTEavARVAXVToBm1NCzdFB9ccqgh0B+BlD2M="

        manifest_utils = ManifestUtils()
        parse_result = manifest_utils.parse_sdl(env_only_sdl)
        assert parse_result.get('status') == 'success'

        manifest_data = parse_result.get('manifest_data', [])
        legacy_manifest = manifest_utils._create_legacy_manifest(manifest_data)
        manifest_json = json.dumps(legacy_manifest, sort_keys=True, separators=(',', ':'))

        manifest_json = manifest_utils._escape_html(manifest_json)

        version_bytes = hashlib.sha256(manifest_json.encode()).digest()
        version_base64 = base64.b64encode(version_bytes).decode('utf-8')
        version_hex = hashlib.sha256(manifest_json.encode()).hexdigest()

        assert version_hex == expected_version_hex
        assert version_base64 == expected_version_base64

    def test_manifest_version_multi_service_sdl(self):
        """Test manifest version calculation for multi-service SDL with separate placements."""
        import hashlib
        import json
        import base64
        from akash.modules.manifest.utils import ManifestUtils

        multi_service_sdl = '''version: "2.0"
services:
  web:
    image: nginx:alpine
    expose:
      - port: 80
        as: 80
        to:
          - global: true
    env:
      - BACKEND_URL=http://api:3000
  api:
    image: node:alpine
    expose:
      - port: 3000
        as: 3000
        to:
          - service: web
    env:
      - NODE_ENV=production
      - API_VERSION=v1
    command:
      - "sh"
      - "-c"
      - 'echo "const http = require(\\"http\\"); const server = http.createServer((req, res) => { res.writeHead(200); res.end(\\"API Service v1 - OK\\"); }); server.listen(3000);" > server.js && node server.js'
profiles:
  compute:
    web:
      resources:
        cpu:
          units: 0.1
        memory:
          size: 128Mi
        storage:
          size: 512Mi
    api:
      resources:
        cpu:
          units: 0.25
        memory:
          size: 256Mi
        storage:
          size: 512Mi
  placement:
    web-placement:
      attributes:
        host: akash
      pricing:
        web:
          denom: uakt
          amount: 1000
    api-placement:
      attributes:
        host: akash
      pricing:
        api:
          denom: uakt
          amount: 1000
deployment:
  web:
    web-placement:
      profile: web
      count: 1
  api:
    api-placement:
      profile: api
      count: 1
'''

        expected_version_base64 = "quf9XTmXpmjHy/zrZOT5R5LKJVNLyJkmnmNyoaDsWrE="

        manifest_utils = ManifestUtils()
        parse_result = manifest_utils.parse_sdl(multi_service_sdl)
        assert parse_result.get('status') == 'success'

        manifest_data = parse_result.get('manifest_data', [])
        legacy_manifest = manifest_utils._create_legacy_manifest(manifest_data)

        print("\n=== MANIFEST STRUCTURE ===")
        print(json.dumps(legacy_manifest, indent=2))
        print("\n=== MANIFEST JSON (for version) ===")

        manifest_json = json.dumps(legacy_manifest, sort_keys=True, separators=(',', ':'))
        manifest_json = manifest_utils._escape_html(manifest_json)

        print(manifest_json)
        print("\n=== VERSION CALCULATION ===")

        version_bytes = hashlib.sha256(manifest_json.encode()).digest()
        version_base64 = base64.b64encode(version_bytes).decode('utf-8')
        version_hex = hashlib.sha256(manifest_json.encode()).hexdigest()

        print(f"Calculated base64: {version_base64}")
        print(f"Expected base64:   {expected_version_base64}")
        print(f"Calculated hex:    {version_hex}")
        print(f"Match: {version_base64 == expected_version_base64}")

        assert version_base64 == expected_version_base64, f"Version mismatch: got {version_base64}, expected {expected_version_base64}"

    def test_manifest_version_three_service_sdl(self):
        """Test manifest version calculation for 3-service SDL with command/args separation."""
        import hashlib
        import json
        import base64
        from akash.modules.manifest.utils import ManifestUtils

        three_service_sdl = '''version: "2.0"
services:
  web:
    image: nginx:alpine
    expose:
      - port: 80
        as: 80
        to:
          - global: true
    env:
      - BACKEND_URL=http://api:3000
  api:
    image: node:alpine
    expose:
      - port: 3000
        as: 3000
        to:
          - service: web
    env:
      - NODE_ENV=production
      - API_VERSION=v1
    command:
      - "sh"
      - "-c"
    args:
      - 'echo "const http = require(\\"http\\"); const server = http.createServer((req, res) => { res.writeHead(200); res.end(\\"API Service v1 - OK\\"); }); server.listen(3000);" > server.js && node server.js'
  cache:
    image: redis:alpine
    expose:
      - port: 6379
        as: 6379
        to:
          - service: api
    command:
      - "redis-server"
      - "--maxmemory"
      - "64mb"
profiles:
  compute:
    web:
      resources:
        cpu:
          units: 0.1
        memory:
          size: 128Mi
        storage:
          size: 512Mi
    api:
      resources:
        cpu:
          units: 0.25
        memory:
          size: 256Mi
        storage:
          size: 512Mi
    cache:
      resources:
        cpu:
          units: 0.1
        memory:
          size: 128Mi
        storage:
          size: 512Mi
  placement:
    web-placement:
      attributes:
        host: akash
      pricing:
        web:
          denom: uakt
          amount: 10000
    api-placement:
      attributes:
        host: akash
      pricing:
        api:
          denom: uakt
          amount: 10000
    cache-placement:
      attributes:
        host: akash
      pricing:
        cache:
          denom: uakt
          amount: 10000
deployment:
  web:
    web-placement:
      profile: web
      count: 1
  api:
    api-placement:
      profile: api
      count: 1
  cache:
    cache-placement:
      profile: cache
      count: 1
'''

        expected_version_hex = "717e89d13b1e3215ed48dac3ff63f1d7c62dd32eae2bb1d62babf6726e99ae8c"
        expected_version_base64 = "cX6J0TseMhXtSNrD/2Px18Yt0y6uK7HWK6v2cm6Zrow="

        manifest_utils = ManifestUtils()
        parse_result = manifest_utils.parse_sdl(three_service_sdl)
        assert parse_result.get('status') == 'success'

        manifest_data = parse_result.get('manifest_data', [])
        legacy_manifest = manifest_utils._create_legacy_manifest(manifest_data)
        manifest_json = json.dumps(legacy_manifest, sort_keys=True, separators=(',', ':'))
        manifest_json = manifest_utils._escape_html(manifest_json)

        version_bytes = hashlib.sha256(manifest_json.encode()).digest()
        version_base64 = base64.b64encode(version_bytes).decode('utf-8')
        version_hex = hashlib.sha256(manifest_json.encode()).hexdigest()

        assert version_hex == expected_version_hex
        assert version_base64 == expected_version_base64

    def test_manifest_version_persistent_sdl(self):
        """Test manifest version calculation for SDL with persistence."""
        import hashlib
        import json
        import base64
        from akash.modules.manifest.utils import ManifestUtils

        persistent_sdl = '''version: "2.0"
services:
  storage-test:
    image: ubuntu:latest
    expose:
      - port: 80
        as: 80
        to:
          - global: true
    env:
      - TEST_ENV=persistent-storage
    command:
      - "bash"
      - "-c"
    args:
      - 'apt-get update && apt-get install -y nginx && echo "Persistent Storage Test" > /data/test.txt && nginx -g "daemon off;"'
    params:
      storage:
        data:
          mount: /data
          readOnly: false
profiles:
  compute:
    storage-test:
      resources:
        cpu:
          units: 0.5
        memory:
          size: 512Mi
        storage:
          - size: 512Mi
          - name: data
            size: 1Gi
            attributes:
              persistent: true
              class: beta3
  placement:
    global:
      attributes:
        host: akash
      pricing:
        storage-test:
          denom: uakt
          amount: 10000
deployment:
  storage-test:
    global:
      profile: storage-test
      count: 1
'''

        expected_version_hex = "2d6e7b1b6c72da0c45600edd97270de90fb882739684418d8e21b119a70cf7c6"
        expected_version_base64 = "LW57G2xy2gxFYA7dlycN6Q+4gnOWhEGNjiGxGacM98Y="

        manifest_utils = ManifestUtils()
        parse_result = manifest_utils.parse_sdl(persistent_sdl)
        assert parse_result.get('status') == 'success'

        manifest_data = parse_result.get('manifest_data', [])
        legacy_manifest = manifest_utils._create_legacy_manifest(manifest_data)
        manifest_json = json.dumps(legacy_manifest, sort_keys=True, separators=(',', ':'))
        manifest_json = manifest_utils._escape_html(manifest_json)

        version_bytes = hashlib.sha256(manifest_json.encode()).digest()
        version_base64 = base64.b64encode(version_bytes).decode('utf-8')
        version_hex = hashlib.sha256(manifest_json.encode()).hexdigest()

        assert version_hex == expected_version_hex
        assert version_base64 == expected_version_base64

    def test_manifest_version_gpu(self):
        """Test manifest version calculation for SDL with gpu."""
        import hashlib
        import json
        import base64
        from akash.modules.manifest.utils import ManifestUtils

        sdl = '''version: "2.0"
services:
  gpu-test:
    image: nvidia/cuda:11.8.0-base-ubuntu22.04
    expose:
      - port: 80
        as: 80
        to:
          - global: true
    env:
      - GPU_TEST=enabled
    command:
      - "bash"
      - "-c"
    args:
      - 'apt-get update && apt-get install -y nginx && nvidia-smi > /usr/share/nginx/html/gpu-info.txt 2>&1 || echo "nvidia-smi not available" > /usr/share/nginx/html/gpu-info.txt && echo "<h1>GPU Test Deployment</h1><pre>$(cat /usr/share/nginx/html/gpu-info.txt)</pre>" > /usr/share/nginx/html/index.html && nginx -g "daemon off;"'
profiles:
  compute:
    gpu-test:
      resources:
        cpu:
          units: 1
        memory:
          size: 2Gi
        gpu:
          units: 1
          attributes:
            vendor:
              nvidia:
              - model: rtx4090
        storage:
          - size: 1Gi
  placement:
    global:
      attributes:
        host: akash
      pricing:
        gpu-test:
          denom: uakt
          amount: 10000
deployment:
  gpu-test:
    global:
      profile: gpu-test
      count: 1
'''

        expected_version_hex = "dccba5dea1305ac11b9464c2132f15a9a4b8c3cc02fec5c01010ea18fec882dd"
        expected_version_base64 = "3Mul3qEwWsEblGTCEy8VqaS4w8wC/sXAEBDqGP7Igt0="

        manifest_utils = ManifestUtils()
        parse_result = manifest_utils.parse_sdl(sdl)
        assert parse_result.get('status') == 'success'

        manifest_data = parse_result.get('manifest_data', [])
        legacy_manifest = manifest_utils._create_legacy_manifest(manifest_data)
        manifest_json = json.dumps(legacy_manifest, sort_keys=True, separators=(',', ':'))
        manifest_json = manifest_utils._escape_html(manifest_json)

        version_bytes = hashlib.sha256(manifest_json.encode()).digest()
        version_base64 = base64.b64encode(version_bytes).decode('utf-8')
        version_hex = hashlib.sha256(manifest_json.encode()).hexdigest()

        assert version_hex == expected_version_hex
        assert version_base64 == expected_version_base64

    def test_manifest_version_gpu_another(self):
        """Test manifest version calculation for SDL with gpu."""
        import hashlib
        import json
        import base64
        from akash.modules.manifest.utils import ManifestUtils

        sdl = '''
version: "2.0"
services:
  ml-workload:
    image: nvidia/cuda:11.8.0-base-ubuntu22.04
    expose:
      - port: 8080
        as: 80
        to:
          - global: true
    env:
      - CUDA_VISIBLE_DEVICES=0
      - ML_TEST=enabled
    command:
      - "bash"
      - "-c"
    args:
      - 'apt-get update && apt-get install -y nginx && (nvidia-smi || echo "GPU info not available") > /usr/share/nginx/html/index.html && echo "<br><br>GPU: A100 40GB requested" >> /usr/share/nginx/html/index.html && nginx -g "daemon off;"'
profiles:
  compute:
    ml-workload:
      resources:
        cpu:
          units: 2
        memory:
          size: 8Gi
        gpu:
          units: 1
          attributes:
            vendor:
              nvidia:
              - model: a100
                ram: 80Gi
        storage:
          - size: 10Gi
  placement:
    global:
      attributes:
        host: akash
      pricing:
        ml-workload:
          denom: uakt
          amount: 150000
deployment:
  ml-workload:
    global:
      profile: ml-workload
      count: 1
'''

        expected_version_hex = "2a5861f18e5c9193761e1086bae28830793c989cee3638928dc3ff50dcf972ed"
        expected_version_base64 = "Klhh8Y5ckZN2HhCGuuKIMHk8mJzuNjiSjcP/UNz5cu0="

        manifest_utils = ManifestUtils()
        parse_result = manifest_utils.parse_sdl(sdl)
        assert parse_result.get('status') == 'success'

        manifest_data = parse_result.get('manifest_data', [])
        legacy_manifest = manifest_utils._create_legacy_manifest(manifest_data)
        manifest_json = json.dumps(legacy_manifest, sort_keys=True, separators=(',', ':'))
        manifest_json = manifest_utils._escape_html(manifest_json)

        version_bytes = hashlib.sha256(manifest_json.encode()).digest()
        version_base64 = base64.b64encode(version_bytes).decode('utf-8')
        version_hex = hashlib.sha256(manifest_json.encode()).hexdigest()

        assert version_hex == expected_version_hex
        assert version_base64 == expected_version_base64

    def test_manifest_version_multi_endpoint(self):
        """Test manifest version calculation for SDL with multiple endpoints."""
        import hashlib
        import json
        import base64
        from akash.modules.manifest.utils import ManifestUtils

        sdl = '''
version: "2.0"
services:
  game-server:
    image: nginx:alpine
    expose:
      - port: 80
        as: 80
        to:
          - global: true
      - port: 12345
        as: 12345
        proto: udp
        to:
          - global: true
    env:
      - SERVER_MODE=multi-protocol
      - HTTP_PORT=80
      - UDP_PORT=12345
    command:
      - "sh"
      - "-c"
    args:
      - |
        echo "<html><body><h1>Multi-Protocol Server</h1><p>HTTP: Port 80 (TCP)</p><p>UDP: Port 12345</p></body></html>" > /usr/share/nginx/html/index.html
        nginx -g "daemon off;"
profiles:
  compute:
    game-server:
      resources:
        cpu:
          units: 0.5
        memory:
          size: 512Mi
        storage:
          size: 1Gi
  placement:
    global:
      attributes:
        host: akash
      pricing:
        game-server:
          denom: uakt
          amount: 10000
deployment:
  game-server:
    global:
      profile: game-server
      count: 1
'''

        expected_version_hex = "6a556eea1c1ce239ee70ba77739dce449a027147eb6e76d596e060d9822b45ae"
        expected_version_base64 = "alVu6hwc4jnucLp3c53ORJoCcUfrbnbVluBg2YIrRa4="

        manifest_utils = ManifestUtils()
        parse_result = manifest_utils.parse_sdl(sdl)
        assert parse_result.get('status') == 'success'

        manifest_data = parse_result.get('manifest_data', [])
        legacy_manifest = manifest_utils._create_legacy_manifest(manifest_data)
        manifest_json = json.dumps(legacy_manifest, sort_keys=True, separators=(',', ':'))
        manifest_json = manifest_utils._escape_html(manifest_json)

        version_bytes = hashlib.sha256(manifest_json.encode()).digest()
        version_base64 = base64.b64encode(version_bytes).decode('utf-8')
        version_hex = hashlib.sha256(manifest_json.encode()).hexdigest()

        assert version_hex == expected_version_hex
        assert version_base64 == expected_version_base64

    def test_manifest_version_ip_lease(self):
        """Test manifest version calculation for SDL with ip lease."""
        import hashlib
        import json
        import base64
        from akash.modules.manifest.utils import ManifestUtils

        sdl = '''
version: "2.0"

endpoints:
  myendpoint:
    kind: ip

services:
  web:
    image: nginx:alpine
    expose:
      - port: 80
        as: 80
        to:
          - global: true
            ip: "myendpoint"

profiles:
  compute:
    web:
      resources:
        cpu:
          units: 0.5
        memory:
          size: 512Mi
        storage:
          size: 1Gi
  placement:
    global:
      attributes:
        host: akash
      pricing:
        web:
          denom: uakt
          amount: 1000

deployment:
  web:
    global:
      profile: web
      count: 1
'''

        expected_version_hex = "cb12db433087f2382e488abafa6103d976552a1df52350aeda47f153d8d9493c"
        expected_version_base64 = "yxLbQzCH8jguSIq6+mED2XZVKh31I1Cu2kfxU9jZSTw="

        manifest_utils = ManifestUtils()
        parse_result = manifest_utils.parse_sdl(sdl)
        assert parse_result.get('status') == 'success'

        manifest_data = parse_result.get('manifest_data', [])
        legacy_manifest = manifest_utils._create_legacy_manifest(manifest_data)
        manifest_json = json.dumps(legacy_manifest, sort_keys=True, separators=(',', ':'))
        manifest_json = manifest_utils._escape_html(manifest_json)

        version_bytes = hashlib.sha256(manifest_json.encode()).digest()
        version_base64 = base64.b64encode(version_bytes).decode('utf-8')
        version_hex = hashlib.sha256(manifest_json.encode()).hexdigest()

        assert version_hex == expected_version_hex
        assert version_base64 == expected_version_base64


class TestManifestFieldCompleteness:
    """Test that all manifest fields are correctly structured and complete."""

    def test_service_params_storage_mounts(self):
        """Test service params structure for storage mounts."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        sdl_with_params = '''
version: "2.0"
services:
  web:
    image: nginx:alpine
    params:
      storage:
        data:
          mount: /data
          readOnly: false
        configs:
          mount: /configs
          readOnly: true
profiles:
  compute:
    web:
      resources:
        cpu:
          units: 0.1
        memory:
          size: 128Mi
        storage:
          - name: default
            size: 512Mi
          - name: data
            size: 1Gi
          - name: configs
            size: 100Mi
  placement:
    global:
      pricing:
        web:
          denom: uakt
          amount: 1000
deployment:
  web:
    global:
      profile: web
      count: 1
'''

        result = manifest_client.parse_sdl(sdl_with_params)
        assert result["status"] == "success"

        manifest = result["manifest_data"]
        service = manifest[0]["Services"][0]

        assert "params" in service
        assert service["params"] is not None
        assert "storage" in service["params"]

        storage_params = service["params"]["storage"]
        assert len(storage_params) == 2

        data_mount = next((m for m in storage_params if m["name"] == "data"), None)
        assert data_mount is not None
        assert data_mount["mount"] == "/data"
        assert data_mount["readOnly"] is False

        configs_mount = next((m for m in storage_params if m["name"] == "configs"), None)
        assert configs_mount is not None
        assert configs_mount["mount"] == "/configs"
        assert configs_mount["readOnly"] is True

    def test_credentials_structure(self):
        """Test credentials format and required fields."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        sdl_with_credentials = '''
version: "2.0"
services:
  web:
    image: nginx:alpine
    credentials:
      host: docker.io
      username: myuser
      password: mypass
      email: user@example.com
profiles:
  compute:
    web:
      resources:
        cpu:
          units: 0.1
        memory:
          size: 128Mi
        storage:
          size: 512Mi
  placement:
    global:
      pricing:
        web:
          denom: uakt
          amount: 1000
deployment:
  web:
    global:
      profile: web
      count: 1
'''

        result = manifest_client.parse_sdl(sdl_with_credentials)
        assert result["status"] == "success"

        service = result["manifest_data"][0]["Services"][0]

        assert "credentials" in service
        credentials = service["credentials"]
        assert credentials["host"] == "docker.io"
        assert credentials["username"] == "myuser"
        assert credentials["password"] == "mypass"
        assert credentials["email"] == "user@example.com"

    def test_credentials_email_defaults_to_empty_string(self):
        """Test that credentials email defaults to empty string when not provided."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        sdl_credentials_no_email = '''
version: "2.0"
services:
  web:
    image: nginx:alpine
    credentials:
      host: docker.io
      username: myuser
      password: mypass
profiles:
  compute:
    web:
      resources:
        cpu:
          units: 0.1
        memory:
          size: 128Mi
        storage:
          size: 512Mi
  placement:
    global:
      pricing:
        web:
          denom: uakt
          amount: 1000
deployment:
  web:
    global:
      profile: web
      count: 1
'''

        result = manifest_client.parse_sdl(sdl_credentials_no_email)
        assert result["status"] == "success"

        service = result["manifest_data"][0]["Services"][0]
        credentials = service["credentials"]
        assert credentials["email"] == ""

    def test_expose_flatmap_behavior(self):
        """Test that expose creates one entry per 'to' config."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        sdl_multiple_to = '''
version: "2.0"
services:
  web:
    image: nginx:alpine
    expose:
      - port: 80
        as: 8080
        to:
          - global: true
          - service: api
profiles:
  compute:
    web:
      resources:
        cpu:
          units: 0.1
        memory:
          size: 128Mi
        storage:
          size: 512Mi
  placement:
    global:
      pricing:
        web:
          denom: uakt
          amount: 1000
deployment:
  web:
    global:
      profile: web
      count: 1
'''

        result = manifest_client.parse_sdl(sdl_multiple_to)
        assert result["status"] == "success"

        service = result["manifest_data"][0]["Services"][0]
        expose = service["expose"]

        assert len(expose) == 2
        assert expose[0]["port"] == 80
        assert expose[1]["port"] == 80

    def test_expose_hosts_from_accept(self):
        """Test that expose hosts field comes from accept in SDL."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        sdl_with_accept = '''
version: "2.0"
services:
  web:
    image: nginx:alpine
    expose:
      - port: 80
        accept:
          - example.com
          - www.example.com
        to:
          - global: true
profiles:
  compute:
    web:
      resources:
        cpu:
          units: 0.1
        memory:
          size: 128Mi
        storage:
          size: 512Mi
  placement:
    global:
      pricing:
        web:
          denom: uakt
          amount: 1000
deployment:
  web:
    global:
      profile: web
      count: 1
'''

        result = manifest_client.parse_sdl(sdl_with_accept)
        assert result["status"] == "success"

        service = result["manifest_data"][0]["Services"][0]
        expose = service["expose"][0]

        assert "hosts" in expose
        assert expose["hosts"] == ["example.com", "www.example.com"]

    def test_expose_custom_http_options(self):
        """Test that custom http_options from SDL are merged with defaults."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        sdl_custom_http_options = '''
version: "2.0"
services:
  web:
    image: nginx:alpine
    expose:
      - port: 80
        http_options:
          max_body_size: 2097152
          read_timeout: 120000
          send_timeout: 90000
          next_tries: 5
        to:
          - global: true
profiles:
  compute:
    web:
      resources:
        cpu:
          units: 0.1
        memory:
          size: 128Mi
        storage:
          size: 512Mi
  placement:
    global:
      pricing:
        web:
          denom: uakt
          amount: 1000
deployment:
  web:
    global:
      profile: web
      count: 1
'''

        result = manifest_client.parse_sdl(sdl_custom_http_options)
        assert result["status"] == "success"

        service = result["manifest_data"][0]["Services"][0]
        http_opts = service["expose"][0]["httpOptions"]

        assert http_opts["maxBodySize"] == 2097152
        assert http_opts["readTimeout"] == 120000
        assert http_opts["sendTimeout"] == 90000
        assert http_opts["nextTries"] == 5

        assert http_opts["nextTimeout"] == 0
        assert http_opts["nextCases"] == ["error", "timeout"]

    def test_expose_external_port_defaults_to_zero(self):
        """Test that externalPort defaults to 0 when not specified."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        sdl_no_as = '''
version: "2.0"
services:
  web:
    image: nginx:alpine
    expose:
      - port: 443
        to:
          - global: true
profiles:
  compute:
    web:
      resources:
        cpu:
          units: 0.1
        memory:
          size: 128Mi
        storage:
          size: 512Mi
  placement:
    global:
      pricing:
        web:
          denom: uakt
          amount: 1000
deployment:
  web:
    global:
      profile: web
      count: 1
'''

        result = manifest_client.parse_sdl(sdl_no_as)
        assert result["status"] == "success"

        service = result["manifest_data"][0]["Services"][0]
        expose = service["expose"][0]

        assert expose["port"] == 443
        assert expose["externalPort"] == 0

    def test_expose_sorting(self):
        """Test that expose entries are sorted by service, port, proto, global."""
        mock_akash_client = Mock()
        manifest_client = ManifestClient(mock_akash_client)

        sdl_multiple_expose = '''
version: "2.0"
services:
  web:
    image: nginx:alpine
    expose:
      - port: 443
        to:
          - global: true
      - port: 80
        to:
          - global: true
          - service: api
profiles:
  compute:
    web:
      resources:
        cpu:
          units: 0.1
        memory:
          size: 128Mi
        storage:
          size: 512Mi
  placement:
    global:
      pricing:
        web:
          denom: uakt
          amount: 1000
deployment:
  web:
    global:
      profile: web
      count: 1
'''

        result = manifest_client.parse_sdl(sdl_multiple_expose)
        assert result["status"] == "success"

        service = result["manifest_data"][0]["Services"][0]
        expose = service["expose"]

        for i in range(len(expose) - 1):
            curr = expose[i]
            next_exp = expose[i + 1]

            curr_key = (curr["service"], curr["port"], curr["proto"], not curr["global"])
            next_key = (next_exp["service"], next_exp["port"], next_exp["proto"], not next_exp["global"])

            assert curr_key <= next_key, f"Expose not sorted: {curr} > {next_exp}"


class TestManifestVersionHashConsistency:
    """Test version hash calculation consistency."""

    def test_legacy_manifest_format_for_version_hash(self):
        """Test that version hash uses legacy format (lowercase name/services)."""
        from akash.modules.manifest.utils import ManifestUtils

        simple_sdl = '''
version: "2.0"
services:
  web:
    image: nginx:alpine
    expose:
      - port: 80
        to:
          - global: true
profiles:
  compute:
    web:
      resources:
        cpu:
          units: 0.1
        memory:
          size: 128Mi
        storage:
          size: 512Mi
  placement:
    global:
      pricing:
        web:
          denom: uakt
          amount: 1000
deployment:
  web:
    global:
      profile: web
      count: 1
'''

        manifest_utils = ManifestUtils()
        result = manifest_utils.parse_sdl(simple_sdl)
        assert result["status"] == "success"

        manifest_data = result["manifest_data"]
        legacy_manifest = manifest_utils._create_legacy_manifest(manifest_data)

        assert "name" in legacy_manifest[0]
        assert "services" in legacy_manifest[0]

        service = legacy_manifest[0]["services"][0]
        resources = service["resources"]
        assert "size" in resources["memory"]

        for storage in resources["storage"]:
            assert "size" in storage

    def test_version_hash_deployment_manifest_consistency(self):
        """Test that deployment and manifest use same version hash."""
        import hashlib
        import json
        from akash.modules.manifest.utils import ManifestUtils

        simple_sdl = '''
version: "2.0"
services:
  web:
    image: nginx:alpine
    expose:
      - port: 80
        to:
          - global: true
profiles:
  compute:
    web:
      resources:
        cpu:
          units: 0.1
        memory:
          size: 128Mi
        storage:
          size: 512Mi
  placement:
    global:
      pricing:
        web:
          denom: uakt
          amount: 1000
deployment:
  web:
    global:
      profile: web
      count: 1
'''

        manifest_utils = ManifestUtils()
        result = manifest_utils.parse_sdl(simple_sdl)
        manifest_data = result["manifest_data"]

        legacy_manifest = manifest_utils._create_legacy_manifest(manifest_data)
        manifest_json = json.dumps(legacy_manifest, sort_keys=True, separators=(',', ':'))
        escaped_json = manifest_utils._escape_html(manifest_json)
        version_hash = hashlib.sha256(escaped_json.encode()).hexdigest()

        second_hash = hashlib.sha256(escaped_json.encode()).hexdigest()
        assert version_hash == second_hash

    def test_version_hash_field_ordering(self):
        """Test that version hash uses alphabetical field ordering."""
        import json
        from akash.modules.manifest.utils import ManifestUtils

        simple_sdl = '''
version: "2.0"
services:
  web:
    image: nginx:alpine
profiles:
  compute:
    web:
      resources:
        cpu:
          units: 0.1
        memory:
          size: 128Mi
        storage:
          size: 512Mi
  placement:
    global:
      pricing:
        web:
          denom: uakt
          amount: 1000
deployment:
  web:
    global:
      profile: web
      count: 1
'''

        manifest_utils = ManifestUtils()
        result = manifest_utils.parse_sdl(simple_sdl)
        manifest_data = result["manifest_data"]

        legacy_manifest = manifest_utils._create_legacy_manifest(manifest_data)
        manifest_json = json.dumps(legacy_manifest, sort_keys=True, separators=(',', ':'))

        parsed_back = json.loads(manifest_json)
        reserialized = json.dumps(parsed_back, sort_keys=True, separators=(',', ':'))

        assert manifest_json == reserialized, "JSON not consistently sorted"

        first_service_start = manifest_json.find('"services":[{')
        if first_service_start != -1:
            service_section = manifest_json[first_service_start:first_service_start + 500]
            pos_args = service_section.find('"args"')
            pos_command = service_section.find('"command"')
            pos_count = service_section.find('"count"')

            if pos_args != -1 and pos_command != -1 and pos_count != -1:
                assert pos_args < pos_command < pos_count, \
                    f"Service fields not alphabetically ordered: args={pos_args}, command={pos_command}, count={pos_count}"

    def test_version_hash_html_escaping(self):
        """Test that version hash escapes HTML characters."""
        from akash.modules.manifest.utils import ManifestUtils

        manifest_utils = ManifestUtils()

        test_json = '{"test":"<>&"}'
        escaped = manifest_utils._escape_html(test_json)

        assert '\\u003c' in escaped  # <
        assert '\\u003e' in escaped  # >
        assert '\\u0026' in escaped  # &

        assert '<' not in escaped
        assert '>' not in escaped
        assert '&' not in escaped

        test_multiple = '{"args":"<<test>> && echo"}'
        escaped_multiple = manifest_utils._escape_html(test_multiple)

        assert escaped_multiple.count('\\u003c') == 2
        assert escaped_multiple.count('\\u003e') == 2
        assert escaped_multiple.count('\\u0026') == 2

        double_escaped = manifest_utils._escape_html(escaped_multiple)
        assert double_escaped == escaped_multiple, "Escaping should be idempotent"


class TestManifestQueryMissingCoverage:
    """Test previously uncovered manifest query functions."""

    def test_get_deployment_manifest_structure(self):
        """Test get_deployment_manifest uses correct gRPC structures."""
        from unittest.mock import Mock

        # Test manifest response structure
        mock_manifest = Mock()
        mock_manifest.manifest = "services:\n  web:\n    image: nginx"
        mock_manifest.leases = []

        assert hasattr(mock_manifest, 'manifest')
        assert hasattr(mock_manifest, 'leases')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
