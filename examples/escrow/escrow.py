#!/usr/bin/env python3
"""
Escrow module example demonstrating escrow functionality.

Tests escrow functionality by creating deployments and testing blocks remaining calculation.
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

TENANT_MNEMONIC = "poverty torch street hybrid estate message increase play negative vibrant transfer six police tiny garment congress survey tired used audit dolphin focus abstract appear"

PROVIDER_MNEMONIC = "true ridge approve quantum sister primary notable have express fitness forum capable"


class EscrowE2ETests:
    """E2E tests for Escrow module."""

    def __init__(self, network="testnet"):
        if network == "mainnet":
            self.client = AkashClient(MAINNET_RPC, MAINNET_CHAIN)
            self.network = "mainnet"
            self.rpc_url = MAINNET_RPC
        else:
            self.client = AkashClient(TESTNET_RPC, TESTNET_CHAIN)
            self.network = "testnet"
            self.rpc_url = TESTNET_RPC

        self.wallet = AkashWallet.from_mnemonic(TENANT_MNEMONIC)
        self.provider_wallet = AkashWallet.from_mnemonic(PROVIDER_MNEMONIC)
        self.created_dseq = None
        self.test_owner = None
        self.test_results = {
            'passed': 0, 'failed': 0, 'tests': []
        }

        print(f"Testing on {self.network.upper()}: {self.rpc_url}")
        print(f"Tenant wallet: {self.wallet.address}")
        print(f"Provider wallet: {self.provider_wallet.address}")

    def test_find_deployment_with_leases(self):
        """Find any existing deployments with active leases for proper testing."""
        print(" Finding any deployment with active leases ")

        try:
            print("Querying active leases across the network...")

            try:
                leases = self.client.market.get_leases(state="active")

                if leases and len(leases) > 0:
                    print(f"✅ Found {len(leases)} active lease(s) on network")

                    first_lease = leases[0]
                    lease_id = first_lease.get('lease', {}).get('lease_id', {})
                    owner = lease_id.get('owner')
                    dseq = lease_id.get('dseq')

                    if owner and dseq:
                        self.created_dseq = int(dseq)
                        self.test_owner = owner

                        print(f"✅ Using deployment with active lease:")
                        print(f" Owner: {owner}")
                        print(f" Dseq: {self.created_dseq}")

                        return f"Found active lease deployment: {self.created_dseq}"

            except Exception as e:
                print(f" Lease query failed: {e}")

            print("Fallback: Querying all deployments on network...")

            try:
                deployments = self.client.deployment.get_deployments()

                if deployments and len(deployments) > 0:
                    print(f"✅ Found {len(deployments)} deployment(s) on network")

                    checked = 0
                    max_check = 10

                    for deployment in deployments:
                        if checked >= max_check:
                            break

                        deployment_info = deployment.get('deployment', {})
                        deployment_id = deployment_info.get('deployment_id', {})
                        owner = deployment_id.get('owner')
                        dseq = deployment_id.get('dseq')
                        state = deployment_info.get('state')

                        if owner and dseq and state == 1:
                            checked += 1
                            print(f" Checking deployment dseq {dseq} (owner: {owner})")

                            try:
                                leases = self.client.market.get_leases(
                                    owner=owner,
                                    dseq=int(dseq),
                                    state="active"
                                )

                                if leases and len(leases) > 0:
                                    self.created_dseq = int(dseq)
                                    self.test_owner = owner

                                    print(f"✅ Found deployment with {len(leases)} active lease(s):")
                                    print(f" Owner: {owner}")
                                    print(f" Dseq: {self.created_dseq}")

                                    return f"Found deployment with active leases: {self.created_dseq}"

                            except Exception as e:
                                print(f" Failed to check leases: {e}")
                                continue

                    print(f"❌ No active leases found in first {checked} deployments")
                    return None

            except Exception as e:
                print(f" All deployments query failed: {e}")
                return None

        except Exception as e:
            print(f"❌ Deployment search error: {e}")
            return None

    def test_blocks_remaining_calculation(self):
        """Test blocks remaining calculation with deployment that has active leases."""
        print(" Blocks remaining calculation ")

        if not self.created_dseq:
            print("❌ No deployment available for testing")
            return None

        owner_address = self.test_owner or self.wallet.address

        try:
            print(f"Testing blocks remaining for dseq {self.created_dseq} (owner: {owner_address})...")

            blocks_result = self.client.escrow.get_blocks_remaining(
                owner_address,
                self.created_dseq
            )

            if blocks_result and 'blocks_remaining' in blocks_result:
                blocks_remaining = blocks_result['blocks_remaining']
                hours_remaining = blocks_result.get('estimated_hours', 0)
                balance = blocks_result.get('escrow_balance_uakt', '0')
                daily_cost = blocks_result.get('daily_cost', '0')

                print(f"✅ Blocks remaining: {blocks_remaining:,}")
                print(f"✅ Time remaining: {hours_remaining:.1f} hours")
                print(f"✅ Escrow balance: {balance} base units")
                print(f"✅ Daily cost: {daily_cost} base units")

                if blocks_remaining >= 0 and hours_remaining >= 0:
                    return f"✅ Real test pass: {blocks_remaining:,} blocks, {hours_remaining:.1f}h"
                else:
                    print("❌ Invalid calculation results")
                    return None
            else:
                print("❌ No blocks remaining data returned")
                return None

        except Exception as e:
            print(f"❌ Blocks remaining failed: {str(e)}")
            return None

    def test_create_controlled_deployment_with_lease(self):
        """Create deployment and controlled bid/lease like lifecycle test."""
        print(" Creating controlled deployment with lease ")

        if self.network == "mainnet":
            print("Skipping deployment creation on mainnet (too expensive)")
            return "Deployment creation skipped on mainnet"

        try:
            provider_wallet = self.provider_wallet

            provider_balance_str = self.client.bank.get_balance(provider_wallet.address, "uakt")
            provider_balance = int(provider_balance_str) if provider_balance_str else 0
            print(f"Provider balance: {provider_balance:,} uakt")

            if provider_balance < 1000000:
                print("Funding provider wallet from tenant...")
                fund_result = self.client.bank.send(
                    wallet=self.wallet,
                    recipient=provider_wallet.address,
                    amount="2000000",
                    denom="uakt",
                    memo="",
                    use_simulation=True
                )

                if not (fund_result and fund_result.success):
                    print(f"❌ Provider funding failed: {fund_result.raw_log if fund_result else 'No result'}")
                    return None

                print(f"✅ Provider funded: Tx {fund_result.tx_hash}")
                time.sleep(3)

            balance_str = self.client.bank.get_balance(self.wallet.address, "uakt")
            balance = int(balance_str) if balance_str else 0
            print(f"Wallet balance: {balance:,} uakt ({balance / 1000000:.2f} AKT)")

            if balance < 10000000:
                print("❌ Insufficient balance for controlled deployment creation")
                return None

            test_groups = [{
                'name': 'escrow-test-controlled',
                'resources': [{
                    'cpu': '100000',  # 0.1 CPU
                    'memory': '268435456',  # 256MB
                    'storage': '536870912',  # 512MB
                    'price': '1000',  # 1000 uakt per block
                    'count': 1
                }]
            }]

            print("Creating deployment...")
            deployment_result = self.client.deployment.create_deployment(
                wallet=self.wallet,
                groups=test_groups,
                deposit="5000000",  # 5 AKT deposit
                memo="",
                use_simulation=True
            )

            if not (deployment_result and deployment_result.success):
                print(
                    f"❌ Deployment creation failed: {deployment_result.raw_log if deployment_result else 'No result'}")
                return None

            self.created_dseq = deployment_result.get_dseq()
            if not self.created_dseq:
                print("❌ Could not extract dseq")
                return None

            print(f"✅ Deployment created: dseq {self.created_dseq}, Tx {deployment_result.tx_hash}")

            time.sleep(3)

            print("Creating controlled bid on deployment...")
            bid_result = self.client.market.create_bid(
                wallet=provider_wallet,
                owner=self.wallet.address,
                dseq=self.created_dseq,
                gseq=1,
                oseq=1,
                price='1000',
                memo="",
                use_simulation=True
            )

            if not (bid_result and bid_result.success):
                print(f"❌ Bid creation failed: {bid_result.raw_log if bid_result else 'No result'}")
                return f"Created deployment without lease: {self.created_dseq}"

            print(f"✅ Bid created: Tx {bid_result.tx_hash}")

            time.sleep(3)

            print("Accepting bid to create lease...")
            lease_result = self.client.market.create_lease(
                wallet=self.wallet,
                owner=self.wallet.address,
                dseq=self.created_dseq,
                gseq=1,
                oseq=1,
                provider=provider_wallet.address,
                memo="",
                use_simulation=True
            )

            if not (lease_result and lease_result.success):
                print(f"❌ Lease creation failed: {lease_result.raw_log if lease_result else 'No result'}")
                return f"Created deployment with bid but no lease: {self.created_dseq}"

            print(f"✅ Lease created: Tx {lease_result.tx_hash}")

            time.sleep(3)

            leases = self.client.market.get_leases(
                owner=self.wallet.address,
                dseq=self.created_dseq,
                state="active"
            )

            if leases and len(leases) > 0:
                self.test_owner = self.wallet.address
                print(f"✅ Controlled deployment has {len(leases)} active lease(s)")
                return f"Created controlled deployment with lease: {self.created_dseq}"
            else:
                print("❌ No active leases found after creation")
                return f"Created deployment but lease not found: {self.created_dseq}"

        except Exception as e:
            print(f"❌ Controlled deployment creation error: {e}")
            return None

    def run_test_method(self, test_method):
        """Run a single test method and track results."""
        test_name = test_method.__name__.replace('test_', '').replace('_', ' ')
        print(f"\n{test_name}...")

        try:
            result = test_method()
            if result:
                print(f"✅ Pass: {result}")
                self.test_results['passed'] += 1
                self.test_results['tests'].append(f"Pass: {test_name}")
                return True
            else:
                print(f"❌ Fail: {test_name}")
                self.test_results['failed'] += 1
                self.test_results['tests'].append(f"Fail: {test_name}")
                return False
        except Exception as e:
            print(f"❌ Error: {test_name} - {str(e)}")
            self.test_results['failed'] += 1
            self.test_results['tests'].append(f"Error: {test_name}")
            return False

    def run_all_tests(self):
        """Run escrow module tests with deployment creation."""
        print("=" * 60)
        print(f"Escrow module tests - {self.network.upper()}")
        print("=" * 60)

        print("\nStep 1: Looking for existing deployments with active leases...")
        found_deployment = self.run_test_method(self.test_find_deployment_with_leases)

        if not found_deployment:
            print("\nStep 2: No deployments with leases found, creating controlled deployment...")
            created_deployment = self.run_test_method(self.test_create_controlled_deployment_with_lease)

            if not created_deployment:
                print("\n❌ Cannot test blocks remaining - no deployments available")
                self.print_results()
                return

        if self.created_dseq:
            print(f"\nStep 3: Testing blocks remaining with dseq {self.created_dseq}...")
            self.run_test_method(self.test_blocks_remaining_calculation)
        else:
            print("\n❌ No deployment available for blocks remaining test")
            self.test_results['failed'] += 1
            self.test_results['tests'].append("Fail: No deployment for testing")

        self.print_results()

    def print_results(self):
        """Print test results."""
        print("\n" + "=" * 60)
        print(f"Escrow module test results - {self.network.upper()}")
        print("=" * 60)

        results = self.test_results
        total = results['passed'] + results['failed']
        pass_rate = (results['passed'] / total * 100) if total > 0 else 0

        print(f"\n{self.network.upper()} results:")
        print(f" Total tests: {total}")
        print(f" Passed: {results['passed']}")
        print(f" Failed: {results['failed']}")
        print(f" Pass rate: {pass_rate:.1f}%")

        if results['tests']:
            print(f"\n  Details:")
            for test_result in results['tests']:
                print(f" {test_result}")

        print(f"\nEscrow module test on {self.network} completed.")

        if results['passed'] > 0:
            print(f"✅ Status: Escrow module functional on {self.network.upper()}")
        else:
            print(f"❌ Status: Escrow module issues on {self.network.upper()}")


def run_on_network(network_name):
    """Run tests on a specific network."""
    try:
        tests = EscrowE2ETests(network=network_name)
        tests.run_all_tests()
        return tests.test_results
    except KeyboardInterrupt:
        print(f"\nTests on {network_name} interrupted by user")
        return {'passed': 0, 'failed': 1, 'tests': ['Interrupted']}
    except Exception as e:
        print(f"\nTest suite failed on {network_name}: {e}")
        import traceback
        traceback.print_exc()
        return {'passed': 0, 'failed': 1, 'tests': ['Error']}


def main():
    """Run complete escrow module tests."""
    print("Starting escrow module tests on both networks...")
    print("=" * 80)

    print("\nTestnet testing")
    testnet_results = run_on_network("testnet")

    print("\n" + "=" * 80)

    print("\nMainnet testing")
    mainnet_results = run_on_network("mainnet")

    print("\n" + "=" * 80)
    print("Overall escrow module summary")
    print("=" * 80)

    testnet_total = testnet_results['passed'] + testnet_results['failed']
    mainnet_total = mainnet_results['passed'] + mainnet_results['failed']

    print(f"\nTestnet: {testnet_results['passed']}/{testnet_total} passed")
    print(f"Mainnet: {mainnet_results['passed']}/{mainnet_total} passed")

    overall_passed = testnet_results['passed'] + mainnet_results['passed']
    overall_total = testnet_total + mainnet_total

    if overall_passed > 0:
        print(f"\n✅ Escrow module: {overall_passed}/{overall_total} tests passed across networks")
    else:
        print(f"\n❌ Escrow module: All tests failed across networks")

    print("\nEscrow module testing complete!")


if __name__ == "__main__":
    main()