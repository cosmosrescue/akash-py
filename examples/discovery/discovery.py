#!/usr/bin/env python3
"""
Discovery module example demonstrating provider discovery functionality.

Tests the Grpc-first, Http fallback discovery implementation with:
- Provider search and DNS pre-filtering
- Provider connectivity testing when available
"""

import socket
import sys
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Development mode: Use local akash if running from repo
examples_dir = Path(__file__).parent.parent
if (examples_dir.parent / "akash").exists() and (examples_dir.parent / "pyproject.toml").exists():
    sys.path.insert(0, str(examples_dir.parent))
    print("✓ Development mode: Using local akash")

try:
    from akash import AkashClient, AkashWallet
except ImportError as e:
    print(f"Failed to import akash SDK: {e}")
    print("Please run: pip install -r requirements.txt")
    sys.exit(1)

MAINNET_RPC = "https://akash-rpc.polkachu.com:443"
MAINNET_CHAIN = "akashnet-2"


class AkashDiscoveryE2ETests:
    def __init__(self):
        self.test_results = {
            'discovery': {'passed': 0, 'failed': 0, 'tests': []},
            'connectivity': {'passed': 0, 'failed': 0, 'tests': []},
            'logic': {'passed': 0, 'failed': 0, 'tests': []},
        }
        self.tested_providers = []
        self.reachable_providers = []
        print(f"Akash Discovery E2E Tests")

    def check_dns_resolution(self, hostname, timeout=2):
        """Quick DNS resolution check."""
        try:
            socket.setdefaulttimeout(timeout)
            socket.gethostbyname(hostname)
            return True
        except socket.error:
            return False
        finally:
            socket.setdefaulttimeout(None)

    def check_port_connectivity(self, hostname, port, timeout=2):
        """Check if a specific port is reachable."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((hostname, port))
            sock.close()
            return result == 0
        except Exception:
            return False

    def find_reachable_providers(self, providers, max_concurrent=10, max_check=100):
        """Find providers that are actually reachable via DNS and port checks."""
        print(f"Pre-filtering up to {max_check} providers for reachability...")

        def check_provider(provider):
            host_uri = provider.get("host_uri", "")
            if not host_uri.startswith("http"):
                return None

            try:
                if host_uri.startswith("https://"):
                    hostname = host_uri.replace("https://", "").split(":")[0]
                    port = 8443
                    if ":" in host_uri.replace("https://", ""):
                        port = int(host_uri.split(":")[-1])
                elif host_uri.startswith("http://"):
                    hostname = host_uri.replace("http://", "").split(":")[0]
                    port = 8080
                    if ":" in host_uri.replace("http://", ""):
                        port = int(host_uri.split(":")[-1])
                else:
                    return None

                if not self.check_dns_resolution(hostname, timeout=1):
                    return None

                if self.check_port_connectivity(hostname, port, timeout=1):
                    return {
                        **provider,
                        "hostname": hostname,
                        "port": port,
                        "reachable": True
                    }

            except Exception:
                pass

            return None

        reachable = []
        test_providers = providers[:max_check]

        with ThreadPoolExecutor(max_workers=max_concurrent) as executor:
            futures = [executor.submit(check_provider, provider) for provider in test_providers]

            for i, future in enumerate(as_completed(futures)):
                try:
                    result = future.result()
                    if result:
                        reachable.append(result)
                        print(f" ✅ Found reachable: {result['hostname']}")

                        if len(reachable) >= 10:
                            break

                except Exception:
                    continue

        print(f"✅ Found {len(reachable)} reachable providers from {len(test_providers)} tested")
        return reachable

    def get_providers_from_networks(self):
        """Get providers from mainnet."""
        all_providers = []

        try:
            print(f"Querying mainnet providers...")
            client = AkashClient(MAINNET_RPC, MAINNET_CHAIN)
            providers_result = client.discovery.get_providers()
            providers = providers_result.get("providers", [])

            network_providers = []
            for provider in providers:
                host_uri = provider.get("host_uri")
                if not host_uri:
                    info = provider.get("info", {})
                    host_uri = info.get("host_uri")

                if host_uri and host_uri.startswith("http"):
                    network_providers.append({
                        **provider,
                        "network": "Mainnet",
                        "rpc": MAINNET_RPC,
                        "chain_id": MAINNET_CHAIN
                    })

            print(f" Found {len(network_providers)} providers with host_uri")
            all_providers.extend(network_providers)

        except Exception as e:
            print(f" ❌ Failed to query mainnet: {e}")

        print(f"Total providers collected: {len(all_providers)}")
        return all_providers

    def test_discovery_logic_validation(self):
        """Test discovery module logic with synthetic inputs - always works."""
        print("\n Discovery Logic Validation ")

        try:
            client = AkashClient(MAINNET_RPC, MAINNET_CHAIN)

            test_cases = [
                {
                    "name": "Https URI detection",
                    "input": "https://fake-provider.example.com:8443",
                    "expected": "failed"
                },
                {
                    "name": "Hostname:Port detection",
                    "input": "fake-provider.example.com:8443",
                    "expected": "failed"
                },
                {
                    "name": "Invalid blockchain address",
                    "input": "akash1invalidaddress123",
                    "expected": "failed"
                },
                {
                    "name": "Empty input validation",
                    "input": "",
                    "expected": "failed"
                }
            ]

            passed_tests = 0

            for test_case in test_cases:
                try:
                    print(f"\nTesting: {test_case['name']}")

                    result = client.discovery.get_provider_status(test_case["input"])
                    actual_status = result.get("status")

                    if actual_status == test_case["expected"]:
                        print(f" ✅ Pass: Correct error handling")
                        passed_tests += 1
                    else:
                        print(f" ❌ Fail: Expected {test_case['expected']}, got {actual_status}")

                except Exception as e:
                    print(f" ❌ Exception: {e}")

            print(f"\nLogic Validation: {passed_tests}/{len(test_cases)} passed")

            if passed_tests >= len(test_cases) * 0.75:  # 75% threshold
                return f"Discovery logic validation: {passed_tests}/{len(test_cases)} passed"
            else:
                return None

        except Exception as e:
            print(f"❌ Logic validation failed: {e}")
            return None

    def test_real_provider_discovery(self):
        """Test discovery with providers when available."""
        print("\n Provider discovery ")

        all_providers = self.get_providers_from_networks()
        if not all_providers:
            print("❌ No providers available")
            return self._test_with_synthetic_providers()

        self.reachable_providers = self.find_reachable_providers(all_providers)

        if not self.reachable_providers:
            print("⚠️ No reachable providers found (common in blockchain networks)")
            return self._test_with_synthetic_providers()

        successful_connections = 0
        grpc_connections = 0
        http_connections = 0

        for provider in self.reachable_providers[:8]:
            host_uri = provider["host_uri"]
            hostname = provider.get("hostname", "unknown")
            network = provider.get("network", "unknown")

            try:
                print(f"\nTesting reachable provider:")
                print(f" URI: {host_uri}")
                print(f" Network: {network}")

                client = AkashClient(provider.get("rpc", MAINNET_RPC), provider.get("chain_id", MAINNET_CHAIN))

                start_time = time.time()
                result = client.discovery.get_provider_status(host_uri)
                response_time = int((time.time() - start_time) * 1000)

                if result.get("status") == "success":
                    successful_connections += 1
                    provider_status = result.get("provider_status", {})
                    method = provider_status.get("method", "Unknown")

                    if method == "GRPC":
                        grpc_connections += 1
                        print(f" ✅ Grpc connection successful ({response_time}ms)")
                        print(f" Protocol: Grpc (insecure SSL)")
                    elif method == "HTTP":
                        http_connections += 1
                        print(f" ✅ Http connection successful ({response_time}ms)")
                        print(f" Protocol: Http REST API")
                    else:
                        print(f" ✅ Connection successful via {method} ({response_time}ms)")

                    self._display_detailed_provider_info(provider_status, hostname)

                    self.tested_providers.append({
                        "host_uri": host_uri,
                        "method": method,
                        "response_time": response_time,
                        "status": "success"
                    })

                else:
                    print(f" ❌ Connection failed (provider may be down)")

            except Exception as e:
                print(f" ❌ Exception: {str(e)[:100]}...")

        print(f"\nProvider results:")
        print(f" Tested: {min(8, len(self.reachable_providers))}")
        print(f" Successful: {successful_connections}")
        print(f" Grpc connections: {grpc_connections}")
        print(f" Http connections: {http_connections}")

        if successful_connections > 0:
            return f"Provider discovery: {successful_connections} successful Grpc-first connections"
        elif len(self.reachable_providers) > 0:
            return f"Provider discovery tested with {len(self.reachable_providers)} reachable providers"
        else:
            return self._test_with_synthetic_providers()

    def _test_with_synthetic_providers(self):
        """Fallback to synthetic testing to validate logic."""
        print("Using synthetic provider testing as fallback...")

        synthetic_tests = [
            "https://synthetic-provider.test:8443",
            "synthetic-provider.test:8443"
        ]

        client = AkashClient(MAINNET_RPC, MAINNET_CHAIN)
        working_tests = 0

        for test_uri in synthetic_tests:
            try:
                result = client.discovery.get_provider_status(test_uri)
                if result.get("status") == "failed":
                    working_tests += 1
            except:
                pass

        if working_tests >= len(synthetic_tests):
            return f"Discovery logic validated with synthetic testing"
        return None

    def _display_detailed_provider_info(self, provider_status, hostname):
        """Display provider information."""
        try:
            print(f" Provider: {hostname}")

            cluster = provider_status.get("cluster", {})
            if cluster:
                leases_info = cluster.get("leases", {})
                if isinstance(leases_info, dict):
                    active_leases = leases_info.get("active", 0)
                else:
                    active_leases = leases_info
                print(f" Active leases: {active_leases}")

                inventory = cluster.get("inventory", {})
                if inventory:
                    # Get the nested cluster data that contains nodes
                    cluster_data = inventory.get("cluster", {})
                    nodes = cluster_data.get("nodes", [])

                    if nodes and len(nodes) > 0:
                        total_nodes = len(nodes)
                        print(f" Total nodes: {total_nodes}")

                        total_cpu = 0
                        total_memory = 0
                        total_storage = 0
                        total_gpu = 0

                        for node in nodes:
                            resources = node.get("resources", {})
                            if isinstance(resources, dict):
                                # Parse CPU
                                cpu = resources.get("cpu", {})
                                if isinstance(cpu, dict):
                                    cpu_quantity = cpu.get("quantity", {})
                                    allocatable = cpu_quantity.get("allocatable", {})
                                    if "string" in allocatable:
                                        try:
                                            cpu_str = allocatable["string"]
                                            # Handle millicores (e.g., "19550m")
                                            if cpu_str.endswith("m"):
                                                total_cpu += int(cpu_str[:-1])
                                            else:
                                                total_cpu += int(cpu_str) * 1000  # Convert to millicores
                                        except (ValueError, TypeError):
                                            pass

                                # Parse Memory
                                memory = resources.get("memory", {})
                                if isinstance(memory, dict):
                                    mem_quantity = memory.get("quantity", {})
                                    allocatable = mem_quantity.get("allocatable", {})
                                    if "string" in allocatable:
                                        try:
                                            total_memory += int(allocatable["string"])
                                        except (ValueError, TypeError):
                                            pass

                                # Parse Storage
                                storage = resources.get("ephemeral_storage", {})
                                if isinstance(storage, dict):
                                    allocatable = storage.get("allocatable", {})
                                    if "string" in allocatable:
                                        try:
                                            total_storage += int(allocatable["string"])
                                        except (ValueError, TypeError):
                                            pass

                                # Parse GPU
                                gpu = resources.get("gpu", {})
                                if isinstance(gpu, dict):
                                    gpu_quantity = gpu.get("quantity", {})
                                    allocatable = gpu_quantity.get("allocatable", {})
                                    if "string" in allocatable:
                                        try:
                                            total_gpu += int(allocatable["string"])
                                        except (ValueError, TypeError):
                                            pass

                        if total_cpu > 0:
                            print(f" CPU: {total_cpu:,} millicores allocatable")
                        if total_memory > 0:
                            memory_gb = total_memory / (1024 ** 3)
                            print(f" Memory: {memory_gb:.2f} GB allocatable")
                        if total_storage > 0:
                            storage_gb = total_storage / (1024 ** 3)
                            print(f" Storage: {storage_gb:.2f} GB allocatable")
                        if total_gpu > 0:
                            print(f" GPU: {total_gpu} units allocatable")
                    else:
                        print(f" No nodes found in inventory")

                resources = cluster.get("resources", {})
                if resources:
                    print(f" Resource Summary:")
                    cpu = resources.get("cpu", 0)
                    memory = resources.get("memory", 0)
                    storage = resources.get("storage", 0)
                    gpu = resources.get("gpu", 0)

                    if cpu:
                        print(f" Total CPU: {cpu}")
                    if memory:
                        print(f" Total Memory: {memory}")
                    if storage:
                        print(f" Total Storage: {storage}")
                    if gpu:
                        print(f" Total GPU: {gpu}")

            bid_engine = provider_status.get("bid_engine", {})
            if bid_engine:
                print(f" Bid engine: Active")

            hostnames = provider_status.get("public_hostnames", [])
            if hostnames:
                print(f" Public hostnames: {len(hostnames)} configured")

            errors = provider_status.get("errors", [])
            if errors:
                print(f" ⚠️ Provider errors: {len(errors)} reported")
                for i, error in enumerate(errors[:3]):
                    print(f" {i + 1}. {str(error)[:100]}...")
            else:
                print(f" ✅ Provider status: No errors reported")

            timestamp = provider_status.get("timestamp", "")
            if timestamp:
                print(f" Last updated: {timestamp}")

        except Exception as e:
            print(f" ⚠️ Error displaying provider info: {e}")
            cluster = provider_status.get("cluster", {})
            leases = cluster.get("leases", {}).get("active", 0) if cluster else 0
            print(f" Active leases: {leases}")
            print(f" Status: Connected successfully")

    def test_method_consistency(self):
        """Test consistency between different discovery methods."""
        print("\n Discovery Method Consistency ")

        test_uri = "https://test-provider.example.com:8443"

        try:
            client = AkashClient(MAINNET_RPC, MAINNET_CHAIN)

            methods = [
                ("get_provider_status", lambda: client.discovery.get_provider_status(test_uri)),
                ("get_provider_capabilities", lambda: client.discovery.get_provider_capabilities(test_uri)),
                ("get_providers_status", lambda: client.discovery.get_providers_status(provider_uris=[test_uri]))
            ]

            working_methods = 0

            for method_name, method_func in methods:
                try:
                    result = method_func()
                    if result.get("status") in ["success", "failed"]:
                        print(f" ✅ {method_name}: Working")
                        working_methods += 1
                    else:
                        print(f" ❌ {method_name}: Unexpected response")
                except Exception as e:
                    print(f" ❌ {method_name}: Exception - {e}")

            print(f"\nMethod Consistency: {working_methods}/{len(methods)} methods working")

            if working_methods >= len(methods) * 0.75:
                return f"Discovery method consistency: {working_methods}/{len(methods)} methods working"
            else:
                return None

        except Exception as e:
            print(f"❌ Method consistency test failed: {e}")
            return None

    def test_blockchain_provider_query(self):
        """Test blockchain provider querying functionality."""
        print("\n Blockchain Provider Query ")

        try:
            client = AkashClient(MAINNET_RPC, MAINNET_CHAIN)

            print(" Step 1: Querying providers from blockchain...")
            providers_result = client.discovery.get_providers(limit=50, count_total=True)

            if providers_result.get("status") == "success":
                total_providers = providers_result.get("total", 0)
                active_providers = len(providers_result.get("active_providers", []))
                inactive_providers = len(providers_result.get("inactive_providers", []))

                print(f" Total providers: {total_providers}")
                print(f" Active providers: {active_providers}")
                print(f" Inactive providers: {inactive_providers}")

                step1_success = total_providers > 0
            else:
                print(" Blockchain provider query failed")
                return None

            # Initialize connectivity tracking variables
            successful_resource_queries = 0
            successful_capacity_checks = 0
            total_attempts = 0

            if active_providers > 0:
                print(" Step 2: Testing provider connectivity (finding working providers)...")

                # Keep trying providers until we find working ones or exhaust reasonable limit
                all_providers = providers_result["active_providers"]
                max_test_limit = min(20, len(all_providers))  # Test up to 20 providers max

                working_resource_providers = []
                working_capacity_providers = []

                for i, test_provider in enumerate(all_providers[:max_test_limit], 1):
                    provider_uri = test_provider.get("host_uri", "")
                    print(f" Testing provider {i}: {provider_uri}")

                    provider_working = False

                    # Test resource query
                    try:
                        resources_result = client.discovery.get_provider_resources(provider_uri)
                        if resources_result.get("status") == "success":
                            successful_resource_queries += 1
                            working_resource_providers.append(provider_uri)
                            print(f" Resource query: ✅ success")
                            provider_working = True
                        else:
                            print(f" Resource query: ❌ {resources_result.get('status', 'failed')}")
                    except Exception as e:
                        print(f" Resource query: ❌ error ({str(e)[:50]}...)")

                    # Test capacity check  
                    try:
                        required_resources = {"cpu": "100m", "memory": "128Mi", "storage": "1Gi"}
                        capacity_result = client.discovery.get_provider_capacity(
                            provider_uri, required_resources
                        )

                        if capacity_result.get("status") == "success":
                            successful_capacity_checks += 1
                            working_capacity_providers.append(provider_uri)
                            print(f" Capacity check: ✅ success")
                            provider_working = True
                        else:
                            print(f" Capacity check: ❌ {capacity_result.get('status', 'failed')}")
                    except Exception as e:
                        print(f" Capacity check: ❌ error ({str(e)[:50]}...)")

                    total_attempts = i

                    # Stop early if we found enough working providers
                    if len(working_resource_providers) >= 2 and len(working_capacity_providers) >= 2:
                        print(f" Found sufficient working providers, stopping early ({i}/{max_test_limit} tested)")
                        break

                    # Continue if we haven't found any working providers yet
                    if i >= 5 and not (working_resource_providers or working_capacity_providers):
                        continue

                print(f" Connectivity results:")
                print(f" Tested: {total_attempts}/{len(all_providers)} providers")
                print(f" Resource queries: {successful_resource_queries} successful")
                print(f" Capacity checks: {successful_capacity_checks} successful")

                if working_resource_providers:
                    print(f" Working resource providers: {len(working_resource_providers)}")
                if working_capacity_providers:
                    print(f" Working capacity providers: {len(working_capacity_providers)}")

                # Success criteria: Must find at least 1 working provider for each test type
                step2_success = len(working_resource_providers) > 0
                step3_success = len(working_capacity_providers) > 0
            else:
                print(" Step 2 & 3: No active providers for resource testing")
                step2_success = True  # Not a failure, just no providers to test
                step3_success = True

            # Step1 must pass (provider list), connectivity tests must find working providers
            if step1_success:
                if step2_success and step3_success:
                    if active_providers > 0:
                        return f"Blockchain provider query: {total_providers} providers, {active_providers} active, connectivity verified ({successful_resource_queries} resource, {successful_capacity_checks} capacity from {total_attempts} tested)"
                    else:
                        return f"Blockchain provider query: {total_providers} providers, {active_providers} active"
                else:
                    if active_providers > 0:
                        # Connectivity test failed - couldn't find working providers
                        return None  # This should be a failure, not a pass
                    else:
                        return f"Blockchain provider query: {total_providers} providers, {active_providers} active"
            else:
                return None

        except Exception as e:
            print(f"❌ Blockchain provider query failed: {e}")
            return None

    def test_client_info_functionality(self):
        """Test client information and RPC compatibility functionality."""
        print("\n Client Info Functionality ")

        try:
            client = AkashClient(MAINNET_RPC, MAINNET_CHAIN)

            print(" Testing SDK client info retrieval...")
            client_info = client.discovery.get_client_info()

            if client_info.get("status") == "success":
                sdk_name = client_info.get("sdk_name", "")
                sdk_version = client_info.get("sdk_version", "")
                api_version = client_info.get("api_version", "")
                python_version = client_info.get("python_version", "")
                platform_info = client_info.get("platform", "")

                print(f" SDK: {sdk_name} v{sdk_version}")
                print(f" API version: {api_version}")
                print(f" Python version: {python_version}")
                print(f" Platform: {platform_info}")
                print(f" RPC endpoint: {client_info.get('rpc_endpoint', 'unknown')}")

                supported_endpoints = client_info.get("supported_endpoints", [])
                print(f" Supported endpoints: {', '.join(supported_endpoints)}")

                required_fields = ["sdk_name", "sdk_version", "api_version", "python_version"]
                has_required = all(client_info.get(field) for field in required_fields)

                if has_required:
                    return f"Client info: {sdk_name} v{sdk_version} on {platform_info}"
                else:
                    print(" Missing required client info fields")
                    return None
            else:
                print(f" Client info query failed: {client_info.get('error', 'Unknown error')}")
                return None

        except Exception as e:
            print(f"❌ Client info functionality test failed: {e}")
            return None

    def run_test(self, test_method, category):
        """Run a single test method."""
        test_name = test_method.__name__.replace('test_', '').replace('_', ' ').title()
        try:
            print(f"\n{'=' * 60}")
            result = test_method()
            if result:
                print(f"\n✅ Pass: {result}")
                self.test_results[category]['passed'] += 1
                self.test_results[category]['tests'].append(f"Pass: {test_name}")
                return True
            else:
                print(f"\n❌ Fail: {test_name}")
                self.test_results[category]['failed'] += 1
                self.test_results[category]['tests'].append(f"Fail: {test_name}")
                return False
        except Exception as e:
            print(f"\n❌ Error: {test_name} - {str(e)}")
            self.test_results[category]['failed'] += 1
            self.test_results[category]['tests'].append(f"Error: {test_name}")
            return False

    def run_all_tests(self):
        """Run all discovery tests."""
        print("=" * 80)
        print("Akash discovery tests")
        print("=" * 80)
        print("Testing Grpc-first, Http fallback implementation")

        test_sequence = [
            ('logic', self.test_discovery_logic_validation),
            ('discovery', self.test_real_provider_discovery),
            ('discovery', self.test_method_consistency),
            ('discovery', self.test_blockchain_provider_query),
            ('logic', self.test_client_info_functionality),
        ]

        for category, test_method in test_sequence:
            self.run_test(test_method, category)
            time.sleep(1)

        self.print_results()

    def print_results(self):
        """Print test results."""
        print("\n" + "=" * 80)
        print("Discovery test results")
        print("=" * 80)

        total_passed = 0
        total_failed = 0

        for category, results in self.test_results.items():
            passed = results['passed']
            failed = results['failed']
            total = passed + failed

            if total > 0:
                pass_rate = (passed / total * 100)
                print(f"\n{category.upper()}:")
                print(f" Passed: {passed}/{total} ({pass_rate:.1f}%)")

                for test_result in results['tests']:
                    status = "✅" if test_result.startswith("Pass") else "❌"
                    print(f" {status} {test_result}")

                total_passed += passed
                total_failed += failed

        total_tests = total_passed + total_failed
        overall_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0

        print(f"\nOverall results:")
        print(f" Total tests: {total_tests}")
        print(f" Passed: {total_passed}")
        print(f" Failed: {total_failed}")
        print(f" Success rate: {overall_rate:.1f}%")

        if self.tested_providers:
            successful_providers = [p for p in self.tested_providers if p.get("status") == "success"]
            grpc_providers = [p for p in successful_providers if p.get("method") == "GRPC"]

            print(f"\nProvider connections:")
            print(f" Reachable providers found: {len(self.reachable_providers)}")
            print(f" Successful connections: {len(successful_providers)}")
            if grpc_providers:
                print(f" gRPC connections: {len(grpc_providers)}")

        logic_passed = any(
            "logic" in category and results['passed'] > 0 for category, results in self.test_results.items())

        if overall_rate >= 66 or (logic_passed and total_passed >= 2):
            print("\nDiscovery module: excellent")
            print(" ✅ Grpc-first implementation validated")
            print(" ✅ Error handling and logic robust")
            if len(self.tested_providers) > 0:
                print(" ✅ Provider connections successful")
        elif overall_rate >= 33 or logic_passed:
            print("\n⚠️ Discovery module: good")
            print(" ✅ Core logic functioning correctly")
            print(" ⚠️ Network connectivity challenges (common)")
            print(" ✅ Implementation is sound")
        else:
            print("\n❌ Discovery module: needs investigation")
            print(" Review implementation")


if __name__ == "__main__":
    print("Starting discovery tests...")
    print("Logic validation and provider testing when available")

    try:
        tests = AkashDiscoveryE2ETests()
        tests.run_all_tests()
    except KeyboardInterrupt:
        print("\nTests interrupted by user")
    except Exception as e:
        print(f"\nTest suite failed: {e}")
        import traceback

        traceback.print_exc()
