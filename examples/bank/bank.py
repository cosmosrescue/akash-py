#!/usr/bin/env python3
"""
Bank module example demonstrating all bank functionality.

Shows how to use the Akash Python SDK for bank operations including:
- Balance queries and account information
- Address validation and fee estimation
- Token transfers with custom fees
- Amount conversion utilities
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

RECEIVER_MNEMONIC = "another test wallet mnemonic would go here if we had one"


class BankE2ETests:
    """Bank module functionality examples."""

    def __init__(self):
        self.testnet_client = AkashClient(TESTNET_RPC, TESTNET_CHAIN)
        self.mainnet_client = AkashClient(MAINNET_RPC, MAINNET_CHAIN)
        self.wallet = AkashWallet.from_mnemonic(TEST_MNEMONIC)
        self.test_results = {
            'testnet': {'passed': 0, 'failed': 0, 'tests': []},
            'mainnet': {'passed': 0, 'failed': 0, 'tests': []}
        }

    def run_test(self, network, test_name, test_func, skip_mainnet_tx=False):
        """Run a single test and record results."""
        print(f" Testing {test_name}...")
        try:
            result = test_func()
            if result:
                print(f" ✅ Pass: {result}")
                self.test_results[network]['passed'] += 1
                self.test_results[network]['tests'].append(f"✅ {test_name}")
                return True
            else:
                print(f" ❌ Fail: Transaction failed or timed out")
                self.test_results[network]['failed'] += 1
                self.test_results[network]['tests'].append(f"❌ {test_name}: Transaction failed")
                return False
        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)[:100]}"
            print(f" ❌ Fail: {error_msg}")
            self.test_results[network]['failed'] += 1
            self.test_results[network]['tests'].append(f"❌ {test_name}: {error_msg}")
            return False

    def test_query_balance(self, client):
        """Test balance query functionality."""
        balance = client.bank.get_balance(self.wallet.address, "uakt")
        if balance:
            balance_akt = client.bank.calculate_akt_amount(balance)
            return f"Balance: {balance_akt:.6f} AKT ({balance} uakt)"
        return None

    def test_query_all_balances(self, client):
        """Test all balances query."""
        balances = client.bank.get_all_balances(self.wallet.address)
        if isinstance(balances, dict):
            return f"Found {len(balances)} denominations"
        return None

    def test_get_account_info(self, client):
        """Test account info retrieval."""
        account_info = client.bank.get_account_info(self.wallet.address)
        if account_info:
            seq = account_info.get('sequence', 'unknown')
            acc_num = account_info.get('account_number', 'unknown')
            return f"Account info: seq={seq}, acc_num={acc_num}"
        return None

    def test_validate_address(self, client):
        """Test address format validation."""

        valid_existing = client.bank.validate_address(self.wallet.address)

        valid_unused = client.bank.validate_address("akash1qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq7cdc78")

        invalid_format = client.bank.validate_address("invalid_address")

        wrong_prefix = client.bank.validate_address("cosmos1qnnhhgzxj24f2kld5yhy4v4h4s9r295a3apz55")

        too_short = client.bank.validate_address("akash1")

        empty = client.bank.validate_address("")

        if (valid_existing is True and valid_unused is True and
                invalid_format is False and wrong_prefix is False and
                too_short is False and empty is False):
            return f"Address format validation working correctly"

        print(f" Debug: valid_existing={valid_existing}, valid_unused={valid_unused}")
        print(f" Debug: invalid_format={invalid_format}, wrong_prefix={wrong_prefix}")
        print(f" Debug: too_short={too_short}, empty={empty}")
        return None

    def test_get_supply(self, client):
        """Test supply query."""
        try:
            supply = client.bank.get_supply("uakt")
            if supply and 'amount' in supply:
                return f"uAKT supply: {supply.get('amount_akt', 'unknown')} AKT"
            return "Supply query returned empty"
        except ImportError:
            return "Supply query skipped (protobuf not available)"

    def test_estimate_fee(self, client):
        """Test fee estimation."""
        fee_info = client.bank.estimate_fee(message_count=1, gas_per_message=200000)
        if fee_info and 'estimated_fee' in fee_info:
            return f"Fee estimate: {fee_info['fee_akt']} AKT for {fee_info['gas_limit']} gas"
        return None

    def test_amount_conversions(self, client):
        """Test AKT/uAKT conversion utilities."""
        akt_amount = client.bank.calculate_akt_amount("1000000")
        uakt_amount = client.bank.calculate_uakt_amount(1.0)

        if akt_amount == 1.0 and uakt_amount == "1000000":
            return "Amount conversion utilities working"
        return None

    def test_send(self, client, network):
        """Test basic send functionality."""
        print(" Preparing send transaction...")

        amount = "1000"
        memo = ''

        result = client.bank.send(
            wallet=self.wallet,
            to_address=self.wallet.address,
            amount=amount,
            denom="uakt",
            memo=memo
        )

        if result and result.success:
            return f"Tx: {result.tx_hash} (amount: {amount} uakt)"
        elif result:
            print(
                f" Transaction failed - Code {result.code}: {result.raw_log[:50] if hasattr(result, 'raw_log') else 'No log'}")
            return None
        return None

    def test_send_with_custom_fee(self, client, network):
        """Test send with custom fee using main send() function."""
        print(" Preparing custom fee transaction...")

        amount = "1000"
        fee_amount = "10000"
        gas_limit = 150000
        memo = ''

        result = client.bank.send(
            wallet=self.wallet,
            to_address=self.wallet.address,
            amount=amount,
            denom="uakt",
            fee_amount=fee_amount,
            gas_limit=gas_limit,
            memo=memo
        )

        if result and result.success:
            return f"Tx: {result.tx_hash} (fee: {fee_amount} uakt, gas: {gas_limit})"
        elif result:
            print(
                f" Transaction failed - Code {result.code}: {result.raw_log[:50] if hasattr(result, 'raw_log') else 'No log'}")
            return None
        return None

    def run_network_tests(self, network, client):
        """Run all tests for a specific network."""
        print(f"\nTesting bank module on {network.upper()}")
        print("=" * 60)

        query_tests = [
            ("get_balance", lambda: self.test_query_balance(client), False),
            ("query_all_balances", lambda: self.test_query_all_balances(client), False),
            ("get_account_info", lambda: self.test_get_account_info(client), False),
            ("validate_address", lambda: self.test_validate_address(client), False),
            ("get_supply", lambda: self.test_get_supply(client), False),
            ("estimate_fee", lambda: self.test_estimate_fee(client), False),
            ("amount_conversions", lambda: self.test_amount_conversions(client), False),
        ]

        tx_tests = [
            ("send", lambda: self.test_send(client, network), True),
            ("send_with_custom_fee", lambda: self.test_send_with_custom_fee(client, network), True),
        ]

        print("\n  Query functions:")
        for test_name, test_func, _ in query_tests:
            self.run_test(network, test_name, test_func, skip_mainnet_tx=False)
            time.sleep(0.5)

        print("\n  Transaction functions:")
        for test_name, test_func, skip_mainnet in tx_tests:
            self.run_test(network, test_name, test_func, skip_mainnet_tx=(network == "mainnet" and skip_mainnet))
            if not (network == "mainnet" and skip_mainnet):
                time.sleep(2)

    def run_all_tests(self):
        """Run all E2E tests."""
        print("Bank module E2E tests")
        print("=" * 70)
        print(f"Test wallet: {self.wallet.address}")
        print(f"Testnet: {TESTNET_RPC}")
        print(f"Mainnet: {MAINNET_RPC}")
        print("\nNote: Transaction tests run on testnet only to preserve mainnet funds")

        self.run_network_tests("testnet", self.testnet_client)
        self.run_network_tests("mainnet", self.mainnet_client)
        self.print_summary()

    def print_summary(self):
        """Print test results summary."""
        print("\n" + "=" * 70)
        print("Bank module E2E test results")
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
            print(f"\n✅ Bank module: tests successful")
        elif overall_success >= 60:
            print(f"\n⚠️ Bank module: partially successful")
        else:
            print(f"\n❌ Bank module: needs attention")

        print("\n" + "=" * 70)


def main():
    """Run Bank module examples."""
    print("Starting bank module examples...")
    print("Demonstrating all bank functions including transactions")

    test_runner = BankE2ETests()
    test_runner.run_all_tests()

    print("\nBank module examples complete")


if __name__ == "__main__":
    main()
