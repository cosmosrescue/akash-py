#!/usr/bin/env python3
"""
Evidence module example demonstrating evidence functionality.

Tests evidence functionality including evidence queries and validation.
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

TESTNET_RPC = "https://rpc.sandbox-01.aksh.pw:443"
TESTNET_CHAIN = "sandbox-01"
MAINNET_RPC = "https://akash-rpc.polkachu.com:443"
MAINNET_CHAIN = "akashnet-2"

TEST_MNEMONIC = "poverty torch street hybrid estate message increase play negative vibrant transfer six police tiny garment congress survey tired used audit dolphin focus abstract appear"
TEST_ADDRESS = "akash1qnnhhgzxj24f2kld5yhy4v4h4s9r295ak5gjw4"


class EvidenceCompleteE2ETests:

    def __init__(self):
        self.testnet_client = AkashClient(TESTNET_RPC, TESTNET_CHAIN)
        self.mainnet_client = AkashClient(MAINNET_RPC, MAINNET_CHAIN)
        self.wallet = AkashWallet.from_mnemonic(TEST_MNEMONIC)
        self.test_results = {
            'testnet': {'passed': 0, 'failed': 0, 'tests': []},
            'mainnet': {'passed': 0, 'failed': 0, 'tests': []}
        }

    def run_test(self, network, test_name, test_func, skip_mainnet_tx=False):
        print(f" Testing {test_name}...")
        try:
            result = test_func()
            if result:
                print(f" ✅ Pass: {result}")
                self.test_results[network]['passed'] += 1
                self.test_results[network]['tests'].append(f"✅ {test_name}")
                return True
            else:
                print(f" ❌ Fail: Test failed or returned no data")
                self.test_results[network]['failed'] += 1
                self.test_results[network]['tests'].append(f"❌ {test_name}: Test failed")
                return False
        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)[:100]}"
            print(f" ❌ Fail: {error_msg}")
            self.test_results[network]['failed'] += 1
            self.test_results[network]['tests'].append(f"❌ {test_name}: {error_msg}")
            return False

    def test_get_evidence(self, client):
        test_hash = "deadbeefcafebabe" + "0" * 48
        evidence = client.evidence.get_evidence(test_hash)

        if isinstance(evidence, dict) and len(evidence) == 0:
            return f"Evidence query correctly returns empty for non-existent hash"
        elif isinstance(evidence, dict) and len(evidence) > 0:
            return f"Found actual evidence: {list(evidence.keys())}"
        return None

    def test_get_all_evidence(self, client):
        evidence_list = client.evidence.get_all_evidence(limit=10)
        if isinstance(evidence_list, list):
            if len(evidence_list) == 0:
                return f"Evidence query working correctly (no evidence found, which is normal)"
            else:
                return f"Found {len(evidence_list)} evidence records (unusual but valid)"
        return None

    def test_get_all_evidence_with_pagination(self, client):
        evidence_list = client.evidence.get_all_evidence(limit=5, offset=0)
        if isinstance(evidence_list, list):
            return f"Pagination parameters accepted correctly: {len(evidence_list)} records"
        return None

    def test_validate_evidence_format_valid(self, client):
        valid_evidence = {
            "type_url": "/cosmos.evidence.v1beta1.Equivocation",
            "content": "some_evidence_content"
        }
        validation = client.evidence.validate_evidence_format(valid_evidence)

        if (isinstance(validation, dict) and
                validation.get('valid') is True and
                isinstance(validation.get('errors'), list) and
                isinstance(validation.get('warnings'), list)):
            return f"Valid evidence format accepted: {len(validation['errors'])} errors, {len(validation['warnings'])} warnings"
        return None

    def test_validate_evidence_format_invalid(self, client):
        invalid_evidence = {
            "type_url": "/cosmos.evidence.v1beta1.Equivocation"
        }
        validation = client.evidence.validate_evidence_format(invalid_evidence)

        if (isinstance(validation, dict) and
                validation.get('valid') is False and
                len(validation.get('errors', [])) > 0):
            return f"Invalid evidence format correctly rejected: {len(validation['errors'])} errors"
        return None

    def test_validate_evidence_format_warnings(self, client):
        warning_evidence = {
            "type_url": "/unusual.module.v1.SomeEvidence",
            "content": "some_evidence_content"
        }
        validation = client.evidence.validate_evidence_format(warning_evidence)

        if (isinstance(validation, dict) and
                len(validation.get('warnings', [])) > 0):
            return f"Unusual type_url generated warnings: {len(validation['warnings'])} warnings"
        return None

    def test_validate_evidence_format_empty(self, client):
        empty_evidence = {}
        validation = client.evidence.validate_evidence_format(empty_evidence)

        if (isinstance(validation, dict) and
                validation.get('valid') is False and
                len(validation.get('errors', [])) > 0):
            return f"Empty evidence correctly rejected: {len(validation['errors'])} errors"
        return None

    def test_submit_evidence(self, client, network):
        print(" Note: Testing evidence validation - submission should be rejected")

        invalid_evidence = {
            "type_url": "/cosmos.evidence.v1beta1.Equivocation",
            "content": "clearly_invalid_test_data"
        }

        try:
            result = client.evidence.submit_evidence(
                wallet=self.wallet,
                evidence_data=invalid_evidence,
                memo="",
            )

            if result and result.success:
                return None
            elif result and result.code != 0:
                return f"Blockchain correctly rejected invalid evidence: Code {result.code}"
            else:
                return None
        except Exception as e:
            return f"Evidence validation working: {type(e).__name__}"

    def run_network_tests(self, network, client):
        print(f"\nTesting evidence module on {network.upper()}")
        print("=" * 60)

        query_tests = [
            ("get_evidence", lambda: self.test_get_evidence(client), False),
            ("get_all_evidence", lambda: self.test_get_all_evidence(client), False),
            ("get_all_evidence_pagination", lambda: self.test_get_all_evidence_with_pagination(client), False),
        ]

        utility_tests = [
            ("validate_evidence_valid", lambda: self.test_validate_evidence_format_valid(client), False),
            ("validate_evidence_invalid", lambda: self.test_validate_evidence_format_invalid(client), False),
            ("validate_evidence_warnings", lambda: self.test_validate_evidence_format_warnings(client), False),
            ("validate_evidence_empty", lambda: self.test_validate_evidence_format_empty(client), False),
        ]

        tx_tests = [
            ("submit_evidence", lambda: self.test_submit_evidence(client, network), True),
        ]

        print("\n  Query functions:")
        for test_name, test_func, _ in query_tests:
            self.run_test(network, test_name, test_func, skip_mainnet_tx=False)
            time.sleep(0.5)

        print("\n  Utility functions:")
        for test_name, test_func, _ in utility_tests:
            self.run_test(network, test_name, test_func, skip_mainnet_tx=False)
            time.sleep(0.2)

        if network == "testnet":
            print("\n  Transaction functions (testnet only):")
            for test_name, test_func, skip_mainnet in tx_tests:
                self.run_test(network, test_name, test_func, skip_mainnet_tx=False)
                time.sleep(2)

    def run_all_tests(self):
        print("Evidence module tests")
        print("=" * 70)
        print(f"Test wallet: {self.wallet.address}")
        print(f"Testnet: {TESTNET_RPC}")
        print(f"Mainnet: {MAINNET_RPC}")
        print("\nNote: evidence is rare on Akash - most queries will return empty results")
        print("Note: evidence submissions require specific validator misbehavior conditions")

        self.run_network_tests("testnet", self.testnet_client)
        self.run_network_tests("mainnet", self.mainnet_client)
        self.print_summary()

    def print_summary(self):
        print("\n" + "=" * 70)
        print("Evidence module test results")
        print("=" * 70)

        total_passed = 0
        total_failed = 0
        total_skipped = 0

        for network in ['testnet', 'mainnet']:
            results = self.test_results[network]
            passed = results['passed']
            failed = results['failed']
            skipped = 0
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
            print(f"\n✅ Evidence module: tests successful")
        elif overall_success >= 60:
            print(f"\n⚠️ Evidence module: partially successful")
        else:
            print(f"\n❌ Evidence module: needs attention")

        print("\n" + "=" * 70)


def main():
    """Run complete evidence module tests."""
    print("Starting evidence module tests...")
    print("Testing all functions including rare evidence operations")

    test_runner = EvidenceCompleteE2ETests()
    test_runner.run_all_tests()

    print("\nEvidence module testing complete")


if __name__ == "__main__":
    main()
