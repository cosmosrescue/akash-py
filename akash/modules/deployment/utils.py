import hashlib
import json
import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)


class DeploymentUtils:
    """
    Mixin for deployment utilities.
    """

    def _get_storage_size(self, storage_config) -> str:
        """
        Extract storage size from storage config.
        Storage can be either a dict with 'size' key or a list of storage volumes.

        Args:
            storage_config: Storage configuration (dict or list)

        Returns:
            str: Storage size (e.g., "512Mi", "1Gi")

        Raises:
            ValueError: If storage config is invalid or missing required 'size' field
        """
        if isinstance(storage_config, dict):
            if "size" not in storage_config:
                raise ValueError("Storage config missing required 'size' field")
            return storage_config["size"]
        elif isinstance(storage_config, list):
            if not storage_config:
                raise ValueError("Storage config is an empty list")

            for item in storage_config:
                if isinstance(item, dict) and "name" not in item:
                    if "size" not in item:
                        raise ValueError(f"Storage volume missing required 'size' field: {item}")
                    return item["size"]

            if isinstance(storage_config[0], dict):
                if "size" not in storage_config[0]:
                    raise ValueError(f"Storage volume missing required 'size' field: {storage_config[0]}")
                return storage_config[0]["size"]

            raise ValueError(f"Invalid storage config format: {storage_config}")
        else:
            raise ValueError(f"Invalid storage config type: {type(storage_config)}, expected dict or list")

    def _build_storage_volumes(self, storage_config) -> List[Dict]:
        """
        Build storage volumes array from SDL storage config.
        Handles both single storage (dict) and multiple volumes (list).

        Args:
            storage_config: Storage configuration from SDL (dict or list)

        Returns:
            List of storage volume objects with name, size, and attributes
        """
        volumes = []

        if isinstance(storage_config, dict):
            volumes.append({
                "name": "default",
                "size": self._parse_storage_to_bytes(storage_config["size"]),
                "attributes": {}
            })
        elif isinstance(storage_config, list):
            for item in storage_config:
                if not isinstance(item, dict):
                    raise ValueError(f"Storage item must be a dict, got {type(item)}")

                if "size" not in item:
                    raise ValueError(f"Storage volume missing required 'size' field: {item}")

                name = item.get("name", "default")

                size_bytes = self._parse_storage_to_bytes(item["size"])

                attributes = item.get("attributes", {})

                volumes.append({
                    "name": name,
                    "size": size_bytes,
                    "attributes": attributes
                })
        else:
            raise ValueError(f"Storage config must be a dict or list, got {type(storage_config)}")

        return volumes

    def _parse_gpu_config(self, gpu_config: Dict) -> Dict:
        """
        Parse GPU configuration from SDL and return structured GPU data with attributes.

        Args:
            gpu_config: GPU configuration dict from SDL with units and optional attributes

        Returns:
            Dict with 'units' and 'attributes' (empty list if no GPU or attributes)
        """
        GPU_SUPPORTED_VENDORS = ["nvidia", "amd"]
        GPU_SUPPORTED_INTERFACES = ["pcie", "sxm"]

        if not gpu_config:
            return {
                "units": "0",
                "attributes": []
            }

        units = gpu_config.get("units", 0)
        units_int = int(units) if units is not None else 0

        if units_int == 0:
            return {
                "units": "0",
                "attributes": []
            }

        attributes = gpu_config.get("attributes", {})

        if units_int > 0 and not attributes:
            raise ValueError("GPU must have attributes if units is not 0")

        vendor_specs = attributes.get("vendor", {})
        if not vendor_specs:
            raise ValueError("GPU must specify a vendor if units is not 0")

        for vendor in vendor_specs.keys():
            if vendor not in GPU_SUPPORTED_VENDORS:
                raise ValueError(
                    f"Unsupported GPU vendor '{vendor}'. Must be one of: {', '.join(GPU_SUPPORTED_VENDORS)}"
                )

        gpu_attributes = []
        for vendor, models in vendor_specs.items():
            if not models:
                gpu_attributes.append({
                    "key": f"vendor/{vendor}/model/*",
                    "value": "true"
                })
            else:
                for model_spec in models:
                    if isinstance(model_spec, str):
                        gpu_attributes.append({
                            "key": f"vendor/{vendor}/model/{model_spec}",
                            "value": "true"
                        })
                    elif isinstance(model_spec, dict):
                        model_name = model_spec.get("model", "*")
                        key = f"vendor/{vendor}/model/{model_name}"

                        if "ram" in model_spec:
                            key += f"/ram/{model_spec['ram']}"

                        if "interface" in model_spec:
                            interface = model_spec["interface"]
                            if interface not in GPU_SUPPORTED_INTERFACES:
                                raise ValueError(
                                    f"Unsupported GPU interface '{interface}'. Must be one of: {', '.join(GPU_SUPPORTED_INTERFACES)}"
                                )
                            key += f"/interface/{interface}"

                        gpu_attributes.append({
                            "key": key,
                            "value": "true"
                        })

        gpu_attributes.sort(key=lambda x: x["key"])

        return {
            "units": str(units_int),
            "attributes": gpu_attributes
        }

    def _build_gpu_for_deployment(self, gpu_data: Dict) -> Dict:
        """
        Build GPU structure for deployment message.

        Args:
            gpu_data: GPU data dict with 'units' and 'attributes'

        Returns:
            Dict with GPU units and attributes in deployment message format
        """
        if not gpu_data or not isinstance(gpu_data, dict):
            return {
                "units": {"val": "0"},
                "attributes": []
            }

        units = gpu_data.get("units", "0")
        attributes = gpu_data.get("attributes", [])

        return {
            "units": {"val": str(units)},
            "attributes": attributes
        }

    def _safe_decode_bytes(self, bytes_data: bytes) -> str:
        """
        Safely decode bytes to string, handling non-UTF8 data.

        Args:
            bytes_data: Bytes to decode

        Returns:
            str: Decoded string or hex representation if not valid UTF-8
        """
        try:
            return bytes_data.decode("utf-8")
        except UnicodeDecodeError:
            return bytes_data.hex()

    def validate_sdl(self, sdl: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate SDL (Stack Definition Language) structure and contents.

        Args:
            sdl: SDL configuration dictionary

        Returns:
            Dict with validation results and details
        """
        try:
            validation_result = {
                "valid": True,
                "errors": [],
                "warnings": [],
                "details": {},
            }

            required_keys = ["version", "services", "profiles", "deployment"]
            for key in required_keys:
                if key not in sdl:
                    validation_result["valid"] = False
                    validation_result["errors"].append(f"Missing required key: {key}")

            if not validation_result["valid"]:
                return validation_result

            services = sdl.get("services", {})
            if not services:
                validation_result["valid"] = False
                validation_result["errors"].append("No services defined")
                return validation_result

            validation_result["details"]["version"] = sdl["version"]
            validation_result["details"]["services"] = list(services.keys())

            profiles = sdl.get("profiles", {})
            compute_profiles = profiles.get("compute", {})
            placement_profiles = profiles.get("placement", {})

            resources_info = {}
            for service_name, profile in compute_profiles.items():
                resources = profile.get("resources", {})
                storage_config = resources.get("storage", {})
                resources_info[service_name] = {
                    "cpu": resources.get("cpu", {}).get("units", "N/A"),
                    "memory": resources.get("memory", {}).get("size", "N/A"),
                    "storage": self._get_storage_size(storage_config),
                }

                cpu_units = resources.get("cpu", {}).get("units", "0")
                memory_size = resources.get("memory", {}).get("size", "0Mi")

                try:
                    cpu_value = float(cpu_units)
                    if cpu_value < 0.1:
                        validation_result["warnings"].append(
                            f"Service '{service_name}': CPU allocation might be too low ({cpu_units})"
                        )
                except (ValueError, TypeError):
                    validation_result["warnings"].append(
                        f"Service '{service_name}': Invalid CPU units format"
                    )

                if "Mi" in memory_size or "Gi" in memory_size:
                    try:
                        memory_value = int(
                            memory_size.replace("Mi", "").replace("Gi", "")
                        )
                        if "Mi" in memory_size and memory_value < 128:
                            validation_result["warnings"].append(
                                f"Service '{service_name}': Memory allocation might be too low ({memory_size})"
                            )
                    except (ValueError, TypeError):
                        validation_result["warnings"].append(
                            f"Service '{service_name}': Invalid memory size format"
                        )

            validation_result["details"]["resources"] = resources_info

            pricing_info = {}
            for placement_name, profile in placement_profiles.items():
                pricing = profile.get("pricing", {})
                pricing_info[placement_name] = {}

                for service, price in pricing.items():
                    amount = price.get("amount", "N/A")
                    denom = price.get("denom", "N/A")
                    pricing_info[placement_name][service] = f"{amount} {denom}"

                    try:
                        price_value = int(amount)
                        if price_value < 10:
                            validation_result["warnings"].append(
                                f"Service '{service}': Price might be too low ({amount} {denom}/block)"
                            )
                    except (ValueError, TypeError):
                        validation_result["warnings"].append(
                            f"Service '{service}': Invalid price format"
                        )

            validation_result["details"]["pricing"] = pricing_info

            deployment_config = sdl.get("deployment", {})
            deployment_info = {}
            for service_name, placement_config in deployment_config.items():
                if service_name not in services:
                    validation_result["errors"].append(
                        f"Deployment references undefined service: {service_name}"
                    )
                    validation_result["valid"] = False

                deployment_info[service_name] = placement_config

            validation_result["details"]["deployment"] = deployment_info

            logger.info(
                f"SDL validation completed: {'valid' if validation_result['valid'] else 'invalid'}"
            )
            return validation_result

        except Exception as e:
            logger.error(f"SDL validation error: {e}")
            return {
                "valid": False,
                "errors": [f"Validation error: {str(e)}"],
                "warnings": [],
                "details": {},
            }

    def generate_sdl_version(self, sdl: Dict[str, Any]) -> bytes:
        """
        Generate version hash from SDL content.

        Creates a SHA256 hash from the canonically sorted JSON representation
        of the SDL configuration for deployment version identification.

        Args:
            sdl: SDL configuration dictionary

        Returns:
            bytes: SHA256 hash of the SDL content
        """
        try:
            sdl_json = json.dumps(sdl, sort_keys=True, separators=(",", ":"))

            hash_obj = hashlib.sha256(sdl_json.encode("utf-8"))
            return hash_obj.digest()

        except Exception as e:
            logger.error(f"Failed to generate SDL version hash: {e}")
            raise ValueError(f"Could not generate version from SDL: {e}")

    def sdl_to_groups(self, sdl: Dict[str, Any]) -> list:
        """
        Convert SDL to deployment groups format expected by create_deployment.

        Args:
            sdl: SDL configuration dictionary

        Returns:
            list: List of group specifications
        """
        try:
            groups = []
            services = sdl.get("services", {})
            compute_profiles = sdl.get("profiles", {}).get("compute", {})
            placement_profiles = sdl.get("profiles", {}).get("placement", {})
            deployment_config = sdl.get("deployment", {})

            for service_name, deployment_info in deployment_config.items():
                if service_name not in services:
                    continue

                service = services[service_name]

                for placement_name, placement_config in deployment_info.items():
                    if placement_name not in placement_profiles:
                        continue

                    placement_profile = placement_profiles[placement_name]

                    if service_name not in compute_profiles:
                        continue

                    compute_profile = compute_profiles[service_name]
                    resources_config = compute_profile.get("resources", {})

                    pricing = placement_profile.get("pricing", {}).get(service_name, {})

                    group = {
                        "name": f"{service_name}-{placement_name}",
                        "resources": [
                            {
                                "cpu": self._parse_cpu_units(
                                    resources_config.get("cpu", {}).get("units")
                                ),
                                "memory": self._parse_memory_size(
                                    resources_config.get("memory", {}).get("size")
                                ),
                                "storage": self._parse_storage_size(
                                    self._get_storage_size(resources_config.get("storage", {}))
                                ),
                                "price": pricing.get("amount"),
                                "count": placement_config.get("count"),
                            }
                        ],
                    }

                    groups.append(group)

            return groups

        except Exception as e:
            logger.error(f"Failed to convert SDL to groups: {e}")
            raise ValueError(f"Could not convert SDL to deployment groups: {e}")

    def _parse_cpu_units(self, cpu_str: str) -> str:
        """Convert CPU specification to nanocpus.

        Args:
            cpu_str: CPU specification string (e.g., "0.5" for half a CPU)

        Returns:
            str: CPU units in nanocpus

        Raises:
            ValueError: If cpu_str is invalid or cannot be parsed
        """
        try:
            if isinstance(cpu_str, str):
                cpu_value = float(cpu_str)
            else:
                cpu_value = float(cpu_str)

            nanocpus = int(cpu_value * 1_000_000_000)
            return str(nanocpus)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid CPU units specification: {cpu_str!r}") from e

    def _parse_memory_size(self, memory_str: str) -> str:
        """Convert memory specification to bytes.

        Args:
            memory_str: Memory specification string (e.g., "512Mi", "2Gi")

        Returns:
            str: Memory size in bytes

        Raises:
            ValueError: If memory_str is invalid or cannot be parsed
        """
        try:
            if "Mi" in memory_str:
                value = int(memory_str.replace("Mi", ""))
                return str(value * 1024 * 1024)
            elif "Gi" in memory_str:
                value = int(memory_str.replace("Gi", ""))
                return str(value * 1024 * 1024 * 1024)
            else:
                return str(int(memory_str))
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid memory size specification: {memory_str!r}") from e

    def _parse_storage_size(self, storage_str: str) -> str:
        """Convert storage specification to bytes.

        Args:
            storage_str: Storage specification string (e.g., "10Gi", "500Mi")

        Returns:
            str: Storage size in bytes

        Raises:
            ValueError: If storage_str is invalid or cannot be parsed
        """
        try:
            if "Gi" in storage_str:
                value = int(storage_str.replace("Gi", ""))
                return str(value * 1024 * 1024 * 1024)
            elif "Mi" in storage_str:
                value = int(storage_str.replace("Mi", ""))
                return str(value * 1024 * 1024)
            else:
                return str(int(storage_str))
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid storage size specification: {storage_str!r}") from e

    def _group_spec_to_dict(self, group_data: dict) -> dict:
        """
        Convert group data to dictionary format for message encoding.

        Args:
            group_data: Group specification data with required fields:
                - name: Group name (required)
                - resources: List of resource specifications (required)

        Returns:
            dict: Group specification dictionary

        Raises:
            ValueError: If required fields are missing
        """
        if "name" not in group_data:
            raise ValueError("Group name is required")

        if "resources" not in group_data or not group_data["resources"]:
            raise ValueError("At least one resource specification is required")

        resources = []
        for i, resource_data in enumerate(group_data["resources"]):
            if "cpu" not in resource_data:
                raise ValueError(f"CPU specification required for resource {i}")
            if "memory" not in resource_data:
                raise ValueError(f"Memory specification required for resource {i}")
            if "storage" not in resource_data:
                raise ValueError(f"Storage specification required for resource {i}")
            if "price" not in resource_data:
                raise ValueError(f"Price specification required for resource {i}")

            storage_specs = []
            if isinstance(resource_data["storage"], list):
                for storage in resource_data["storage"]:
                    if "name" not in storage or "size" not in storage:
                        raise ValueError("Storage must have 'name' and 'size' fields")

                    attributes_list = []
                    if "attributes" in storage and isinstance(storage["attributes"], dict):
                        attrs = storage["attributes"]

                        if attrs.get("class") == "ram" and "persistent" not in attrs:
                            attrs = dict(attrs)
                            attrs["persistent"] = "false"

                        for key, value in attrs.items():
                            attributes_list.append({
                                "key": key,
                                "value": str(value).lower() if isinstance(value, bool) else str(value)
                            })

                        attributes_list.sort(key=lambda x: x["key"])

                    storage_specs.append(
                        {
                            "name": storage["name"],
                            "quantity": {"val": str(storage["size"])},
                            "attributes": attributes_list
                        }
                    )
            else:
                storage_specs.append(
                    {
                        "name": "default",
                        "quantity": {"val": str(resource_data["storage"])},
                        "attributes": []
                    }
                )

            # Convert to actual uAKT amount
            price_amount = int(resource_data["price"]) * (10 ** 18)

            endpoints_specs = []
            if "endpoints" in resource_data:
                for endpoint in resource_data["endpoints"]:
                    kind = endpoint.get("kind", 0)
                    endpoint_spec = {
                        "kind": kind,
                        "sequence_number": endpoint.get("sequence_number", 0)
                    }
                    endpoints_specs.append(endpoint_spec)

            resource_spec = {
                "resource": {
                    "id": i + 1,
                    "cpu": {
                        "units": {"val": str(resource_data["cpu"])},
                        "attributes": []
                    },
                    "memory": {
                        "quantity": {"val": str(resource_data["memory"])},
                        "attributes": []
                    },
                    "storage": storage_specs,
                    "gpu": self._build_gpu_for_deployment(resource_data.get("gpu", {})),
                },
                "count": resource_data.get("count", 1),
                "price": {
                    "denom": resource_data.get("price_denom", "uakt"),
                    "amount": str(price_amount),
                },
            }

            if endpoints_specs:
                resource_spec["resource"]["endpoints"] = endpoints_specs
            resources.append(resource_spec)

        return {
            "name": group_data["name"],
            "requirements": group_data.get(
                "requirements", {"signed_by": {}, "attributes": []}
            ),
            "resources": resources,
        }

    def _close_deployment_msg(self, owner: str, dseq: int) -> dict:
        """
        Create MsgCloseDeployment message dictionary.

        Args:
            owner: Deployment owner address
            dseq: Deployment sequence number

        Returns:
            dict: Message dictionary for MsgCloseDeployment
        """
        return {
            "@type": "/akash.deployment.v1beta4.MsgCloseDeployment",
            "id": {"owner": owner, "dseq": str(dseq)},
        }

    def _deposit_deployment_msg(
        self, owner: str, dseq: int, amount: str, denom: str, depositor: str
    ) -> dict:
        """
        Create MsgDepositDeployment message dictionary.

        Args:
            owner: Deployment owner address
            dseq: Deployment sequence number
            amount: Deposit amount
            denom: Token denomination
            depositor: Address making deposit

        Returns:
            dict: Message dictionary for MsgDepositDeployment
        """
        return {
            "@type": "/akash.deployment.v1beta4.MsgDepositDeployment",
            "id": {"owner": owner, "dseq": str(dseq)},
            "amount": {"denom": denom, "amount": amount},
            "depositor": depositor,
        }

    def _close_group_msg(self, owner: str, dseq: int, gseq: int) -> dict:
        """
        Create MsgCloseGroup message dictionary.

        Args:
            owner: Deployment owner address
            dseq: Deployment sequence number
            gseq: Group sequence number

        Returns:
            dict: Message dictionary for MsgCloseGroup
        """
        return {
            "@type": "/akash.deployment.v1beta4.MsgCloseGroup",
            "id": {"owner": owner, "dseq": str(dseq), "gseq": gseq},
        }

    def _pause_group_msg(self, owner: str, dseq: int, gseq: int) -> dict:
        """
        Create MsgPauseGroup message dictionary.

        Args:
            owner: Deployment owner address
            dseq: Deployment sequence number
            gseq: Group sequence number

        Returns:
            dict: Message dictionary for MsgPauseGroup
        """
        return {
            "@type": "/akash.deployment.v1beta4.MsgPauseGroup",
            "id": {"owner": owner, "dseq": str(dseq), "gseq": gseq},
        }

    def _start_group_msg(self, owner: str, dseq: int, gseq: int) -> dict:
        """
        Create MsgStartGroup message dictionary.

        Args:
            owner: Deployment owner address
            dseq: Deployment sequence number
            gseq: Group sequence number

        Returns:
            dict: Message dictionary for MsgStartGroup
        """
        return {
            "@type": "/akash.deployment.v1beta4.MsgStartGroup",
            "id": {"owner": owner, "dseq": str(dseq), "gseq": gseq},
        }

    def create_group_spec(self, name: str, requirements: dict, resources: list) -> dict:
        """
        Create a group specification dictionary with proper resource definitions.

        Args:
            name: Group name
            requirements: Placement requirements and attributes
            resources: List of resource specifications

        Returns:
            dict: Group specification dictionary
        """
        return {"name": name, "requirements": requirements, "resources": resources}

    def get_service_logs(
        self,
        provider_endpoint: str,
        lease_id: Dict[str, Any],
        service_name: Optional[str] = None,
        tail: int = 100,
        cert_pem: Optional[str] = None,
        key_pem: Optional[str] = None,
        timeout: int = 30,
    ) -> list:
        """
        Get logs from a service running in a deployment.

        This method retrieves logs from services running in a deployment through the
        provider's WebSocket API. It requires an active lease with the provider and
        valid mTLS certificates.

        Args:
            provider_endpoint: Provider's HTTPS endpoint (e.g., "provider.akash.network:8443")
            lease_id: Lease identifier dictionary with keys: owner, dseq, gseq, oseq, provider
            service_name: Specific service name to get logs from (None for all services)
            tail: Number of recent log lines to retrieve
            cert_pem: Client certificate in PEM format for mTLS authentication
            key_pem: Client private key in PEM format for mTLS authentication
            timeout: WebSocket timeout in seconds

        Returns:
            List of log lines from the service(s)
        """
        try:
            import websocket
            import ssl
            import tempfile
            import os
            import json
            import time
            import threading

            logger.info(
                f"Getting logs from {provider_endpoint} for service '{service_name or 'all'}'"
            )

            if not provider_endpoint or not provider_endpoint.strip():
                raise ValueError("Provider endpoint cannot be empty")

            if not lease_id:
                raise ValueError("Lease ID cannot be empty")

            required_fields = ["owner", "dseq", "gseq", "oseq", "provider"]
            for field in required_fields:
                if not lease_id.get(field):
                    raise ValueError(f"Missing required field: lease_id.{field}")

            dseq = lease_id.get("dseq")
            gseq = lease_id.get("gseq")
            oseq = lease_id.get("oseq")

            if provider_endpoint.startswith("https://"):
                ws_endpoint = provider_endpoint.replace("https://", "wss://")
            elif provider_endpoint.startswith("http://"):
                ws_endpoint = provider_endpoint.replace("http://", "ws://")
            elif not provider_endpoint.startswith(("ws://", "wss://")):
                ws_endpoint = f"wss://{provider_endpoint}"
            else:
                ws_endpoint = provider_endpoint

            url = (
                f"{ws_endpoint}/lease/{dseq}/{gseq}/{oseq}/logs?follow=true&tail={tail}"
            )

            if service_name:
                url += f"&service={service_name}"

            if not cert_pem or not key_pem:
                owner = lease_id.get("owner")
                if (
                    hasattr(self.akash_client, "_certificate_store")
                    and owner in self.akash_client._certificate_store
                ):
                    cert_info = self.akash_client._certificate_store[owner]
                    cert_pem = cert_info["certificate_pem"]
                    key_pem = cert_info["private_key_pem"]
                    logger.info("Using certificates from client store")
                else:
                    raise ValueError(
                        "mTLS certificates required - either provide cert_pem/key_pem or create certificate first"
                    )

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".pem", delete=False
            ) as cert_file:
                cert_file.write(cert_pem)
                cert_path = cert_file.name

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".pem", delete=False
            ) as key_file:
                key_file.write(key_pem)
                key_path = key_file.name

            logs = []
            error_occurred = None
            connection_opened = False

            def on_open(ws):
                nonlocal connection_opened
                connection_opened = True
                logger.info("WebSocket connection opened")

            def on_message(ws, message):
                try:
                    log_entry = json.loads(message)

                    if "message" in log_entry:
                        logs.append(log_entry["message"])
                    else:
                        logs.append(str(log_entry))

                except json.JSONDecodeError:
                    logs.append(message)

            def on_error(ws, error):
                nonlocal error_occurred
                error_occurred = error
                logger.error(f"WebSocket error: {error}")

            def on_close(ws, close_status_code, close_msg):
                logger.info(f"WebSocket closed: {close_status_code} - {close_msg}")

            try:
                ssl_context = ssl.create_default_context()
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE
                ssl_context.load_cert_chain(cert_path, key_path)

                logger.info("Connecting to WebSocket...")

                ws = websocket.WebSocketApp(
                    url,
                    on_open=on_open,
                    on_message=on_message,
                    on_error=on_error,
                    on_close=on_close,
                )

                def run_with_timeout():
                    ws.run_forever(sslopt={"context": ssl_context})

                ws_thread = threading.Thread(target=run_with_timeout)
                ws_thread.daemon = True
                ws_thread.start()

                for i in range(10):  # 10 seconds to connect
                    if connection_opened or error_occurred:
                        break
                    time.sleep(1)

                if error_occurred:
                    raise Exception(f"Connection failed: {error_occurred}")

                if not connection_opened:
                    raise Exception("Connection timeout")

                logger.info("Waiting for logs...")
                time.sleep(timeout if timeout > 0 else 10)

                ws.close()

                logger.info(f"Retrieved {len(logs)} log lines")
                return logs

            finally:
                try:
                    os.unlink(cert_path)
                    os.unlink(key_path)
                except BaseException:
                    pass

        except Exception as e:
            logger.error(f"Error getting service logs: {e}")
            raise

    def stream_service_logs(
        self,
        provider_endpoint: str,
        lease_id: Dict[str, Any],
        service_name: Optional[str] = None,
        follow: bool = True,
        cert_pem: Optional[str] = None,
        key_pem: Optional[str] = None,
        timeout: int = 300,
    ):
        """
        Stream logs from a service running in a deployment in real-time.

        This method establishes a WebSocket streaming connection to the provider's endpoint
        and yields log lines as they are generated. Similar to 'kubectl logs -f'.

        Args:
            provider_endpoint: Provider's HTTPS endpoint (e.g., "provider.akash.network:8443")
            lease_id: Lease identifier dictionary with keys: owner, dseq, gseq, oseq, provider
            service_name: Specific service name to stream logs from (None for all services)
            follow: Whether to keep streaming new logs (like tail -f)
            cert_pem: Client certificate in PEM format for mTLS authentication
            key_pem: Client private key in PEM format for mTLS authentication
            timeout: WebSocket streaming timeout in seconds

        Yields:
            Log lines as they are received from the service
        """
        try:
            import websocket
            import ssl
            import tempfile
            import os
            import json
            import time
            import threading
            import queue

            logger.info(
                f"Starting log stream from {provider_endpoint} for service '{service_name or 'all'}'"
            )

            if not provider_endpoint or not provider_endpoint.strip():
                raise ValueError("Provider endpoint cannot be empty")

            if not lease_id:
                raise ValueError("Lease ID cannot be empty")

            required_fields = ["owner", "dseq", "gseq", "oseq", "provider"]
            for field in required_fields:
                if not lease_id.get(field):
                    raise ValueError(f"Missing required field: lease_id.{field}")

            dseq = lease_id.get("dseq")
            gseq = lease_id.get("gseq")
            oseq = lease_id.get("oseq")

            if provider_endpoint.startswith("https://"):
                ws_endpoint = provider_endpoint.replace("https://", "wss://")
            elif provider_endpoint.startswith("http://"):
                ws_endpoint = provider_endpoint.replace("http://", "ws://")
            elif not provider_endpoint.startswith(("ws://", "wss://")):
                ws_endpoint = f"wss://{provider_endpoint}"
            else:
                ws_endpoint = provider_endpoint

            url = f"{ws_endpoint}/lease/{dseq}/{gseq}/{oseq}/logs?follow={'true' if follow else 'false'}&tail=0"

            if service_name:
                url += f"&service={service_name}"

            if not cert_pem or not key_pem:
                owner = lease_id.get("owner")
                if (
                    hasattr(self.akash_client, "_certificate_store")
                    and owner in self.akash_client._certificate_store
                ):
                    cert_info = self.akash_client._certificate_store[owner]
                    cert_pem = cert_info["certificate_pem"]
                    key_pem = cert_info["private_key_pem"]
                    logger.info("Using certificates from client store")
                else:
                    raise ValueError(
                        "mTLS certificates required - either provide cert_pem/key_pem or create certificate first"
                    )

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".pem", delete=False
            ) as cert_file:
                cert_file.write(cert_pem)
                cert_path = cert_file.name

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".pem", delete=False
            ) as key_file:
                key_file.write(key_pem)
                key_path = key_file.name

            log_queue = queue.Queue()
            error_occurred = None
            connection_opened = False
            ws_connection = None

            def on_open(ws):
                nonlocal connection_opened, ws_connection
                connection_opened = True
                ws_connection = ws
                logger.info("WebSocket log stream opened")

            def on_message(ws, message):
                try:
                    log_entry = json.loads(message)

                    if "message" in log_entry:
                        log_queue.put(log_entry["message"])
                    else:
                        log_queue.put(str(log_entry))

                except json.JSONDecodeError:
                    log_queue.put(message)

            def on_error(ws, error):
                nonlocal error_occurred
                error_occurred = error
                logger.error(f"WebSocket stream error: {error}")
                log_queue.put(None)

            def on_close(ws, close_status_code, close_msg):
                logger.info(
                    f"WebSocket stream closed: {close_status_code} - {close_msg}"
                )
                log_queue.put(None)

            try:
                ssl_context = ssl.create_default_context()
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE
                ssl_context.load_cert_chain(cert_path, key_path)

                logger.info("Connecting to WebSocket for streaming...")

                ws = websocket.WebSocketApp(
                    url,
                    on_open=on_open,
                    on_message=on_message,
                    on_error=on_error,
                    on_close=on_close,
                )

                def run_websocket():
                    ws.run_forever(sslopt={"context": ssl_context})

                ws_thread = threading.Thread(target=run_websocket)
                ws_thread.daemon = True
                ws_thread.start()

                for i in range(10):  # 10 seconds to connect
                    if connection_opened or error_occurred:
                        break
                    time.sleep(1)

                if error_occurred:
                    raise Exception(f"Stream connection failed: {error_occurred}")

                if not connection_opened:
                    raise Exception("Stream connection timeout")

                logger.info("Log stream established, yielding logs...")

                start_time = time.time()
                while True:
                    try:
                        if timeout > 0 and (time.time() - start_time) > timeout:
                            logger.info("Stream timeout reached")
                            break

                        log_line = log_queue.get(timeout=1)

                        if log_line is None:
                            break

                        yield log_line

                    except queue.Empty:
                        if not ws_thread.is_alive():
                            break
                        continue

                if ws_connection:
                    ws_connection.close()

            finally:
                try:
                    os.unlink(cert_path)
                    os.unlink(key_path)
                except BaseException:
                    pass

        except Exception as e:
            logger.error(f"Error setting up log stream: {e}")
            raise

    def _create_groups_from_sdl(self, sdl_data: Dict) -> List[Dict]:
        """
        Create deployment groups from SDL with automatic endpoint detection.

        Args:
            sdl_data: Parsed SDL YAML data

        Returns:
            List of deployment group dictionaries
        """
        groups = []

        deployment_config = sdl_data.get("deployment", {})
        profiles = sdl_data.get("profiles", {})
        services = sdl_data.get("services", {})

        endpoint_sequence_numbers = self._compute_endpoint_sequence_numbers(sdl_data)

        for deployment_name, deployment_spec in deployment_config.items():
            for placement_name, placement_spec in deployment_spec.items():
                profile_name = placement_spec.get("profile")
                if not profile_name:
                    continue

                compute_profile = profiles.get("compute", {}).get(profile_name, {})
                if not compute_profile:
                    continue

                placement_profile = profiles.get("placement", {}).get(placement_name, {})
                pricing = placement_profile.get("pricing", {}).get(profile_name, {})

                service_def = services.get(profile_name, {})
                expose_list = service_def.get("expose", [])

                resources = compute_profile.get("resources", {})
                storage_config = resources.get("storage", {})
                gpu_config = resources.get("gpu", {})

                group_resource = {
                    'cpu': self._parse_cpu_to_millis(resources.get("cpu", {}).get("units")),
                    'memory': self._parse_memory_to_bytes(resources.get("memory", {}).get("size")),
                    'storage': self._build_storage_volumes(storage_config),
                    'gpu': self._parse_gpu_config(gpu_config),
                    'price': pricing.get("amount"),
                    'price_denom': pricing.get("denom", "uakt"),
                    'count': placement_spec.get("count")
                }

                group_resource['endpoints'] = self._build_endpoints_from_expose(expose_list, endpoint_sequence_numbers)

                requirements_attrs = []
                if "attributes" in placement_profile:
                    for key, value in placement_profile["attributes"].items():
                        requirements_attrs.append({
                            "key": key,
                            "value": str(value)
                        })
                    requirements_attrs.sort(key=lambda x: x["key"])

                groups.append({
                    'name': placement_name,
                    'requirements': {
                        'signed_by': {
                            'all_of': [],
                            'any_of': []
                        },
                        'attributes': requirements_attrs
                    },
                    'resources': [group_resource]
                })

        if not groups:
            raise ValueError("No deployment groups could be created from SDL - check SDL format")

        return groups

    def _has_global_endpoints(self, expose_list: list) -> bool:
        """Check if service has global endpoints."""
        for expose in expose_list:
            if "to" in expose:
                for to_config in expose["to"]:
                    if isinstance(to_config, dict) and to_config.get("global"):
                        return True
        return False

    def _compute_endpoint_sequence_numbers(self, sdl_data: Dict) -> Dict[str, int]:
        """
        Compute sequence numbers for IP endpoints.

        Returns a dict mapping IP endpoint names to their sequence numbers (starting from 1).
        """
        ip_names = set()
        services = sdl_data.get("services", {})

        for service_name, service_def in services.items():
            expose_list = service_def.get("expose", [])
            for expose in expose_list:
                to_configs = expose.get("to", [])
                for to_config in to_configs:
                    if isinstance(to_config, dict) and to_config.get("global") and to_config.get("ip"):
                        ip_names.add(to_config["ip"])

        sorted_ips = sorted(ip_names)
        return {ip_name: idx + 1 for idx, ip_name in enumerate(sorted_ips)}

    def _build_endpoints_from_expose(self, expose_list: list, endpoint_sequence_numbers: dict = None) -> list:
        """
        Build endpoints array from expose configuration.

        Endpoint kinds:
        - 0 (SHARED_HTTP): TCP on port 80 with global
        - 1 (RANDOM_PORT): Other protocols/ports with global
        - 2 (LEASED_IP): IP endpoints

        Args:
            expose_list: List of expose configurations from SDL
            endpoint_sequence_numbers: Dict mapping IP endpoint names to sequence numbers
        """
        endpoints = []
        if endpoint_sequence_numbers is None:
            endpoint_sequence_numbers = {}

        for expose in expose_list:
            if "to" not in expose:
                continue

            port = expose.get("port", 0)
            external_port = expose.get("as", 0)
            proto = expose.get("proto", "tcp").upper()

            actual_external_port = external_port if external_port != 0 else port

            for to_config in expose["to"]:
                if not isinstance(to_config, dict):
                    continue

                if not to_config.get("global"):
                    continue

                is_ingress = proto == "TCP" and actual_external_port == 80

                if is_ingress:
                    endpoint = {"sequence_number": 0}
                else:
                    endpoint = {"kind": 1, "sequence_number": 0}

                endpoints.append(endpoint)

                if to_config.get("ip"):
                    ip_name = to_config["ip"]
                    sequence_number = endpoint_sequence_numbers.get(ip_name, 0)
                    endpoints.append({"kind": 2, "sequence_number": sequence_number})

        return endpoints

    def _parse_cpu_to_millis(self, cpu_value) -> str:
        """Convert CPU value to millicpu string."""
        if isinstance(cpu_value, str):
            if cpu_value.endswith("m"):
                return cpu_value[:-1]
            else:
                return str(int(float(cpu_value) * 1000))
        elif isinstance(cpu_value, (int, float)):
            return str(int(cpu_value * 1000))
        raise ValueError(f"Invalid CPU value: {cpu_value}. Expected string with 'm' suffix or numeric value.")

    def _parse_memory_to_bytes(self, memory_value: str) -> str:
        """Convert memory value to bytes string."""
        try:
            if memory_value.endswith("Gi"):
                return str(int(memory_value[:-2]) * 1024 * 1024 * 1024)
            elif memory_value.endswith("Mi"):
                return str(int(memory_value[:-2]) * 1024 * 1024)
            elif memory_value.endswith("Ki"):
                return str(int(memory_value[:-2]) * 1024)
            else:
                return str(int(memory_value))
        except:
            raise ValueError(f"Invalid memory value: {memory_value}. Expected format like '128Mi', '2Gi', '512Ki'.")

    def _parse_storage_to_bytes(self, storage_value: str) -> str:
        """Convert storage value to bytes string."""
        try:
            if storage_value.endswith("Gi"):
                return str(int(storage_value[:-2]) * 1024 * 1024 * 1024)
            elif storage_value.endswith("Mi"):
                return str(int(storage_value[:-2]) * 1024 * 1024)
            elif storage_value.endswith("Ki"):
                return str(int(storage_value[:-2]) * 1024)
            else:
                return str(int(storage_value))
        except:
            raise ValueError(f"Invalid storage value: {storage_value}. Expected format like '512Mi', '2Gi', '1Ti'.")

    def submit_manifest_to_provider(
        self,
        provider_endpoint: str,
        lease_id: Dict[str, Any],
        manifest: Dict[str, Any],
        cert_pem: Optional[str] = None,
        key_pem: Optional[str] = None,
        timeout: int = 60,
        use_http: bool = False,
    ) -> Dict[str, Any]:
        """
        Submit manifest to provider with automatic fallback.

        This is a convenience method that provides access to manifest submission from the
        deployment module, using either gRPC or HTTP based on provider compatibility.

        Args:
            provider_endpoint: Provider's endpoint
            lease_id: Lease identifier dictionary
            manifest: Manifest data as dictionary
            cert_pem: Client certificate in PEM format (optional)
            key_pem: Client private key in PEM format (optional)
            timeout: Request timeout in seconds
            use_http: Force HTTP method instead of trying gRPC first

        Returns:
            Dict with submission status and details
        """
        try:
            if not cert_pem or not key_pem:
                owner = lease_id.get("owner")
                if (
                    hasattr(self.akash_client, "_certificate_store")
                    and owner in self.akash_client._certificate_store
                ):
                    cert_info = self.akash_client._certificate_store[owner]
                    cert_pem = cert_info["certificate_pem"]
                    key_pem = cert_info["private_key_pem"]
                    logger.info(
                        "Using certificates from client store for manifest submission"
                    )

            if isinstance(manifest, dict) and 'version' in manifest:
                import yaml
                sdl_content = yaml.dump(manifest)
            else:
                import yaml
                sdl_content = yaml.dump({
                    'version': '2.0',
                    'services': manifest.get('services', {}),
                    'profiles': manifest.get('profiles', {}),
                    'deployment': manifest.get('deployment', {})
                })

            return self.akash_client.manifest.submit_manifest(
                provider_endpoint=provider_endpoint,
                lease_id=lease_id,
                sdl_content=sdl_content,
                cert_pem=cert_pem,
                key_pem=key_pem,
                timeout=timeout
            )

        except Exception as e:
            logger.error(f"Failed to submit manifest to provider: {e}")
            return {"status": "error", "error": str(e), "provider": provider_endpoint}
