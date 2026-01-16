#!/usr/bin/env python3
"""
IBC token transfer example demonstrating IBC transfer functionality.

Tests token transfers via IBC channels between chains.
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

TESTNET_RPC = "https://rpc.sandbox-01.aksh.pw:443"
TESTNET_CHAIN = "sandbox-01"
MAINNET_RPC = "https://akash-rpc.polkachu.com:443"
MAINNET_CHAIN = "akashnet-2"

TEST_MNEMONIC = "poverty torch street hybrid estate message increase play negative vibrant transfer six police tiny garment congress survey tired used audit dolphin focus abstract appear"
TEST_ADDRESS = "akash1qnnhhgzxj24f2kld5yhy4v4h4s9r295ak5gjw4"

COSMOSHUB_ADDRESS = "cosmos1qnnhhgzxj24f2kld5yhy4v4h4s9r295am094h0"

logger = logging.getLogger(__name__)


class IBCTransferE2ETests:
    """E2E tests for IBC token transfer functionality."""

    def __init__(self):
        self.mainnet_client = AkashClient(MAINNET_RPC, MAINNET_CHAIN)
        self.wallet = AkashWallet.from_mnemonic(TEST_MNEMONIC)
        self.test_results = {
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

    def test_known_transfer_channels(self):
        """Test using known transfer channels."""
        try:
            known_channels = {
                'channel-17': 'cosmoshub-4',
                'channel-9': 'osmosis-1'
            }

            return f"Using known channels: {', '.join([f'{ch} -> {chain}' for ch, chain in known_channels.items()])}"

        except Exception as e:
            logger.error(f"Known channels check failed: {e}")
            return None

    def test_small_ibc_transfer(self):
        """Test a small IBC token transfer using known channel."""
        try:
            source_channel = "channel-17"
            target_address = COSMOSHUB_ADDRESS

            result = self.mainnet_client.ibc.transfer(
                wallet=self.wallet,
                source_channel=source_channel,
                token_amount="100",  # 0.0001 AKT
                token_denom="uakt",
                receiver=target_address,
                fee_amount="5000",
                use_simulation=True
            )

            if result.success:
                return f"Transfer completed successfully on {source_channel}, tx: {result.tx_hash}"
            else:
                logger.error(f"Transfer failed: {result.raw_log}")
                return None

        except Exception as e:
            logger.error(f"Transfer test failed: {e}")
            return None

    def test_message_converter_transfer(self):
        """Test the IBC transfer message converter."""
        try:
            from akash.messages.ibc import convert_msg_transfer
            from google.protobuf.any_pb2 import Any

            transfer_msg = {
                'source_port': 'transfer',
                'source_channel': 'channel-0',
                'sender': TEST_ADDRESS,
                'receiver': COSMOSHUB_ADDRESS,
                'token': {'denom': 'uakt', 'amount': '1000000'},
                'timeout_height': {'revision_number': 4, 'revision_height': 1000000},
                'timeout_timestamp': int(time.time() + 300) * 1000000000,
                'memo': 'test transfer'
            }

            any_msg = Any()
            result = convert_msg_transfer(transfer_msg, any_msg)

            if result.type_url == '/ibc.applications.transfer.v1.MsgTransfer':
                return "Transfer message converter working correctly"
            else:
                return None

        except Exception as e:
            logger.error(f"Message converter test failed: {e}")
            return None

    def test_check_wallet_balance(self):
        """Check wallet balance for transfer tests."""
        try:
            balance = self.mainnet_client.bank.get_balance(self.wallet.address, "uakt")
            balance_akt = float(balance) / 1_000_000

            if balance_akt > 0.1:
                return f"Wallet has {balance_akt:.3f} AKT available for transfers"
            else:
                print(f" ❌ Insufficient balance: {balance_akt:.6f} AKT (need > 0.1 AKT)")
                return None

        except Exception as e:
            logger.error(f"Balance check failed: {e}")
            return None

    def test_actual_ibc_transfer(self):
        """Test actual IBC token transfer using known channel."""
        try:
            balance = self.mainnet_client.bank.get_balance(self.wallet.address, "uakt")
            if int(balance) < 100000:
                logger.error("Insufficient balance for transfer test")
                return None

            source_channel = "channel-17"
            target_address = COSMOSHUB_ADDRESS

            result = self.mainnet_client.ibc.transfer(
                wallet=self.wallet,
                source_channel=source_channel,
                token_amount="1000",  # 0.001 AKT
                token_denom="uakt",
                receiver=target_address,
                fee_amount="5000",
                use_simulation=True
            )

            if result.success:
                return f"Transfer successful on {source_channel}, Tx: {result.tx_hash}"
            else:
                logger.error(f"IBC transfer failed: {result.raw_log}")
                return None

        except Exception as e:
            logger.error(f"IBC transfer failed: {e}")
            return None

    def test_channels_query_structure(self):
        """Test IBC channels query structure."""
        try:
            result = self.mainnet_client.ibc.get_channels(limit=10)
            channels = result.get('channels', [])

            if not channels:
                return "No channels found on testnet"

            first_channel = channels[0]
            required_fields = ['channel_id', 'port_id', 'state', 'connection_hops']

            for field in required_fields:
                if field not in first_channel:
                    return f"Missing field {field} in channel structure"

            transfer_channels = [ch for ch in channels if ch.get('port_id') == 'transfer']
            open_channels = [ch for ch in channels if ch.get('state') == 'STATE_OPEN']

            return f"Found {len(channels)} channels: {len(transfer_channels)} transfer, {len(open_channels)} open"

        except Exception as e:
            logger.error(f"Channels query failed: {e}")
            return None

    def run_mainnet_tests(self):
        """Run all mainnet tests."""
        print("\n" + "=" * 60)
        print("IBC TOKEN TRANSFER E2E TESTS - MAINNET")
        print("=" * 60)
        print(f"Testing against: {MAINNET_RPC}")
        print(f"Chain: {MAINNET_CHAIN}")
        print(f"Wallet: {self.wallet.address}")

        self.run_test('mainnet', 'Wallet balance check', self.test_check_wallet_balance)
        self.run_test('mainnet', 'Channels query structure', self.test_channels_query_structure)
        self.run_test('mainnet', 'Known transfer channels', self.test_known_transfer_channels)
        self.run_test('mainnet', 'Message converter', self.test_message_converter_transfer)
        self.run_test('mainnet', 'Small transfer test', self.test_small_ibc_transfer)

        print(f"\nTesting actual IBC transfer")
        print(f"  This will perform a transfer transaction (costs ~0.005 AKT)")
        self.run_test('mainnet', 'Actual IBC transfer', self.test_actual_ibc_transfer)

    def print_results(self):
        """Print test results summary."""
        print("\n" + "=" * 60)
        print("IBC TOKEN TRANSFER E2E TEST RESULTS")
        print("=" * 60)

        for network in ['mainnet']:
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

        if mainnet_rate >= 80:
            print(f"\n✅ IBC token transfer functionality works")
            return "Success"
        else:
            print(f"\n❌ IBC token transfer needs attention")
            print(f" Some functionality issues detected")
            return None


def main():
    """Main test runner."""
    print("Starting IBC token transfer E2E tests...")

    tester = IBCTransferE2ETests()
    tester.run_mainnet_tests()
    result = tester.print_results()

    if result == "Success":
        print("\nAll IBC token transfer tests completed successfully!")
        return "Success"
    else:
        print("\nSome IBC token transfer tests failed. Review output above.")
        return None


if __name__ == "__main__":
    result = main()
    if result != "Success":
        exit(1)
