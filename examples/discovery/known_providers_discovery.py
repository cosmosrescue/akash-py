#!/usr/bin/env python3
"""
Test connectivity to known working Akash providers.
"""

import json
import sys
from pathlib import Path

# Development mode: Use local akash if running from repo
examples_dir = Path(__file__).parent.parent
if (examples_dir.parent / "akash").exists() and (examples_dir.parent / "pyproject.toml").exists():
    sys.path.insert(0, str(examples_dir.parent))
    print("✓ Development mode: Using local akash")

try:
    from akash import AkashClient
except ImportError as e:
    print(f"Failed to import akash SDK: {e}")
    print("Please run: pip install -r requirements.txt")
    sys.exit(1)

MAINNET_RPC = "https://akash-rpc.polkachu.com:443"
MAINNET_CHAIN = "akashnet-2"

KNOWN_PROVIDERS = [
    {
        "name": "EuroPlots",
        "uri": "https://provider.europlots.com:8443",
        "address": "akash18ga02jzaq8cw52anyhzkwta5wygufgu6zsz6xc"
    },
    {
        "name": "BDL Computer",
        "uri": "https://provider.bdl.computer:8443",
        "address": "akash19yhu3jgw8h0320av98h8n5qczje3pj3u9u2amp"
    },
    {
        "name": "Paradigma Politico",
        "uri": "https://provider.paradigmapolitico.online:8443",
        "address": "akash16lr6sexztap5394wqtqgqt4mfuv7y2welmpjr2"
    }
]


def test_provider_connectivity():
    """Test connectivity to known providers with detailed debugging."""

    client = AkashClient(MAINNET_RPC, MAINNET_CHAIN)

    print("Testing known Akash providers...")
    print("=" * 60)

    successful_resource_tests = 0
    successful_capacity_tests = 0
    total_tests = len(KNOWN_PROVIDERS)

    for i, provider in enumerate(KNOWN_PROVIDERS, 1):
        print(f"\nProvider {i}/{total_tests}: {provider['name']}")
        print(f"URI: {provider['uri']}")
        print(f"Address: {provider['address']}")
        print("-" * 40)

        print("Testing full provider status...")
        try:
            status_result = client.discovery.get_provider_status(provider['uri'])
            print(f"Provider status: {status_result.get('status')}")

            if status_result.get("status") == "success":
                print("✅ Provider status: Success")
                provider_status = status_result.get("provider_status", {})

                print("Provider status overview:")
                for key, value in provider_status.items():
                    if key not in ['cluster', 'bid_engine']:
                        print(f"  {key}: {value}")

                cluster = provider_status.get("cluster", {})
                if cluster:
                    print("\nCluster information:")
                    print(f"  Cluster data keys: {list(cluster.keys())}")

                    inventory = cluster.get("inventory", {})
                    if inventory:
                        print("  Inventory keys:", list(inventory.keys()))
                        cluster_resources = inventory.get("cluster", {})
                        if cluster_resources:
                            print("  Cluster resources:")
                            for res_type, res_data in cluster_resources.items():
                                print(f"  {res_type}: {res_data} (type: {type(res_data)})")
                                if isinstance(res_data, dict) and res_data:
                                    print(f" Details: {json.dumps(res_data, indent=6)}")
            else:
                print(f"❌ Provider status: Failed - {status_result.get('status')}")
        except Exception as e:
            print(f"❌ Provider status: Error - {str(e)}")

        print("\nTesting resource query...")
        try:
            resources_result = client.discovery.get_provider_resources(provider['uri'])
            if resources_result.get("status") == "success":
                successful_resource_tests += 1
                print("✅ Resource query: Success")

                resources = resources_result.get("resources", {})
                available = resources.get("available", {})
                print("Resource query result:")
                for res_type, res_value in available.items():
                    print(f"  {res_type}: {res_value} (type: {type(res_value)})")
            else:
                print(f"❌ Resource query: Failed - {resources_result.get('status')}")
        except Exception as e:
            print(f"❌ Resource query: Error - {str(e)}")

        print("\nTesting capacity check...")
        try:
            required_resources = {"cpu": "100m", "memory": "128Mi", "storage": "1Gi"}
            print(f"Required resources: {required_resources}")

            capacity_result = client.discovery.get_provider_capacity(
                provider['uri'], required_resources
            )
            print(f"Capacity check status: {capacity_result.get('status')}")

            if capacity_result.get("status") == "success":
                successful_capacity_tests += 1
                print("✅ Capacity check: Success")
                print(f"Has capacity: {capacity_result.get('has_capacity')}")

                sufficient = capacity_result.get('sufficient', {})
                for res_type, is_sufficient in sufficient.items():
                    status = "✅" if is_sufficient else "❌"
                    print(f"  {res_type}: {status} sufficient")
            else:
                print(f"❌ Capacity check: Failed - {capacity_result.get('status')}")
                if 'error' in capacity_result:
                    print(f"  Error: {capacity_result['error']}")
        except Exception as e:
            print(f"❌ Capacity check: Error - {str(e)}")

    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Total providers tested: {total_tests}")
    print(f"Successful resource queries: {successful_resource_tests}/{total_tests}")
    print(f"Successful capacity checks: {successful_capacity_tests}/{total_tests}")

    if successful_resource_tests > 0 and successful_capacity_tests > 0:
        print("✅ Overall: Provider connectivity working!")
    elif successful_resource_tests > 0:
        print("⚠️  Partial: Resource queries work, capacity checks have issues")
    else:
        print("❌ Overall: Provider connectivity not working")


if __name__ == "__main__":
    test_provider_connectivity()
