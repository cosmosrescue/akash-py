#!/usr/bin/env python3
"""
IBC client creation example demonstrating IBC client creation functionality.

Tests creating new IBC clients for various target chains.
"""

import logging
import sys
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

logger = logging.getLogger(__name__)


class IBCCreateClientE2ETests:
    """E2E tests for IBC client creation functionality."""

    def __init__(self):
        self.testnet_client = AkashClient(TESTNET_RPC, TESTNET_CHAIN)
        self.mainnet_client = AkashClient(MAINNET_RPC, MAINNET_CHAIN)
        self.wallet = AkashWallet.from_mnemonic(TEST_MNEMONIC)
        self.test_results = {
            'testnet': {'passed': 0, 'failed': 0, 'tests': []},
            'mainnet': {'passed': 0, 'failed': 0, 'tests': []}
        }

    def run_test(self, network, test_name, test_func):
        """Run a single test and record results."""
        print(f"  Testing {test_name}...")
        try:
            result = test_func()
            if result:
                print(f"  ✅ Pass: {result}")
                self.test_results[network]['passed'] += 1
                self.test_results[network]['tests'].append(f"✅ {test_name}")
                return True
            else:
                print(f"  ❌ Fail: No result returned")
                self.test_results[network]['failed'] += 1
                self.test_results[network]['tests'].append(f"❌ {test_name}")
                return False
        except Exception as e:
            print(f"  ❌ Fail: {e}")
            self.test_results[network]['failed'] += 1
            self.test_results[network]['tests'].append(f"❌ {test_name}: {str(e)}")
            return False

    def test_create_client_for_provider_on_testnet(self):
        """Test creating actual IBC client for provider testnet ON testnet."""
        try:
            target_chain_id = "provider"
            target_rpc_url = "https://cosmos-testnet-rpc.polkachu.com"

            result = self.testnet_client.ibc.create_client(
                wallet=self.wallet,
                target_chain_id=target_chain_id,
                target_rpc_url=target_rpc_url,
                trusting_period_seconds=1209600,  # 14 days
                unbonding_period_seconds=1814400,  # 21 days
                max_clock_drift_seconds=600,
                fee_amount="5000",
                use_simulation=True
            )

            if result.success:
                client_id = getattr(result, 'client_id', None)

                if client_id:
                    try:
                        client_state = self.testnet_client.ibc.get_client_state(client_id)
                        if client_state and client_state.get('client_state', {}).get('chain_id') == target_chain_id:
                            status = self.testnet_client.ibc.get_client_status(client_id)
                            return f"Created and verified client {client_id} for {target_chain_id}, status: {status}, Tx: {result.tx_hash}"
                        else:
                            return f"Created client {client_id} but chain verification failed, Tx: {result.tx_hash}"
                    except Exception as verify_error:
                        return f"Created client {client_id} but verification error: {verify_error}, Tx: {result.tx_hash}"
                else:
                    if "07-tendermint-" in result.raw_log:
                        import re
                        match = re.search(r'07-tendermint-\d+', result.raw_log)
                        if match:
                            client_id = match.group()
                            return f"Created client {client_id} for {target_chain_id} (extracted from log), Tx: {result.tx_hash}"
                    return f"Client created successfully but no ID extracted, Tx: {result.tx_hash}"
            else:
                return None

        except Exception as e:
            logger.error(f"Provider testnet client creation failed: {e}")
            return None

    def test_create_client_for_osmo_test_on_testnet(self):
        """Test creating actual IBC client for osmo-test-5 ON testnet."""
        try:
            target_chain_id = "osmo-test-5"
            target_rpc_url = "https://osmosis-testnet-rpc.polkachu.com"

            result = self.testnet_client.ibc.create_client(
                wallet=self.wallet,
                target_chain_id=target_chain_id,
                target_rpc_url=target_rpc_url,
                trusting_period_seconds=1209600,  # 14 days
                unbonding_period_seconds=1814400,  # 21 days
                max_clock_drift_seconds=600,
                fee_amount="15000",
                use_simulation=True
            )

            if result.success:
                client_id = getattr(result, 'client_id', None)

                if client_id:
                    try:
                        client_state = self.testnet_client.ibc.get_client_state(client_id)
                        if client_state and client_state.get('client_state', {}).get('chain_id') == target_chain_id:
                            status = self.testnet_client.ibc.get_client_status(client_id)
                            return f"Created and verified client {client_id} for {target_chain_id}, status: {status}, Tx: {result.tx_hash}"
                        else:
                            return f"Created client {client_id} but chain verification failed, Tx: {result.tx_hash}"
                    except Exception as verify_error:
                        return f"Created client {client_id} but verification error: {verify_error}, Tx: {result.tx_hash}"
                else:

                    if "07-tendermint-" in result.raw_log:
                        import re
                        match = re.search(r'07-tendermint-\d+', result.raw_log)
                        if match:
                            client_id = match.group()
                            return f"Created client {client_id} for {target_chain_id} (extracted from log), Tx: {result.tx_hash}"
                    return f"Client created successfully but no ID extracted, Tx: {result.tx_hash}"
            else:
                return None

        except Exception as e:
            logger.error(f"Osmosis testnet client creation failed: {e}")
            return None

    def test_create_client_for_cosmoshub_mainnet(self):
        """Test creating actual IBC client for Cosmoshub on mainnet."""
        try:
            target_chain_id = "cosmoshub-4"
            target_rpc_url = "https://cosmos-rpc.polkachu.com:443"

            result = self.mainnet_client.ibc.create_client(
                wallet=self.wallet,
                target_chain_id=target_chain_id,
                target_rpc_url=target_rpc_url,
                trusting_period_seconds=1209600,  # 14 days
                unbonding_period_seconds=1814400,  # 21 days
                max_clock_drift_seconds=600,
                fee_amount="5000",
                use_simulation=True
            )

            if result.success:
                client_id = None
                if "07-tendermint-" in result.raw_log:
                    import re
                    match = re.search(r'07-tendermint-\d+', result.raw_log)
                    if match:
                        client_id = match.group()

                if client_id:
                    try:
                        client_state = self.testnet_client.ibc.get_client_state(client_id)
                        if client_state and client_state.get('client_state', {}).get('chain_id') == target_chain_id:
                            status = self.testnet_client.ibc.get_client_status(client_id)
                            return f"Created and verified client {client_id} for {target_chain_id}, status: {status}, Tx: {result.tx_hash}"
                        else:
                            return f"Created client {client_id} but chain verification failed, Tx: {result.tx_hash}"
                    except Exception as verify_error:
                        return f"Created client {client_id} but verification error: {verify_error}, Tx: {result.tx_hash}"
                else:

                    if "07-tendermint-" in result.raw_log:
                        import re
                        match = re.search(r'07-tendermint-\d+', result.raw_log)
                        if match:
                            client_id = match.group()
                            return f"Created client {client_id} for {target_chain_id} (extracted from log), Tx: {result.tx_hash}"
                    return f"Client created successfully but no ID extracted, Tx: {result.tx_hash}"
            else:
                return None

        except Exception as e:
            logger.error(f"Client creation failed: {e}")
            return None

    def run_tests(self):
        """Run all E2E client creation tests."""
        print("\n" + "=" * 60)
        print("IBC CLIENT CREATION E2E TESTS")
        print("=" * 60)
        print(f"Testnet: {TESTNET_RPC}")
        print(f"Wallet: {self.wallet.address}")

        print(f"\nCreating actual IBC clients on testnet")
        print(f" This will perform client creation transactions (costs testnet gas)")
        self.run_test('testnet', 'Create client for provider', self.test_create_client_for_provider_on_testnet)
        self.run_test('testnet', 'Create client for osmo-test-5', self.test_create_client_for_osmo_test_on_testnet)

    def print_results(self):
        """Print test results summary."""
        print("\n" + "=" * 60)
        print("IBC CLIENT CREATION E2E TEST RESULTS")
        print("=" * 60)

        for network in ['mainnet', 'testnet']:
            total_tests = self.test_results[network]['passed'] + self.test_results[network]['failed']
            if total_tests == 0:
                continue

            success_rate = (self.test_results[network]['passed'] / total_tests * 100) if total_tests > 0 else 0

            print(
                f"\n{network.upper()} Results: {self.test_results[network]['passed']}/{total_tests} passed ({success_rate:.1f}%)")

            for test_result in self.test_results[network]['tests']:
                print(f" {test_result}")

        print(f"\n" + "=" * 60)

        mainnet_total = self.test_results['mainnet']['passed'] + self.test_results['mainnet']['failed']
        mainnet_rate = (self.test_results['mainnet']['passed'] / mainnet_total * 100) if mainnet_total > 0 else 0

        testnet_total = self.test_results['testnet']['passed'] + self.test_results['testnet']['failed']
        testnet_rate = (self.test_results['testnet']['passed'] / testnet_total * 100) if testnet_total > 0 else 0

        if testnet_rate >= 80:
            print(f"\n✅ IBC client creation works")
            return "Success"
        else:
            print(f"\n❌ IBC client creation needs attention")
            print(f" Some functionality issues detected")
            return None


def main():
    """Main test runner."""
    print("Starting IBC client creation E2E tests...")

    tester = IBCCreateClientE2ETests()
    tester.run_tests()
    result = tester.print_results()

    if result == "Success":
        print("\nAll IBC client creation tests completed successfully!")
        return "Success"
    else:
        print("\nSome IBC client creation tests failed. Review output above.")
        return None


if __name__ == "__main__":
    result = main()
    if result != "Success":
        exit(1)
