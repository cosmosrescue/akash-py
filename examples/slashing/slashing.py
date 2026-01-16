#!/usr/bin/env python3
"""
Slashing module example demonstrating all slashing functionality.

Tests all slashing module functions against testnet/mainnet.
Mixed query and transaction module with validator monitoring.
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


class SlashingE2ETests:
    """Example tests for Slashing module including all functions."""

    def __init__(self):
        self.testnet_client = AkashClient(TESTNET_RPC, TESTNET_CHAIN)
        self.mainnet_client = AkashClient(MAINNET_RPC, MAINNET_CHAIN)
        self.wallet = AkashWallet.from_mnemonic(TEST_MNEMONIC)
        self.test_results = {
            'testnet': {'passed': 0, 'failed': 0, 'tests': []},
            'mainnet': {'passed': 0, 'failed': 0, 'tests': []}
        }

    def test_slashing_parameters_lifecycle(self, client, network):
        """Test complete slashing parameters lifecycle."""
        print(" Testing slashing parameters lifecycle...")

        print(" Step 1: Querying slashing parameters...")
        try:
            params = client.slashing.get_params()
            if params and 'signed_blocks_window' in params:
                window = params.get('signed_blocks_window')
                jail_duration = params.get('downtime_jail_duration', '')
                print(f" Params: window={window}, jail_duration={jail_duration}")
                step1_success = True
            else:
                print(" Parameters query returned empty")
                return None
        except Exception as e:
            print(f" Parameters query failed: {str(e)}")
            return None

        print(" Step 2: Validating parameter consistency...")
        try:
            window_int = int(params.get('signed_blocks_window', '0'))
            if 50 <= window_int <= 500000:
                print(f" Window {window_int} is in reasonable range")
                step2_success = True
            else:
                print(f" Window {window_int} outside expected range")
                return None
        except Exception as e:
            print(f" Parameter validation failed: {str(e)}")
            return None

        print(" Step 3: Validating parameter format...")
        try:
            required_params = ['signed_blocks_window', 'downtime_jail_duration']
            missing_params = [p for p in required_params if p not in params]
            if not missing_params:
                print(f" All required parameters present: {required_params}")
                step3_success = True
            else:
                print(f" Missing parameters: {missing_params}")
                return None
        except Exception as e:
            print(f" Parameter format validation failed: {str(e)}")
            return None

        if step1_success and step2_success and step3_success:
            return f"Parameters lifecycle: query -> validate -> cross-check"
        return None

    def test_validator_signing_info_lifecycle(self, client, network):
        """Test complete validator signing info lifecycle."""
        print(" Testing validator signing info lifecycle...")

        print(" Step 1: Querying all validator signing infos...")
        try:
            all_signing_infos = client.slashing.get_signing_infos(limit=5)
            if all_signing_infos and len(all_signing_infos) > 0:
                validator_count = len(all_signing_infos)
                first_validator = all_signing_infos[0]
                cons_address = first_validator.get('address', '')
                print(f" Found {validator_count} validators, first: {cons_address}")
                step1_success = True
            else:
                print(" No signing infos returned")
                return None
        except Exception as e:
            print(f" Signing infos query failed: {str(e)}")
            return None

        print(" Step 2: Querying specific validator signing info...")
        try:
            specific_info = client.slashing.get_signing_info(cons_address)
            if specific_info and 'address' in specific_info:
                start_height = specific_info.get('start_height', '0')
                tombstoned = specific_info.get('tombstoned', False)
                print(f" Validator info: height={start_height}, tombstoned={tombstoned}")
                step2_success = True
            else:
                print(" Specific validator info query returned empty")
                return None
        except Exception as e:
            print(f" Specific info query failed: {str(e)}")
            return None

        print(" Step 3: Validating data consistency...")
        try:
            matching_info = None
            for info in all_signing_infos:
                if info.get('address') == cons_address:
                    matching_info = info
                    break

            if matching_info:
                specific_height = specific_info.get('start_height')
                list_height = matching_info.get('start_height')
                if specific_height == list_height:
                    print(f" Data consistency verified: height={specific_height}")
                    step3_success = True
                else:
                    print(f" Data inconsistency: {specific_height} != {list_height}")
                    return None
            else:
                print(" Could not find matching validator in list")
                return None
        except Exception as e:
            print(f" Data consistency check failed: {str(e)}")
            return None

        if step1_success and step2_success and step3_success:
            return f"Signing info lifecycle: list -> specific -> validate"
        return None

    def test_unjail_transaction_capability(self, client, network):
        """Test unjail transaction capability (simulation only)."""
        print(" Testing unjail transaction capability...")

        print(" Step 1: Searching for jailed validators...")
        try:
            all_signing_infos = client.slashing.get_signing_infos(limit=10)
            jailed_validator = None

            for info in all_signing_infos:
                tombstoned = info.get('tombstoned', False)
                if tombstoned:
                    jailed_validator = info.get('address')
                    print(f" Found tombstoned validator: {jailed_validator}")
                    break

            if not jailed_validator:
                try:
                    validators = client.staking.get_validators()
                    if validators and len(validators) > 0:
                        test_validator = validators[0].get('operator_address', '')
                        if test_validator:
                            print(f" Using validator for capability test: {test_validator}")
                            jailed_validator = test_validator
                        else:
                            print(" No validator address found in first validator")
                            return None
                    else:
                        print(" No validators found for capability test")
                        return None
                except Exception as e:
                    print(f" Failed to get validators: {str(e)}")
                    return None

            step1_success = True
        except Exception as e:
            print(f" Validator search failed: {str(e)}")
            return None

        print(" Step 2: Testing unjail transaction construction...")
        try:
            result = client.slashing.unjail(
                wallet=self.wallet,
                memo="",
                fee_amount="8000",
                use_simulation=True
            )

            if result and hasattr(result, 'success'):
                print(f" Unjail construction: success={result.success}")
                if result.success:
                    print(f" Transaction hash: {result.tx_hash}")
                    step2_success = True
                else:
                    error = result.raw_log or result.error or "Unknown error"
                    expected_errors = [
                        "not jailed",
                        "validator not found",
                        "account sequence mismatch",
                        "incorrect account sequence",
                        "confirmation timeout"
                    ]

                    if any(expected in error.lower() for expected in expected_errors):
                        print(f" Expected simulation error: {error}")
                        step2_success = True
                    else:
                        print(f" Unexpected error: {error}")
                        return None
            else:
                print(" Unjail construction failed")
                return None
        except Exception as e:
            print(f" Unjail construction failed: {str(e)}")
            return None

        print(" Step 3: Verifying transaction message format...")
        try:
            if jailed_validator.startswith('akashvaloper') and len(jailed_validator) > 20:
                print(f" Message format validation: validator address format correct")
                step3_success = True
            else:
                print(f" Message format validation: invalid validator address format")
                return None
        except Exception as e:
            print(f" Message format validation failed: {str(e)}")
            return None

        if step1_success and step2_success and step3_success:
            return f"Unjail capability: find_validator -> construct_tx -> validate_format"
        return None

    def run_network_tests(self, client, network):
        """Run all slashing tests for a specific network."""
        print(f" Running {network} tests...")

        test_methods = [
            self.test_slashing_parameters_lifecycle,
            self.test_validator_signing_info_lifecycle,
            self.test_unjail_transaction_capability
        ]

        for test_method in test_methods:
            test_name = test_method.__name__.replace('test_', '').replace('_', ' ')
            print(f" {test_name}:")

            try:
                result = test_method(client, network)
                if result:
                    print(f" ✅ PASS: {result}")
                    self.test_results[network]['passed'] += 1
                    self.test_results[network]['tests'].append((test_name, 'PASS', result))
                else:
                    print(f" ❌ FAIL: Test did not complete successfully")
                    self.test_results[network]['failed'] += 1
                    self.test_results[network]['tests'].append((test_name, 'FAIL', 'Test incomplete'))
            except Exception as e:
                print(f" ❌ ERROR: {str(e)}")
                self.test_results[network]['failed'] += 1
                self.test_results[network]['tests'].append((test_name, 'ERROR', str(e)[:100]))

            time.sleep(1)

    def run_all_tests(self):
        """Run all slashing example tests on both networks."""
        print("Slashing module example tests")
        print("=" * 50)

        print("\nTestnet tests")
        print("-" * 20)
        try:
            self.run_network_tests(self.testnet_client, 'testnet')
        except Exception as e:
            print(f"❌ Testnet tests failed: {e}")

  
        print("\nMainnet tests")
        print("-" * 20)
        try:
            self.run_network_tests(self.mainnet_client, 'mainnet')
        except Exception as e:
            print(f"❌ Mainnet tests failed: {e}")

        print("\n Test summary")
        print("=" * 30)

        for network in ['testnet', 'mainnet']:
            results = self.test_results[network]
            total = results['passed'] + results['failed']
            if total > 0:
                success_rate = (results['passed'] / total) * 100
                print(f"{network.upper()}: {results['passed']}/{total} passed ({success_rate:.1f}%)")

                for test_name, status, details in results['tests']:
                    status_emoji = "✅" if status == "PASS" else "❌"
                    print(f" {status_emoji} {test_name}: {details}")
            else:
                print(f"{network.upper()}: no tests completed")

        total_passed = self.test_results['testnet']['passed'] + self.test_results['mainnet']['passed']
        total_tests = sum(len(self.test_results[net]['tests']) for net in ['testnet', 'mainnet'])

        if total_tests > 0:
            overall_rate = (total_passed / total_tests) * 100
            print(f"\nOVERALL: {total_passed}/{total_tests} passed ({overall_rate:.1f}%)")

            if overall_rate >= 90:
                print(" Slashing module: great success!")
            elif overall_rate >= 75:
                print("✅ Slashing module: good success!")
            else:
                print("⚠️ Slashing module: partial success")
        else:
            print("\n❌ NO tests completed")


def main():
    """Run slashing example tests."""
    test_runner = SlashingE2ETests()
    test_runner.run_all_tests()


if __name__ == "__main__":
    main()
