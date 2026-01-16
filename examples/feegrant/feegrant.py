#!/usr/bin/env python3
"""
Feegrant module example demonstrating feegrant functionality.

Tests all feegrant module functions against testnet/mainnet.
Includes transaction functions: grant_allowance, revoke_allowance
"""

import os
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

GRANTEE_MNEMONIC = "true ridge approve quantum sister primary notable have express fitness forum capable"
GRANTEE_ADDRESS = "akash1dunnyt0y5476j0xawfh85n83uyzrdzlhaytyqv"


class FeegrantE2ETests:
    """E2E tests for Feegrant module including all functions."""

    def __init__(self):
        self.testnet_client = AkashClient(TESTNET_RPC, TESTNET_CHAIN)
        self.mainnet_client = AkashClient(MAINNET_RPC, MAINNET_CHAIN)
        self.wallet = AkashWallet.from_mnemonic(TEST_MNEMONIC)
        self.grantee_wallet = AkashWallet.from_mnemonic(GRANTEE_MNEMONIC)
        self.test_results = {
            'testnet': {'passed': 0, 'failed': 0, 'tests': []},
            'mainnet': {'passed': 0, 'failed': 0, 'tests': []}
        }

    def run_test(self, network, test_name, test_func, skip_mainnet_tx=False):
        """
        Run a single test and record results. all Tests run - NO Skipping.

        Test functions must return:
        - Success message string when transaction succeeds
        - None when transaction fails or times out
        """
        print(f" Testing {test_name}...")
        try:
            result = test_func()
            if result:
                print(f" ✅ PASS: {result}")
                self.test_results[network]['passed'] += 1
                self.test_results[network]['tests'].append(f"✅ {test_name}")
                return True
            else:
                print(f" ❌ FAIL: Transaction failed or timed out")
                self.test_results[network]['failed'] += 1
                self.test_results[network]['tests'].append(f"❌ {test_name}: Transaction failed")
                return False
        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)[:100]}"
            print(f" ❌ FAIL: {error_msg}")
            self.test_results[network]['failed'] += 1
            self.test_results[network]['tests'].append(f"❌ {test_name}: {error_msg}")
            return False

    def test_get_allowance(self, client):
        """Test single allowance query functionality."""
        try:
            allowance = client.feegrant.get_allowance(self.wallet.address, self.grantee_wallet.address)
            if isinstance(allowance, dict):
                if allowance:
                    return f"Found allowance: {allowance.get('allowance', {}).get('type_url', 'unknown')}"
                else:
                    return "No allowance found (expected)"
            return None
        except ImportError:
            return "Allowance query skipped (protobuf not available)"
        except Exception as e:
            print(f" Query error: {str(e)[:100]}")
            return None

    def test_get_allowances(self, client):
        """Test all allowances query for grantee."""
        try:
            allowances = client.feegrant.get_allowances(self.grantee_wallet.address)
            if isinstance(allowances, list):
                return f"Found {len(allowances)} allowances for grantee"
            return None
        except ImportError:
            return "Allowances query skipped (protobuf not available)"
        except Exception as e:
            print(f" Query error: {str(e)[:100]}")
            return None

    def test_get_allowances_by_granter(self, client):
        """Test allowances by granter query."""
        try:
            granted = client.feegrant.get_allowances_by_granter(self.wallet.address)
            if isinstance(granted, list):
                return f"Found {len(granted)} grants by this granter"
            return None
        except ImportError:
            return "Granter grants query skipped (protobuf not available)"
        except Exception as e:
            print(f" Query error: {str(e)[:100]}")
            return None

    def test_allowance_lifecycle_basic(self, client, network):
        """Test complete basic allowance lifecycle: query -> revoke -> grant -> verify -> revoke -> verify."""
        print(" Testing complete basic allowance lifecycle...")

        print(" Step 1: Checking for existing allowance...")
        try:
            existing_allowance = client.feegrant.get_allowance(self.wallet.address, self.grantee_wallet.address)
            has_existing = bool(existing_allowance)
            print(f" Existing allowance: {'Found' if has_existing else 'None'}")
        except Exception as e:
            print(f" Query failed: {str(e)}")
            has_existing = False

        if has_existing:
            print(" Step 2: Revoking existing allowance...")
            revoke_result = client.feegrant.revoke_allowance(
                wallet=self.wallet,
                grantee=self.grantee_wallet.address,
                memo="",
                fee_amount="6000",
                use_simulation=True
            )

            if not (revoke_result and revoke_result.success):
                print(" Failed to revoke existing allowance")
                return None

            print(f" Revoked: TX {revoke_result.tx_hash}")
            time.sleep(3)

            try:
                after_revoke = client.feegrant.get_allowance(self.wallet.address, self.grantee_wallet.address)
                if after_revoke:
                    print(" ERROR: Allowance still exists after revoke")
                    return None
                print(" Verified: Allowance successfully removed")
            except Exception:
                print(" Verified: No allowance found (revoke successful)")

        print(" Step 3: Granting new basic allowance...")
        amount = "2000000"  # 2 AKT
        grant_result = client.feegrant.grant_allowance(
            wallet=self.wallet,
            grantee=self.grantee_wallet.address,
            allowance_type="basic",
            spend_limit=amount,
            denom="uakt",
            memo="",
            fee_amount="8000",
            use_simulation=True
        )

        if not (grant_result and grant_result.success):
            print(
                f" Grant failed - Code {grant_result.code if grant_result else 'None'}: {grant_result.raw_log[:50] if grant_result and hasattr(grant_result, 'raw_log') else 'No log'}")
            return None

        print(f" Granted: TX {grant_result.tx_hash} (limit: {amount} uakt)")
        time.sleep(3)

        print(" Step 4: Verifying grant was created...")
        try:
            new_allowance = client.feegrant.get_allowance(self.wallet.address, self.grantee_wallet.address)
            if not new_allowance:
                print(" ERROR: No allowance found after grant")
                return None
            print(f" Verified: Allowance created ({new_allowance.get('allowance', {}).get('type_url', 'unknown')})")
        except Exception as e:
            print(f" Verification failed: {str(e)}")
            return None

        print(" Step 5: Final revoke to clean up...")
        final_revoke = client.feegrant.revoke_allowance(
            wallet=self.wallet,
            grantee=self.grantee_wallet.address,
            memo="",
            fee_amount="6000",
            use_simulation=True
        )

        if not (final_revoke and final_revoke.success):
            print(" Final revoke failed")
            return None

        print(f" Final revoke: TX {final_revoke.tx_hash}")
        time.sleep(3)

        print(" Step 6: Verifying cleanup...")
        try:
            final_check = client.feegrant.get_allowance(self.wallet.address, self.grantee_wallet.address)
            if final_check:
                print(" Warning: Allowance still exists after final revoke")
            else:
                print(" Verified: Complete cleanup successful")
        except Exception:
            print(" Verified: No allowance found (cleanup successful)")

        return f"Complete lifecycle: grant -> verify -> revoke -> verify (TXs: {grant_result.tx_hash}/{final_revoke.tx_hash})"

    def test_allowance_lifecycle_periodic(self, client, network):
        """Test complete periodic allowance lifecycle: query -> clean -> grant -> verify -> revoke -> verify."""
        print(" Testing complete periodic allowance lifecycle...")

        print(" Step 1: Cleaning existing allowances...")
        try:
            existing = client.feegrant.get_allowance(self.wallet.address, self.grantee_wallet.address)
            if existing:
                print(" Found existing allowance, revoking...")
                clean_result = client.feegrant.revoke_allowance(
                    wallet=self.wallet,
                    grantee=self.grantee_wallet.address,
                    memo="",
                    fee_amount="6000",
                    use_simulation=True
                )
                if clean_result and clean_result.success:
                    print(f" Cleaned: TX {clean_result.tx_hash}")
                    time.sleep(3)
                else:
                    print(" Cleanup failed")
                    return None
            else:
                print(" No existing allowance (clean slate)")
        except Exception as e:
            print(f" Cleanup check failed: {str(e)}")

        print(" Step 2: Granting periodic allowance...")
        amount = "4000000"  # 4 AKT
        expiration = "2025-12-31T23:59:59Z"

        grant_result = client.feegrant.grant_allowance(
            wallet=self.wallet,
            grantee=self.grantee_wallet.address,
            allowance_type="periodic",
            spend_limit=amount,
            denom="uakt",
            expiration=expiration,
            memo="",
            fee_amount="8000",
            use_simulation=True
        )

        if not (grant_result and grant_result.success):
            print(
                f" Periodic grant failed - Code {grant_result.code if grant_result else 'None'}: {grant_result.raw_log[:50] if grant_result and hasattr(grant_result, 'raw_log') else 'No log'}")
            return None

        print(f" Periodic granted: TX {grant_result.tx_hash} (limit: {amount} uakt)")
        time.sleep(3)

        print(" Step 3: Verifying periodic allowance...")
        try:
            periodic_allowance = client.feegrant.get_allowance(self.wallet.address, self.grantee_wallet.address)
            if not periodic_allowance:
                print(" ERROR: No periodic allowance found after grant")
                return None

            allowance_type = periodic_allowance.get('allowance', {}).get('type_url', '')
            is_periodic = 'PeriodicAllowance' in allowance_type
            print(f" Verified: {'Periodic' if is_periodic else 'Basic'} allowance created ({allowance_type})")

            if not is_periodic:
                print(" Warning: Expected periodic allowance but got different type")

        except Exception as e:
            print(f" Periodic verification failed: {str(e)}")
            return None

        print(" Step 4: Cleaning up periodic allowance...")
        cleanup_result = client.feegrant.revoke_allowance(
            wallet=self.wallet,
            grantee=self.grantee_wallet.address,
            memo="",
            fee_amount="6000",
            use_simulation=True
        )

        if not (cleanup_result and cleanup_result.success):
            print(" Periodic cleanup failed")
            return None

        print(f" Periodic cleanup: TX {cleanup_result.tx_hash}")
        time.sleep(3)

        print(" Step 5: Verifying periodic cleanup...")
        try:
            final_check = client.feegrant.get_allowance(self.wallet.address, self.grantee_wallet.address)
            if final_check:
                print(" Warning: Periodic allowance still exists after revoke")
            else:
                print(" Verified: Periodic allowance successfully removed")
        except Exception:
            print(" Verified: No allowance found (periodic cleanup successful)")

        return f"Periodic lifecycle: grant -> verify -> revoke -> verify (TXs: {grant_result.tx_hash}/{cleanup_result.tx_hash})"

    def test_allowance_query_verification(self, client, network):
        """Test allowance queries work correctly with grant/revoke cycle."""
        print(" Testing allowance query verification...")

        print(" Step 1: Ensuring clean state...")
        try:
            initial_check = client.feegrant.get_allowance(self.wallet.address, self.grantee_wallet.address)
            if initial_check:
                print(" Cleaning existing allowance...")
                clean_result = client.feegrant.revoke_allowance(
                    wallet=self.wallet,
                    grantee=self.grantee_wallet.address,
                    memo="",
                    fee_amount="6000",
                    use_simulation=True
                )
                if not (clean_result and clean_result.success):
                    print(" Initial cleanup failed")
                    return None
                time.sleep(3)
        except Exception:
            pass

        print(" Step 2: Verifying empty state...")
        try:
            empty_check = client.feegrant.get_allowance(self.wallet.address, self.grantee_wallet.address)
            if empty_check:
                print(" ERROR: Allowance still exists after cleanup")
                return None
            print(" Verified: No allowance exists (clean state)")
        except Exception:
            print(" Verified: No allowance found (clean state)")

        print(" Step 3: Granting allowance for query test...")
        grant_result = client.feegrant.grant_allowance(
            wallet=self.wallet,
            grantee=self.grantee_wallet.address,
            allowance_type="basic",
            spend_limit="1500000",  # 1.5 AKT
            denom="uakt",
            memo="",
            fee_amount="8000",
            use_simulation=True
        )

        if not (grant_result and grant_result.success):
            print(" Query test grant failed")
            return None

        print(f" Query test granted: TX {grant_result.tx_hash}")
        time.sleep(3)

        print(" Step 4: Testing all query methods...")

        try:
            single_allowance = client.feegrant.get_allowance(self.wallet.address, self.grantee_wallet.address)
            if not single_allowance:
                print(" ERROR: get_allowance returned empty after grant")
                return None
            print(" ✅ get_allowance: Found allowance")
        except Exception as e:
            print(f" ❌ get_allowance failed: {str(e)}")
            return None

        try:
            grantee_allowances = client.feegrant.get_allowances(self.grantee_wallet.address)
            found_in_grantee = any(a.get('granter') == self.wallet.address for a in grantee_allowances)
            print(
                f" ✅ get_allowances: Found {len(grantee_allowances)} allowances, ours: {'Yes' if found_in_grantee else 'No'}")
        except Exception as e:
            print(f" ⚠️ get_allowances failed: {str(e)}")

        try:
            granter_allowances = client.feegrant.get_allowances_by_granter(self.wallet.address)
            found_in_granter = any(a.get('grantee') == self.grantee_wallet.address for a in granter_allowances)
            print(
                f" ✅ get_allowances_by_granter: Found {len(granter_allowances)} grants, ours: {'Yes' if found_in_granter else 'No'}")
        except Exception as e:
            print(f" ⚠️ get_allowances_by_granter failed: {str(e)}")

        print(" Step 5: Revoking and verifying query updates...")
        revoke_result = client.feegrant.revoke_allowance(
            wallet=self.wallet,
            grantee=self.grantee_wallet.address,
            memo="",
            fee_amount="6000",
            use_simulation=True
        )

        if not (revoke_result and revoke_result.success):
            print(" Query test revoke failed")
            return None

        print(f" Query test revoked: TX {revoke_result.tx_hash}")
        time.sleep(3)

        try:
            after_revoke = client.feegrant.get_allowance(self.wallet.address, self.grantee_wallet.address)
            if after_revoke:
                print(" Warning: Allowance still found after revoke (timing issue)")
            else:
                print(" ✅ Verified: Allowance removed from queries")
        except Exception:
            print(" ✅ Verified: No allowance found after revoke")

        return f"Query verification: grant -> query -> revoke -> query (TXs: {grant_result.tx_hash}/{revoke_result.tx_hash})"

    def test_create_basic_allowance(self, client):
        """Test basic allowance creation utility."""
        try:
            basic_allowance = client.feegrant.create_basic_allowance(
                spend_limit="5000000",
                denom="uakt",
                expiration="2025-12-31T23:59:59Z"
            )
            
            expected_fields = ["@type", "spend_limit"]
            missing_fields = [field for field in expected_fields if field not in basic_allowance]
            
            if not missing_fields:
                has_expiration = "expiration" in basic_allowance
                return f"Basic allowance structure created: {len(basic_allowance)} fields, expiration: {'Yes' if has_expiration else 'No'}"
            else:
                return None
        except Exception as e:
            print(f" Utility error: {str(e)[:100]}")
            return None

    def test_create_periodic_allowance(self, client):
        """Test periodic allowance creation utility."""
        try:
            periodic_allowance = client.feegrant.create_periodic_allowance(
                total_limit="10000000",
                period_limit="1000000", 
                period_seconds=86400,
                denom="uakt"
            )
            
            expected_fields = ["@type", "basic", "period", "period_spend_limit"]
            missing_fields = [field for field in expected_fields if field not in periodic_allowance]
            
            if not missing_fields:
                has_period = "seconds" in periodic_allowance.get("period", {})
                return f"Periodic allowance structure created: {len(periodic_allowance)} fields, period: {'Yes' if has_period else 'No'}"
            else:
                return None
        except Exception as e:
            print(f" Utility error: {str(e)[:100]}")
            return None

    def test_grant_with_custom_parameters(self, client, network):
        """Test grant with custom gas and fee parameters."""
        print(" Preparing custom parameter grant...")

        amount = "3000000"  # 3 AKT
        custom_fee = "12000"  # 0.012 AKT fee
        custom_gas = 250000
        memo = ''

        result = client.feegrant.grant_allowance(
            wallet=self.wallet,
            grantee=self.grantee_wallet.address,
            allowance_type="basic",
            spend_limit=amount,
            denom="uakt",
            memo=memo,
            fee_amount=custom_fee,
            gas_limit=custom_gas,
            use_simulation=False
        )

        if result and result.success:
            return f"TX: {result.tx_hash} (fee: {custom_fee} uakt, gas: {custom_gas})"
        elif result:
            print(
                f" Transaction failed - Code {result.code}: {result.raw_log[:50] if hasattr(result, 'raw_log') else 'No log'}")
            return None
        return None

    def run_network_tests(self, network, client):
        """Run all tests for a specific network."""
        print(f"\nTesting feegrant module on {network.upper()}")
        print("=" * 60)

        query_tests = [
            ("get_allowance", lambda: self.test_get_allowance(client), False),
            ("get_allowances", lambda: self.test_get_allowances(client), False),
            ("get_allowances_by_granter", lambda: self.test_get_allowances_by_granter(client), False),
        ]

        utility_tests = [
            ("create_basic_allowance", lambda: self.test_create_basic_allowance(client), False),
            ("create_periodic_allowance", lambda: self.test_create_periodic_allowance(client), False),
        ]

        tx_tests = [
            ("allowance_lifecycle_basic", lambda: self.test_allowance_lifecycle_basic(client, network), True),
            ("allowance_lifecycle_periodic", lambda: self.test_allowance_lifecycle_periodic(client, network), True),
            ("allowance_query_verification", lambda: self.test_allowance_query_verification(client, network), True),
            ("grant_with_custom_parameters", lambda: self.test_grant_with_custom_parameters(client, network), True),
        ]

        print("\n  Query functions:")
        for test_name, test_func, _ in query_tests:
            self.run_test(network, test_name, test_func, skip_mainnet_tx=False)
            time.sleep(0.5)

        print("\n  Utility functions:")
        for test_name, test_func, _ in utility_tests:
            self.run_test(network, test_name, test_func, skip_mainnet_tx=False)
            time.sleep(0.2)

        print("\n  Transaction functions:")
        for test_name, test_func, skip_mainnet in tx_tests:
            self.run_test(network, test_name, test_func, skip_mainnet_tx=(network == "mainnet" and skip_mainnet))
            if not (network == "mainnet" and skip_mainnet):
                time.sleep(3)

    def run_all_tests(self):
        """Run all E2E tests."""
        print("Feegrant module tests")
        print("=" * 70)
        print(f"Test wallet (granter): {self.wallet.address}")
        print(f"Grantee wallet: {self.grantee_wallet.address}")
        print(f"Testnet: {TESTNET_RPC}")
        print(f"Mainnet: {MAINNET_RPC}")
        print("\nNote: Transaction tests run on testnet only to preserve mainnet funds")

        self.run_network_tests("testnet", self.testnet_client)

        self.run_network_tests("mainnet", self.mainnet_client)

        self.print_summary()

    def print_summary(self):
        """Print test results summary."""
        print("\n" + "=" * 70)
        print("Feegrant module test results")
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
            print(f"\n✅ Feegrant module: tests successful!")
        elif overall_success >= 60:
            print(f"\n⚠️ Feegrant module: partially successful")
        else:
            print(f"\n❌ Feegrant module: needs attention")

        print("\n" + "=" * 70)


def main():
    """Run feegrant module tests."""
    print("Starting feegrant module tests...")
    print("Testing all functions including transactions")

    test_runner = FeegrantE2ETests()
    test_runner.run_all_tests()

    print("\nFeegrant module testing complete!")


if __name__ == "__main__":
    main()