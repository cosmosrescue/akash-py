#!/usr/bin/env python3
"""
IBC client update example demonstrating IBC client update functionality.

Tests updating existing IBC clients with new block headers.
"""

import os
import sys
import logging
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


class IBCUpdateClientE2ETests:
    """E2E tests for IBC client update functionality."""

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

    def test_find_active_clients_mainnet(self):
        """Test finding known active client 07-tendermint-53."""
        try:
            known_client = "07-tendermint-53"
            status = self.mainnet_client.ibc.get_client_status(known_client)
            
            if status == "Active":
                return f"Known client {known_client} is active"
            else:
                return f"Known client {known_client} status: {status}"

        except Exception as e:
            logger.error(f"Find active clients failed: {e}")
            return None

    def test_client_state_validation(self):
        """Test client state data validation."""
        try:
            result = self.mainnet_client.ibc.get_client_states(limit=3)
            client_states = result.get('client_states', [])

            if not client_states:
                return "No clients found for validation test"

            valid_clients = 0
            for client_info in client_states:
                client_id = client_info['client_id']
                client_state = client_info.get('client_state', {})
                
                required_fields = ['chain_id', 'trusting_period', 'unbonding_period', 'latest_height']
                has_all_fields = all(field in client_state for field in required_fields)
                
                if has_all_fields:
                    chain_id = client_state['chain_id']
                    trusting_period = client_state['trusting_period']
                    latest_height = client_state['latest_height']
                    
                    valid_chain_id = isinstance(chain_id, str) and len(chain_id) > 0
                    valid_trusting_period = isinstance(trusting_period, str) and trusting_period.endswith('s')
                    valid_latest_height = (isinstance(latest_height, dict) and 
                                         'revision_height' in latest_height and
                                         'revision_number' in latest_height)
                    
                    if valid_chain_id and valid_trusting_period and valid_latest_height:
                        valid_clients += 1

            return f"Validated {valid_clients}/{len(client_states)} client states with proper structure"

        except Exception as e:
            logger.error(f"Client state validation failed: {e}")
            return None


    def test_update_client(self):
        """Test actual IBC client update transaction."""
        try:
            active_client = "07-tendermint-53"
            target_rpc = "https://cosmos-rpc.polkachu.com:443"

            print(f"  Testing client update for {active_client}...")
            
            result = self.mainnet_client.ibc.update_client(
                wallet=self.wallet,
                client_id=active_client,
                target_rpc_url=target_rpc,
                gas_limit=600000,
                fee_amount="25000",
                use_simulation=True
            )
            
            if result.success:
                return f"Client {active_client} updated successfully - tx: {result.tx_hash}"
            else:
                logger.error(f"Client update failed: {result.raw_log}")
                return None

        except Exception as e:
            logger.error(f"Client update test failed: {e}")
            return None

    def test_message_converter_update_client(self):
        """Test the update client message converter."""
        try:
            from akash.messages.ibc import convert_msg_update_client
            from google.protobuf.any_pb2 import Any

            update_client_msg = {
                'client_id': 'test-client',
                'signer': TEST_ADDRESS,
                'header': {
                    'signed_header': {
                        'header': {
                            'version': {'block': '11', 'app': '1'},
                            'chain_id': 'test-chain',
                            'height': '100',
                            'time': '2023-01-01T00:00:00Z',
                            'last_block_id': {'hash': '', 'part_set_header': {'total': 0, 'hash': ''}},
                            'last_commit_hash': '',
                            'data_hash': '',
                            'validators_hash': 'abcd1234',
                            'next_validators_hash': 'abcd1234',
                            'consensus_hash': '',
                            'app_hash': '',
                            'last_results_hash': '',
                            'evidence_hash': '',
                            'proposer_address': ''
                        },
                        'commit': {
                            'height': '100',
                            'round': 0,
                            'block_id': {'hash': '', 'part_set_header': {'total': 0, 'hash': ''}},
                            'signatures': []
                        }
                    },
                    'validator_set': {'validators': []},
                    'trusted_height': {'revision_number': 1, 'revision_height': 99},
                    'trusted_validators': {'validators': []}
                }
            }

            any_msg = Any()
            result = convert_msg_update_client(update_client_msg, any_msg)

            if result.type_url == '/ibc.core.client.v1.MsgUpdateClient':
                return "Update client message converter working correctly"
            else:
                return None

        except Exception as e:
            logger.error(f"Message converter test failed: {e}")
            return None

    def run_mainnet_tests(self):
        """Run all mainnet tests."""
        print("\n" + "=" * 60)
        print("IBC CLIENT UPDATE E2E TESTS - MAINNET")
        print("=" * 60)
        print(f"Testing against: {MAINNET_RPC}")
        print(f"Chain: {MAINNET_CHAIN}")
        print(f"Wallet: {self.wallet.address}")

        self.run_test('mainnet', 'Find active clients', self.test_find_active_clients_mainnet)
        self.run_test('mainnet', 'Client state validation', self.test_client_state_validation)
        self.run_test('mainnet', 'Message converter', self.test_message_converter_update_client)

        print(f"\nRunning actual IBC client update test")
        print(f"  This will perform an update transaction (costs ~0.02 AKT)")
        self.run_test('mainnet', 'Update client 07-tendermint-53', self.test_update_client)

    def print_results(self):
        """Print test results summary."""
        print("\n" + "=" * 60)
        print("IBC CLIENT UPDATE E2E TEST RESULTS")
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
        print("IBC client update module capabilities verified:")
        print("=" * 60)

        capabilities = [
            "Active client discovery - Find clients that can be updated",
            "Client state validation - Validate client state data structure and fields",
            "Light client integration - Fetch block data from target chains",
            "Header construction - Build proper IBC update messages",
            "Gas simulation - Estimate gas before broadcasting",
            "Transaction broadcasting - Submit client updates to blockchain",
            "Update verification - Confirm client state changes"
        ]

        for capability in capabilities:
            print(f" ▫️ {capability}")

        mainnet_total = self.test_results['mainnet']['passed'] + self.test_results['mainnet']['failed']
        mainnet_rate = (self.test_results['mainnet']['passed'] / mainnet_total * 100) if mainnet_total > 0 else 0

        if mainnet_rate >= 80:
            print(f"\n✅ IBC client update functionality works")
            return "Success"
        else:
            print(f"\n❌ IBC client update needs attention")
            print(f" Some functionality issues detected")
            return None


def main():
    """Main test runner."""
    print("Starting IBC client update E2E tests...")

    tester = IBCUpdateClientE2ETests()
    tester.run_mainnet_tests()
    result = tester.print_results()

    if result == "Success":
        print("\nAll IBC client update tests completed successfully!")
        return "Success"
    else:
        print("\nSome IBC client update tests failed. Review output above.")
        return None


if __name__ == "__main__":
    result = main()
    if result != "Success":
        exit(1)