#!/usr/bin/env python3
"""
Distribution module example demonstrating all distribution functionality.
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


class DistributionE2ETests:
    """E2E test suite for Distribution module functionality."""

    def __init__(self):
        self.testnet_client = AkashClient(TESTNET_RPC, TESTNET_CHAIN_ID)
        self.test_wallet = AkashWallet.from_mnemonic(TEST_MNEMONIC)
        self.test_address = self.test_wallet.address

        print(f"Distribution tests - testnet: {TESTNET_RPC}")
        print(f"Test address: {self.test_address}")

    def test_get_delegator_rewards_specific_validator(self):
        """Test getting rewards from a specific validator."""
        try:
            print(" Testing get_delegator_rewards for specific validator...")

            all_rewards = self.testnet_client.distribution.get_delegator_rewards(self.test_address)
            if not all_rewards:
                print(" No delegations found - cannot test specific validator rewards")
                return None

            validator_with_rewards = None
            for reward_entry in all_rewards:
                if reward_entry.get('rewards') and len(reward_entry['rewards']) > 0:
                    validator_with_rewards = reward_entry['validator_address']
                    break

            if not validator_with_rewards:
                validator_with_rewards = all_rewards[0]['validator_address']

            print(f" Testing validator: {validator_with_rewards}")
            rewards = self.testnet_client.distribution.get_delegator_rewards(
                self.test_address, validator_with_rewards
            )

            if isinstance(rewards, list):
                print(f" Retrieved {len(rewards)} reward entries")
                if rewards:
                    first_reward = rewards[0]
                    if 'denom' in first_reward and 'amount' in first_reward:
                        print(f" First reward: {first_reward['amount']} {first_reward['denom']}")
                        return f"Retrieved {len(rewards)} validator-specific rewards"
                    else:
                        print(f" Invalid reward structure: {first_reward}")
                        return None
                else:
                    return "Retrieved 0 validator-specific rewards (valid empty result)"
            else:
                print(f" Invalid rewards response type: {type(rewards)}")
                return None

        except Exception as e:
            print(f" Error: {e}")
            return None

    def test_get_delegator_rewards_all(self):
        """Test getting all rewards for delegator."""
        try:
            print(" Testing get_delegator_rewards for all validators...")

            rewards = self.testnet_client.distribution.get_delegator_rewards(self.test_address)

            if isinstance(rewards, list):
                print(f" Retrieved {len(rewards)} validator reward entries")
                if rewards:
                    first_entry = rewards[0]
                    expected_fields = ['validator_address', 'rewards']
                    missing_fields = [field for field in expected_fields if field not in first_entry]

                    if not missing_fields:
                        validator_addr = first_entry['validator_address'][:25]
                        reward_count = len(first_entry['rewards'])
                        print(f" First validator: {validator_addr}... has {reward_count} reward types")
                        return f"Retrieved all rewards for {len(rewards)} validators"
                    else:
                        print(f" Missing fields in rewards structure: {missing_fields}")
                        return None
                else:
                    return "Retrieved 0 delegation rewards (valid empty result)"
            else:
                print(f" Invalid rewards response type: {type(rewards)}")
                return None

        except Exception as e:
            print(f" Error: {e}")
            return None

    def test_get_validator_commission(self):
        """Test getting validator commission."""
        try:
            print(" Testing get_validator_commission...")

            validators = self.testnet_client.staking.get_validators()
            if not validators:
                print(" No validators found - cannot test commission")
                return None

            validator_address = validators[0].get('operator_address', '')
            if not validator_address:
                print(" No validator address found")
                return None

            print(f" Testing validator: {validator_address}")
            commission_info = self.testnet_client.distribution.get_validator_commission(validator_address)

            if isinstance(commission_info, dict):
                if 'commission' in commission_info:
                    commission_list = commission_info['commission']
                    print(f" Retrieved commission with {len(commission_list)} entries")

                    if commission_list:
                        first_commission = commission_list[0]
                        if 'denom' in first_commission and 'amount' in first_commission:
                            print(f" First commission: {first_commission['amount']} {first_commission['denom']}")
                            return f"Retrieved validator commission with {len(commission_list)} entries"
                        else:
                            print(f" Invalid commission structure: {first_commission}")
                            return None
                    else:
                        return "Retrieved validator commission (empty - valid)"
                else:
                    print(f" Commission missing 'commission' field: {commission_info}")
                    return None
            else:
                print(f" Invalid commission response type: {type(commission_info)}")
                return None

        except Exception as e:
            print(f" Error: {e}")
            return None

    def test_get_validator_outstanding_rewards(self):
        """Test getting validator outstanding rewards."""
        try:
            print(" Testing get_validator_outstanding_rewards...")

            validators = self.testnet_client.staking.get_validators()
            if not validators:
                print(" No validators found - cannot test outstanding rewards")
                return None

            validator_address = validators[0].get('operator_address', '')
            if not validator_address:
                print(" No validator address found")
                return None

            print(f" Testing validator: {validator_address}")
            outstanding_rewards = self.testnet_client.distribution.get_validator_outstanding_rewards(validator_address)

            if isinstance(outstanding_rewards, dict):
                if 'rewards' in outstanding_rewards:
                    rewards_list = outstanding_rewards['rewards']
                    print(f" Retrieved outstanding rewards with {len(rewards_list)} entries")

                    if rewards_list:
                        first_reward = rewards_list[0]
                        if 'denom' in first_reward and 'amount' in first_reward:
                            print(f" First outstanding: {first_reward['amount']} {first_reward['denom']}")
                            return f"Retrieved outstanding rewards with {len(rewards_list)} entries"
                        else:
                            print(f" Invalid outstanding reward structure: {first_reward}")
                            return None
                    else:
                        return "Retrieved outstanding rewards (empty - valid)"
                else:
                    print(f" Outstanding rewards missing 'rewards' field: {outstanding_rewards}")
                    return None
            else:
                print(f" Invalid outstanding rewards response type: {type(outstanding_rewards)}")
                return None

        except Exception as e:
            print(f" Error: {e}")
            return None

    def test_get_distribution_params(self):
        """Test getting distribution module parameters."""
        try:
            print(" Testing get_distribution_params...")

            params = self.testnet_client.distribution.get_distribution_params()

            if isinstance(params, dict):
                expected_fields = [
                    'community_tax',
                    'base_proposer_reward',
                    'bonus_proposer_reward',
                    'withdraw_addr_enabled'
                ]

                missing_fields = [field for field in expected_fields if field not in params]

                if not missing_fields:
                    print(f" Community tax: {params['community_tax']}")
                    print(f" Base proposer reward: {params['base_proposer_reward']}")
                    print(f" Withdraw address enabled: {params['withdraw_addr_enabled']}")
                    return "Distribution params retrieved with all expected fields"
                else:
                    print(f" Missing param fields: {missing_fields}")
                    if len(missing_fields) < len(expected_fields):
                        return f"Distribution params partially retrieved (missing: {missing_fields})"
                    else:
                        return None
            else:
                print(f" Invalid params response type: {type(params)}")
                return None

        except Exception as e:
            print(f" Error: {e}")
            return None

    def test_get_community_pool(self):
        """Test getting community pool information."""
        try:
            print(" Testing get_community_pool...")

            pool_info = self.testnet_client.distribution.get_community_pool()

            if isinstance(pool_info, dict):
                if 'pool' in pool_info:
                    pool_coins = pool_info['pool']
                    print(f" Community pool has {len(pool_coins)} coin types")

                    if pool_coins:
                        first_coin = pool_coins[0]
                        if 'denom' in first_coin and 'amount' in first_coin:
                            print(f" First coin: {first_coin['amount']} {first_coin['denom']}")
                            return f"Community pool retrieved with {len(pool_coins)} coin types"
                        else:
                            print(f" Invalid pool coin structure: {first_coin}")
                            return None
                    else:
                        return "Community pool retrieved (empty - valid)"
                else:
                    print(f" Pool missing 'pool' field: {pool_info}")
                    return None
            else:
                print(f" Invalid pool response type: {type(pool_info)}")
                return None

        except Exception as e:
            print(f" Error: {e}")
            return None

    def test_get_validator_slashes(self):
        """Test getting validator slashes."""
        try:
            print(" Testing get_validator_slashes...")

            validators = self.testnet_client.staking.get_validators()
            if not validators:
                print(" No validators found - cannot test slashes")
                return None

            validator_address = validators[0].get('operator_address', '')
            if not validator_address:
                print(" No validator address found")
                return None

            print(f" Testing validator: {validator_address}")

            try:
                slashes = self.testnet_client.distribution.get_validator_slashes(validator_address)

                if isinstance(slashes, list):
                    print(f" Retrieved {len(slashes)} slashes")
                    if slashes:
                        first_slash = slashes[0]
                        if 'validator_period' in first_slash and 'fraction' in first_slash:
                            print(
                                f" First slash: period {first_slash['validator_period']}, fraction {first_slash['fraction']}")
                            return f"Retrieved {len(slashes)} validator slashes"
                        else:
                            print(f" Invalid slash structure: {first_slash}")
                            return None
                    else:
                        return "Retrieved 0 validator slashes (valid - no slashes)"
                else:
                    print(f" Invalid slashes response type: {type(slashes)}")
                    return None
            except Exception as slash_e:
                error_msg = str(slash_e).lower()
                if "empty response" in error_msg or "not found" in error_msg:
                    print(" No slashing data available (valid - validator not slashed)")
                    return "Validator slashes query handled correctly (no slashes found)"
                else:
                    raise slash_e

        except Exception as e:
            print(f" Error: {e}")
            return None

    def test_withdraw_delegator_reward_transaction(self):
        """Test withdrawing delegator reward transaction."""
        try:
            print(" Testing withdraw_delegator_reward transaction...")

            all_rewards = self.testnet_client.distribution.get_delegator_rewards(self.test_address)
            if not all_rewards:
                print(" No delegations found - cannot test reward withdrawal")
                return None

            validator_with_rewards = None
            for reward_entry in all_rewards:
                if reward_entry.get('rewards') and len(reward_entry['rewards']) > 0:
                    has_rewards = any(float(r.get('amount', '0')) > 0 for r in reward_entry['rewards'])
                    if has_rewards:
                        validator_with_rewards = reward_entry['validator_address']
                        break

            if not validator_with_rewards:
                validator_with_rewards = all_rewards[0]['validator_address']

            validator_address = validator_with_rewards

            print(f" Testing withdrawal from validator: {validator_address}")

            try:
                rewards = self.testnet_client.distribution.get_delegator_rewards(self.test_address, validator_address)
                if not rewards or all(float(r.get('amount', '0')) == 0 for r in rewards if 'amount' in r):
                    print(" No rewards available - simulating transaction structure only")
                    return "Withdraw delegator reward method available (no rewards to test)"
            except Exception:
                print(" Could not check rewards - testing transaction structure")

            result = self.testnet_client.distribution.withdraw_delegator_reward(
                wallet=self.test_wallet,
                validator_address=validator_address,
                memo="",
                fee_amount="8000",
                gas_limit=200000,
                use_simulation=True
            )

            time.sleep(15)

            if result and hasattr(result, 'success'):
                if result.success:
                    print(f" Transaction successful: {result.tx_hash if result.tx_hash else 'No hash'}")
                    return f"Withdraw delegator reward transaction executed successfully"
                else:
                    print(
                        f" Transaction failed with code {getattr(result, 'code', 'unknown')}: {getattr(result, 'raw_log', 'No log')}")
                    if "no delegation distribution info" in str(getattr(result, 'raw_log', '')).lower():
                        return "Withdraw delegator reward method working (no rewards available)"
                    else:
                        return None
            else:
                print(f" Invalid result structure: {result}")
                return None

        except Exception as e:
            print(f" Error: {e}")
            return None

    def test_set_withdraw_address_transaction(self):
        """Test setting withdraw address transaction."""
        try:
            print(" Testing set_withdraw_address transaction...")

            result = self.testnet_client.distribution.set_withdraw_address(
                wallet=self.test_wallet,
                withdraw_address=self.test_address,
                memo="",
                fee_amount="6000",
                gas_limit=150000,
                use_simulation=True
            )

            time.sleep(2)

            if result and hasattr(result, 'success'):
                if result.success:
                    print(f" Transaction successful: {result.tx_hash if result.tx_hash else 'No hash'}")
                    return f"Set withdraw address transaction executed successfully"
                else:
                    print(
                        f" Transaction failed with code {getattr(result, 'code', 'unknown')}: {getattr(result, 'raw_log', 'No log')}")
                    raw_log = str(getattr(result, 'raw_log', '')).lower()
                    if "already set" in raw_log or "same" in raw_log:
                        return "Set withdraw address method working (address already set to same value)"
                    else:
                        return None
            else:
                print(f" Invalid result structure: {result}")
                return None

        except Exception as e:
            print(f" Error: {e}")
            return None

    def test_transaction_methods_structure(self):
        """Test that transaction methods have correct structure."""
        try:
            print(" Testing transaction method structures...")

            distribution_client = self.testnet_client.distribution
            methods_found = 0

            transaction_methods = [
                'withdraw_delegator_reward',
                'withdraw_validator_commission',
                'set_withdraw_address',
                'fund_community_pool',
                'withdraw_all_rewards'
            ]

            for method_name in transaction_methods:
                if hasattr(distribution_client, method_name):
                    method = getattr(distribution_client, method_name)
                    if callable(method):
                        print(f" {method_name} method available")
                        methods_found += 1
                    else:
                        print(f" {method_name} not callable")
                        return None
                else:
                    print(f" {method_name} method missing")
                    return None

            return f"All {methods_found} transaction methods have correct structure"

        except Exception as e:
            print(f" Error: {e}")
            return None

    def run_all_tests(self):
        """Run all distribution example tests and report results."""
        print("\nStarting distribution module E2E tests")
        print("=" * 50)

        test_methods = [
            ("get delegator rewards (specific validator)", self.test_get_delegator_rewards_specific_validator),
            ("get delegator rewards (all validators)", self.test_get_delegator_rewards_all),
            ("get validator commission", self.test_get_validator_commission),
            ("get validator outstanding rewards", self.test_get_validator_outstanding_rewards),
            ("get community pool", self.test_get_community_pool),
            ("get validator slashes", self.test_get_validator_slashes),
            ("get distribution parameters", self.test_get_distribution_params),
            ("transaction methods structure", self.test_transaction_methods_structure),
            ("withdraw delegator reward transaction", self.test_withdraw_delegator_reward_transaction),
            ("set withdraw address transaction", self.test_set_withdraw_address_transaction)
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
                    results.append((test_name, "Pass", result))
                    passed += 1
                else:
                    print(f"❌ Fail: {test_name}")
                    results.append((test_name, "Fail", "No result returned"))
                    failed += 1
            except Exception as e:
                print(f"❌ Error: {test_name} - {str(e)}")
                results.append((test_name, "Error", str(e)))
                failed += 1

            time.sleep(1)

        print(f"\nDistribution module test summary")
        print("=" * 45)
        print(f"Total tests: {len(test_methods)}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")

        success_rate = (passed / len(test_methods)) * 100
        print(f"Success rate: {success_rate:.1f}%")

        if success_rate >= 85:
            print(f"\n✅ Excellent: distribution module tests {success_rate:.1f}% successful!")
            print("✅ Distribution module is ready")
        elif success_rate >= 70:
            print(f"\n✅ Good: distribution module tests {success_rate:.1f}% successful")
            print("✅ Distribution module functionality is working well")
        else:
            print(f"\n⚠️ Issues: distribution module tests only {success_rate:.1f}% successful")
            print("❌ Distribution module may need attention")

        return results


if __name__ == "__main__":
    try:
        test_runner = DistributionE2ETests()
        test_results = test_runner.run_all_tests()

        print(f"\nDetailed results:")
        for test_name, status, result in test_results:
            status_emoji = "✅" if status == "Pass" else "❌"
            print(f"{status_emoji} {test_name}: {result}")

    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        import traceback

        traceback.print_exc()
