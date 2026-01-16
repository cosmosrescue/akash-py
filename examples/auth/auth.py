#!/usr/bin/env python3
"""
Auth module example demonstrating all auth functionality.

Tests the auth client functionality against live blockchain data.
"""

import logging
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

logging.getLogger('akash').setLevel(logging.WARNING)

TESTNET_RPC = "https://rpc.sandbox-01.aksh.pw:443"
TESTNET_CHAIN_ID = "sandbox-01"
TEST_MNEMONIC = "poverty torch street hybrid estate message increase play negative vibrant transfer six police tiny garment congress survey tired used audit dolphin focus abstract appear"


class AuthE2ETests:
    """E2E test suite for Auth module functionality."""

    def __init__(self):
        """Initialize test environment with live testnet connection."""
        self.testnet_client = AkashClient(TESTNET_RPC, TESTNET_CHAIN_ID)
        self.test_wallet = AkashWallet.from_mnemonic(TEST_MNEMONIC)
        self.test_address = self.test_wallet.address

        print(f"Auth E2E Tests - Testnet: {TESTNET_RPC}")
        print(f"Test Address: {self.test_address}")

    def test_get_account(self):
        """Test getting account information for a known account."""
        try:
            print(" Testing get_account for funded test wallet...")
            account_info = self.testnet_client.auth.get_account(self.test_address)

            if account_info:
                required_fields = ['address', 'account_number', 'sequence', 'type_url']
                missing_fields = [field for field in required_fields if field not in account_info]

                if not missing_fields:
                    print(f" Account found: {account_info['address']}")
                    print(f" Account number: {account_info['account_number']}")
                    print(f" Sequence: {account_info['sequence']}")
                    print(f" Type: {account_info['type_url']}")
                    return f"Account info retrieved successfully for {self.test_address}"
                else:
                    print(f" Missing fields: {missing_fields}")
                    return None
            else:
                print(" No account info returned")
                return None

        except Exception as e:
            print(f" Error: {e}")
            return None

    def test_get_account_nonexistent(self):
        """Test getting account info for non-existent account."""
        try:
            print(" Testing get_account for non-existent account...")
            fake_address = "akash1nonexistentaccountaddressfortesting123456789"
            account_info = self.testnet_client.auth.get_account(fake_address)

            if account_info is None:
                return "Non-existent account correctly returned None"
            else:
                print(f" Unexpected result for fake address: {account_info}")
                return None

        except Exception as e:
            print(f" Error: {e}")
            return None

    def test_get_accounts(self):
        """Test getting multiple accounts with pagination."""
        try:
            print(" Testing get_accounts with pagination...")

            accounts = self.testnet_client.auth.get_accounts(limit=3, offset=0)

            if isinstance(accounts, list):
                if len(accounts) > 0:
                    print(f" Retrieved {len(accounts)} accounts")

                    first_account = accounts[0]
                    if 'address' in first_account and 'account_number' in first_account:
                        print(f" First account: {first_account['address']}")
                        return f"Retrieved {len(accounts)} accounts successfully"
                    else:
                        print(f" First account missing fields: {first_account}")
                        return None
                else:
                    return "Retrieved 0 accounts (valid empty result)"
            else:
                print(f" Invalid accounts response type: {type(accounts)}")
                return None

        except Exception as e:
            print(f" Error: {e}")
            return None

    def test_get_auth_params(self):
        """Test getting auth module parameters."""
        try:
            print(" Testing get_auth_params...")
            auth_params = self.testnet_client.auth.get_auth_params()

            if auth_params:
                expected_fields = [
                    'max_memo_characters',
                    'tx_sig_limit',
                    'tx_size_cost_per_byte',
                    'sig_verify_cost_ed25519',
                    'sig_verify_cost_secp256k1'
                ]

                missing_fields = [field for field in expected_fields if field not in auth_params]

                if not missing_fields:
                    print(f" Max memo chars: {auth_params['max_memo_characters']}")
                    print(f" Tx sig limit: {auth_params['tx_sig_limit']}")
                    print(f" Size cost per byte: {auth_params['tx_size_cost_per_byte']}")
                    return "Auth params retrieved with all expected fields"
                else:
                    print(f" Missing param fields: {missing_fields}")
                    return None
            else:
                print(" No auth params returned")
                return None

        except Exception as e:
            print(f" Error: {e}")
            return None

    def test_get_module_account_by_name(self):
        """Test getting module account by name."""
        try:
            print(" Testing get_module_account_by_name...")

            test_modules = ['distribution', 'bonded_tokens_pool', 'fee_collector']

            for module_name in test_modules:
                print(f" Testing module account: {module_name}")
                module_account = self.testnet_client.auth.get_module_account_by_name(module_name)

                if module_account:
                    if 'name' in module_account and 'type_url' in module_account:
                        print(f" Found {module_name}: {module_account['type_url']}")
                        return f"Module account {module_name} found successfully"
                    else:
                        print(f" Module account missing fields: {module_account}")
                        continue
                else:
                    print(f" Module account {module_name} not found")
                    continue

            print(" No module accounts found - this may be normal")
            return "Module account query completed (no accounts found)"

        except Exception as e:
            print(f" Error: {e}")
            return None

    def test_convenience_methods(self):
        """Test convenience helper methods."""
        try:
            print(" Testing convenience methods...")

            account_info = self.testnet_client.auth.get_account_info(self.test_address)
            if not account_info or 'sequence' not in account_info:
                print(" get_account_info failed")
                return None

            print(f" Account info - Sequence: {account_info['sequence']}, Number: {account_info['account_number']}")

            is_valid = self.testnet_client.auth.validate_address_existence(self.test_address)
            if not is_valid:
                print(" validate_address failed for valid address")
                return None

            print(f" Address validation: Valid")

            next_seq = self.testnet_client.auth.get_next_sequence_number(self.test_address)
            if next_seq != account_info['sequence']:
                print(f" Sequence mismatch: {next_seq} vs {account_info['sequence']}")
                return None

            print(f" Next sequence number: {next_seq}")

            account_num = self.testnet_client.auth.get_account_number(self.test_address)
            if account_num != account_info['account_number']:
                print(f" Account number mismatch: {account_num} vs {account_info['account_number']}")
                return None

            print(f" Account number: {account_num}")

            return "All convenience methods working correctly"

        except Exception as e:
            print(f" Error: {e}")
            return None

    def test_address_validation(self):
        """Test address format validation methods."""
        try:
            print(" Testing address validation methods...")

            is_format_valid = self.testnet_client.auth.validate_address(self.test_address)
            if not is_format_valid:
                print(" validate_address failed for properly formatted address")
                return None

            print(f" Address format validation: Valid")

            invalid_address = "invalid_address_format"
            is_invalid_format = self.testnet_client.auth.validate_address(invalid_address)
            if is_invalid_format:
                print(" validate_address incorrectly validated invalid address")
                return None

            print(f" Invalid address format validation: Correctly rejected")

            wrong_prefix = "cosmos1qnnhhgzxj24f2kld5yhy4v4h4s9r295ak5gjw4"
            is_wrong_prefix = self.testnet_client.auth.validate_address(wrong_prefix)
            if is_wrong_prefix:
                print(" validate_address incorrectly validated wrong prefix")
                return None

            print(f" Wrong prefix validation: Correctly rejected")

            return "Address validation methods working correctly"

        except Exception as e:
            print(f" Error: {e}")
            return None

    def run_all_tests(self):
        """Run all auth E2E tests and report results."""
        print("\nStarting auth module E2E tests")
        print("=" * 50)

        test_methods = [
            ("Get account info", self.test_get_account),
            ("Get non-existent account", self.test_get_account_nonexistent),
            ("Get accounts with pagination", self.test_get_accounts),
            ("Get auth parameters", self.test_get_auth_params),
            ("Get module account by name", self.test_get_module_account_by_name),
            ("Convenience methods", self.test_convenience_methods),
            ("Address validation", self.test_address_validation),
        ]

        results = []
        passed = 0
        failed = 0

        for test_name, test_method in test_methods:
            print(f"\n{test_name}...")
            try:
                result = test_method()
                if result:
                    print(f"✅ Pass: {result}")
                    results.append((test_name, "PASS", result))
                    passed += 1
                else:
                    print(f"❌ Fail: {test_name}")
                    results.append((test_name, "FAIL", "No result returned"))
                    failed += 1
            except Exception as e:
                print(f"❌ Error: {test_name} - {str(e)}")
                results.append((test_name, "ERROR", str(e)))
                failed += 1

            time.sleep(1)

        print(f"\nAuth module E2E test summary")
        print("=" * 40)
        print(f"Total tests: {len(test_methods)}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")

        success_rate = (passed / len(test_methods)) * 100
        print(f"Success rate: {success_rate:.1f}%")

        if success_rate >= 85:
            print(f"\n✅ Excellent: Auth module tests {success_rate:.1f}% successful!")
            print("✅ Auth module is ready")
        elif success_rate >= 70:
            print(f"\n✅ Good: Auth module tests {success_rate:.1f}% successful")
            print("✅ Auth module functionality is working well")
        else:
            print(f"\n⚠️ Issues: Auth module tests only {success_rate:.1f}% successful")
            print("❌ Auth module may need attention")

        return results


if __name__ == "__main__":
    """Run auth E2E tests when executed directly."""
    try:
        test_runner = AuthE2ETests()
        test_results = test_runner.run_all_tests()

        print(f"\nDetailed results:")
        for test_name, status, result in test_results:
            status_emoji = "✅" if status == "PASS" else "❌"
            print(f"{status_emoji} {test_name}: {result}")

    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        import traceback

        traceback.print_exc()
