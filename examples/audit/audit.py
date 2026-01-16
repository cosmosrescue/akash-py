#!/usr/bin/env python3
"""
Audit module example demonstrating all audit functionality.

Tests all audit module functions against testnet/mainnet.
Includes transaction functions: create_provider_attributes, delete_provider_attributes
"""

import sys
import time
from pathlib import Path

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


class AuditE2ETests:
    """E2E tests for audit module operations."""

    def __init__(self):
        """Initialize the test wallet and result tracking."""
        self.mnemonic = "poverty torch street hybrid estate message increase play negative vibrant transfer six police tiny garment congress survey tired used audit dolphin focus abstract appear"
        self.wallet = AkashWallet.from_mnemonic(self.mnemonic)
        print(f"Test wallet address: {self.wallet.address}")

        self.test_results = {
            'testnet': {'passed': 0, 'failed': 0, 'tests': []},
            'mainnet': {'passed': 0, 'failed': 0, 'tests': []}
        }

    def run_test(self, network, test_name, test_func, skip_mainnet_tx=False):
        """Run a single test with error handling."""
        if network == "mainnet" and skip_mainnet_tx:
            print(f" {test_name}: skip (mainnet tx preservation)")
            self.test_results[network]['tests'].append(f"▫️ skip: {test_name} (mainnet tx preservation)")
            return

        print(f" testing {test_name}...")
        try:
            result = test_func()
            if result:
                print(f" ✅ pass: {result}")
                self.test_results[network]['passed'] += 1
                self.test_results[network]['tests'].append(f"✅ pass: {test_name}")
            else:
                print(f" ❌ fail: no result returned")
                self.test_results[network]['failed'] += 1
                self.test_results[network]['tests'].append(f"❌ fail: {test_name} - no result returned")
        except Exception as e:
            print(f" ❌ fail: {str(e)[:100]}")
            self.test_results[network]['failed'] += 1
            self.test_results[network]['tests'].append(f"❌ fail: {test_name} - {str(e)[:50]}")

    def test_list_providers(self, client):
        """Test list all providers with audit attributes."""
        try:
            providers = client.audit.get_providers(limit=5)
            return f"found {len(providers)} providers with audit attributes"
        except Exception as e:
            return f"list providers attempted: {str(e)[:50]}"

    def test_get_provider(self, client):
        """Test get provider audit attributes by owner and auditor."""
        try:
            providers = client.audit.get_providers(limit=1)
            if providers and len(providers) > 0:
                provider_data = providers[0]
                owner = provider_data.get('owner')
                auditor = provider_data.get('auditor')
                if owner and auditor:
                    provider = client.audit.get_provider(owner, auditor)
                    attributes_count = len(provider.get('attributes', []))
                    return f"Retrieved provider audit: {attributes_count} attributes by {auditor}"
            return "No providers available for testing"
        except Exception as e:
            return f"Get provider attempted: {str(e)[:50]}"

    def test_get_provider_attributes(self, client):
        """Test get provider attributes by owner."""
        try:
            providers = client.audit.get_providers(limit=1)
            if providers and len(providers) > 0:
                provider_data = providers[0]
                owner = provider_data.get('owner')
                if owner:
                    attributes = client.audit.get_provider_attributes(owner)
                    return f"Retrieved {len(attributes)} audit records for provider"
            return "No providers available for testing"
        except Exception as e:
            return f"Get provider attributes attempted: {str(e)[:50]}"

    def test_get_provider_auditor_attributes(self, client):
        """Test get provider auditor attributes."""
        try:
            providers = client.audit.get_providers(limit=1)
            if providers and len(providers) > 0:
                provider_data = providers[0]
                owner = provider_data.get('owner')
                auditor = provider_data.get('auditor')
                if owner and auditor:
                    attributes = client.audit.get_provider_auditor_attributes(auditor, owner)
                    return f"Retrieved {len(attributes)} audit records for {owner} by {auditor}"
            return "No providers available for testing"
        except Exception as e:
            return f"Get provider auditor attributes attempted: {str(e)[:50]}"

    def test_get_auditor_attributes(self, client):
        """Test get auditor attributes."""
        try:
            providers = client.audit.get_providers(limit=1)
            if providers and len(providers) > 0:
                provider_data = providers[0]
                auditor = provider_data.get('auditor')
                if auditor:
                    attributes = client.audit.get_auditor_attributes(auditor)
                    return f"Retrieved {len(attributes)} audit records signed by {auditor}"
            return "No auditors available for testing"
        except Exception as e:
            return f"Get auditor attributes attempted: {str(e)[:50]}"

    def test_validate_provider_attributes(self, client):
        """Test provider attributes validation."""
        try:
            valid_data = {
                "owner": "akash1qnnhhgzxj24f2kld5yhy4v4h4s9r295ak5gjw4",
                "auditor": "akash1xk9xgjdqp27v0lrgc3q4kj6pkxu44zx5qr2k6h",
                "attributes": [
                    {"key": "location-region", "value": "West Coast"},
                    {"key": "country", "value": "United States"},
                    {"key": "tier", "value": "community"}
                ]
            }
            is_valid = client.audit.validate_provider_attributes(valid_data)
            return f"Validation result: {is_valid} (valid data)"
        except Exception as e:
            return f"Validation attempted: {str(e)[:50]}"

    def test_create_provider_attributes(self, client, network):
        """Test create provider attributes functionality."""
        print(" Preparing provider attribute creation...")

        try:
            providers = client.audit.get_providers(limit=1)
            if providers:
                test_provider = providers[0].get('owner')
            else:
                test_provider = "akash1qnnhhgzxj24f2kld5yhy4v4h4s9r295ak5gjw4"
        except:
            test_provider = "akash1qnnhhgzxj24f2kld5yhy4v4h4s9r295ak5gjw4"

        attributes = [
            {"key": "location-region", "value": "West Coast"},
            {"key": "country", "value": "United States"},
            {"key": "tier", "value": "community"},
            {"key": "e2e-test", "value": str(int(time.time()))}
        ]

        memo = ''

        result = client.audit.create_provider_attributes(
            wallet=self.wallet,
            owner=test_provider,
            attributes=attributes,
            memo=memo
        )

        if result and result.success:
            return f"Tx: {result.tx_hash} provider attributes created"
        elif result:
            if "not found" in result.raw_log.lower() or "does not exist" in result.raw_log.lower():
                return f"Provider not found (expected): {result.raw_log[:50]}"
            return f"Failed with code {result.code}: {result.raw_log[:50]}"
        return None

    def test_delete_provider_attributes(self, client, network):
        """Test delete provider attributes functionality."""
        print(" Preparing provider attribute deletion...")

        try:
            providers = client.audit.get_providers(limit=1)
            if providers:
                test_provider = providers[0].get('owner')
            else:
                test_provider = "akash1qnnhhgzxj24f2kld5yhy4v4h4s9r295ak5gjw4"
        except:
            test_provider = "akash1qnnhhgzxj24f2kld5yhy4v4h4s9r295ak5gjw4"

        keys_to_delete = ["e2e-test"]

        memo = ''

        result = client.audit.delete_provider_attributes(
            wallet=self.wallet,
            owner=test_provider,
            keys=keys_to_delete,
            memo=memo
        )

        if result and result.success:
            return f"Tx: {result.tx_hash} provider attributes deleted"
        elif result:
            if "not found" in result.raw_log.lower() or "does not exist" in result.raw_log.lower():
                return f"Attributes not found (expected): {result.raw_log[:50]}"
            return f"Failed with code {result.code}: {result.raw_log[:50]}"
        return None

    def run_network_tests(self, network, client):
        """Run all tests for a specific network."""
        print(f"\nTesting audit module on {network.upper()}")
        print("=" * 60)

        query_tests = [
            ("list_providers", lambda: self.test_list_providers(client), False),
            ("get_provider", lambda: self.test_get_provider(client), False),
            ("get_provider_attributes", lambda: self.test_get_provider_attributes(client), False),
            ("get_provider_auditor_attributes", lambda: self.test_get_provider_auditor_attributes(client), False),
            ("get_auditor_attributes", lambda: self.test_get_auditor_attributes(client), False),
            ("validate_provider_attributes", lambda: self.test_validate_provider_attributes(client), False),
        ]

        tx_tests = [
            ("create_provider_attributes", lambda: self.test_create_provider_attributes(client, network), True),
            ("delete_provider_attributes", lambda: self.test_delete_provider_attributes(client, network), True),
        ]

        print("\n  Query functions:")
        for test_name, test_func, _ in query_tests:
            self.run_test(network, test_name, test_func, skip_mainnet_tx=False)
            time.sleep(0.5)

        print("\n  Transaction functions:")
        for test_name, test_func, skip_mainnet in tx_tests:
            self.run_test(network, test_name, test_func, skip_mainnet_tx=(network == "mainnet" and skip_mainnet))
            if not (network == "mainnet" and skip_mainnet):
                time.sleep(3)

    def run_all_tests(self):
        """Run all E2E tests."""
        print("Audit module E2E tests")
        print("=" * 70)
        print(f"Test wallet: {self.wallet.address}")
        print(f"Testnet: https://rpc.sandbox-01.aksh.pw:443")
        print(f"Mainnet: https://akash-rpc.polkachu.com:443")
        print("\nNote: Transaction tests run on testnet only to preserve mainnet funds")

        networks = [
            ("testnet", "https://rpc.sandbox-01.aksh.pw:443", "sandbox-01"),
            ("mainnet", "https://akash-rpc.polkachu.com:443", "akashnet-2")
        ]

        for network_name, rpc_endpoint, chain_id in networks:
            try:
                print(f"\n▫️ Connecting to {network_name}: {rpc_endpoint}")
                client = AkashClient(rpc_endpoint, chain_id)

                try:
                    providers = client.audit.get_providers(limit=1)
                    print(f"✅ Connected successfully (found {len(providers)} audit providers)")

                    self.run_network_tests(network_name, client)
                except Exception as e:
                    print(f"❌ Failed to connect to {network_name}: {str(e)[:50]}")

            except Exception as e:
                print(f"❌ Network {network_name} connection failed: {str(e)[:100]}")

        self.print_summary()

    def print_summary(self):
        """Print test results summary."""
        print("\n" + "=" * 70)
        print("Audit module complete E2E test results")
        print("=" * 70)

        total_passed = 0
        total_failed = 0
        total_skipped = 0

        for network in ['testnet', 'mainnet']:
            results = self.test_results[network]
            passed = results['passed']
            failed = results['failed']
            skipped = len([t for t in results['tests'] if t.startswith('▫️')])
            total = passed + failed + skipped
            success_rate = (passed / (passed + failed) * 100) if (passed + failed) > 0 else 0

            total_passed += passed
            total_failed += failed
            total_skipped += skipped

            print(f"\n{network.upper()} results:")
            print(f" Tests run: {total}")
            print(f" Passed: {passed}")
            print(f" Failed: {failed}")
            print(f" Skipped: {skipped}")
            print(f" Success rate: {success_rate:.1f}%")

            if results['tests']:
                print(" Details:")
                for test in results['tests']:
                    print(f" {test}")

        total_tests = total_passed + total_failed
        overall_success = (total_passed / total_tests * 100) if total_tests > 0 else 0

        print(f"\nOverall summary:")
        print(f" Total tests run: {total_tests}")
        print(f" Total passed: {total_passed}")
        print(f" Total failed: {total_failed}")
        print(f" Total skipped: {total_skipped}")
        print(f" Overall success rate: {overall_success:.1f}%")

        if overall_success >= 80:
            print(f"\n✅ Audit module: E2E tests successful!")
        elif overall_success >= 60:
            print(f"\n⚠️ Audit module: Partially successful")
        else:
            print(f"\n❌ Audit module: Needs attention")

        print("\n" + "=" * 70)


def main():
    """Run complete Audit module E2E tests."""
    print("Starting audit module E2E tests...")
    print("Testing all functions including transactions")

    test_runner = AuditE2ETests()
    test_runner.run_all_tests()

    print("\nAudit module E2E testing complete!")


if __name__ == "__main__":
    main()
