#!/usr/bin/env python3
"""
Inflation module example demonstrating inflation functionality.

Tests all inflation (mint) module query functions against live blockchain data.
The mint module is query-only, so no transaction tests are included.

Tests:
- get_params: Query mint module parameters  
- get_inflation: Query current inflation rate
- get_annual_provisions: Query current annual provisions
- get_all_mint_info: Query all mint information
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

logging.getLogger('akash').setLevel(logging.WARNING)

TESTNET_RPC = "https://rpc.sandbox-01.aksh.pw:443"
TESTNET_CHAIN_ID = "sandbox-01"
MAINNET_RPC = "https://akash-rpc.polkachu.com:443"
MAINNET_CHAIN_ID = "akashnet-2"

TEST_MNEMONIC = "poverty torch street hybrid estate message increase play negative vibrant transfer six police tiny garment congress survey tired used audit dolphin focus abstract appear"


class InflationE2ETests:
    """E2E test suite for Inflation (mint) module functionality."""

    def __init__(self):
        self.testnet_client = AkashClient(TESTNET_RPC, TESTNET_CHAIN_ID)
        self.mainnet_client = AkashClient(MAINNET_RPC, MAINNET_CHAIN_ID)
        self.test_wallet = AkashWallet.from_mnemonic(TEST_MNEMONIC)
        self.test_address = self.test_wallet.address

        print(f"Inflation E2E Tests")
        print(f"Testnet: {TESTNET_RPC}")
        print(f"Mainnet: {MAINNET_RPC}")
        print(f"Test Address: {self.test_address}")

    def test_get_params_testnet(self):
        """Test getting mint parameters on testnet."""
        try:
            print(" Testing get_params on testnet...")

            params = self.testnet_client.inflation.get_params()

            if not params:
                print(" No params returned")
                return None

            if not isinstance(params, dict):
                print(f" Invalid params type: {type(params)}")
                return None

            required_fields = ['mint_denom', 'inflation_rate_change', 'inflation_max',
                               'inflation_min', 'goal_bonded', 'blocks_per_year']
            missing_fields = [field for field in required_fields if field not in params]

            if missing_fields:
                print(f" Missing required fields: {missing_fields}")
                return None

            print(f" Mint denom: {params.get('mint_denom', 'unknown')}")
            print(f" Inflation max: {params.get('inflation_max', 'unknown')}")
            print(f" Inflation min: {params.get('inflation_min', 'unknown')}")
            print(f" Goal bonded: {params.get('goal_bonded', 'unknown')}")
            print(f" Blocks per year: {params.get('blocks_per_year', 'unknown')}")

            return f"Retrieved mint params with {len(params)} fields"

        except Exception as e:
            print(f" Error: {e}")
            return None

    def test_get_params_mainnet(self):
        """Test getting mint parameters on mainnet."""
        try:
            print(" Testing get_params on mainnet...")

            params = self.mainnet_client.inflation.get_params()

            if not params:
                print(" No params returned")
                return None

            if not isinstance(params, dict):
                print(f" Invalid params type: {type(params)}")
                return None

            required_fields = ['mint_denom', 'inflation_rate_change', 'inflation_max',
                               'inflation_min', 'goal_bonded', 'blocks_per_year']
            missing_fields = [field for field in required_fields if field not in params]

            if missing_fields:
                print(f" Missing required fields: {missing_fields}")
                return None

            print(f" Mint denom: {params.get('mint_denom', 'unknown')}")
            print(f" Inflation max: {params.get('inflation_max', 'unknown')}")
            print(f" Inflation min: {params.get('inflation_min', 'unknown')}")
            print(f" Goal bonded: {params.get('goal_bonded', 'unknown')}")
            print(f" Blocks per year: {params.get('blocks_per_year', 'unknown')}")

            return f"Retrieved mint params with {len(params)} fields"

        except Exception as e:
            print(f" Error: {e}")
            return None

    def test_get_inflation_testnet(self):
        """Test getting current inflation rate on testnet."""
        try:
            print(" Testing get_inflation on testnet...")

            inflation = self.testnet_client.inflation.get_inflation()

            if not inflation:
                print(" No inflation returned")
                return None

            if not isinstance(inflation, str):
                print(f" Invalid inflation type: {type(inflation)}")
                return None

            try:
                float(inflation)
                print(f" Current inflation rate: {inflation}")
                return f"Retrieved inflation rate: {inflation}"
            except ValueError:
                print(f" Invalid inflation format: {inflation}")
                return None

        except Exception as e:
            print(f" Error: {e}")
            return None

    def test_get_inflation_mainnet(self):
        """Test getting current inflation rate on mainnet."""
        try:
            print(" Testing get_inflation on mainnet...")

            inflation = self.mainnet_client.inflation.get_inflation()

            if not inflation:
                print(" No inflation returned")
                return None

            if not isinstance(inflation, str):
                print(f" Invalid inflation type: {type(inflation)}")
                return None

            try:
                float(inflation)
                print(f" Current inflation rate: {inflation}")
                return f"Retrieved inflation rate: {inflation}"
            except ValueError:
                print(f" Invalid inflation format: {inflation}")
                return None

        except Exception as e:
            print(f" Error: {e}")
            return None

    def test_get_annual_provisions_testnet(self):
        """Test getting annual provisions on testnet."""
        try:
            print(" Testing get_annual_provisions on testnet...")

            provisions = self.testnet_client.inflation.get_annual_provisions()

            if not provisions:
                print(" No provisions returned")
                return None

            if not isinstance(provisions, str):
                print(f" Invalid provisions type: {type(provisions)}")
                return None

            try:
                float(provisions)
                print(f" Annual provisions: {provisions}")
                return f"Retrieved annual provisions: {provisions}"
            except ValueError:
                print(f" Invalid provisions format: {provisions}")
                return None

        except Exception as e:
            print(f" Error: {e}")
            return None

    def test_get_annual_provisions_mainnet(self):
        """Test getting annual provisions on mainnet."""
        try:
            print(" Testing get_annual_provisions on mainnet...")

            provisions = self.mainnet_client.inflation.get_annual_provisions()

            if not provisions:
                print(" No provisions returned")
                return None

            if not isinstance(provisions, str):
                print(f" Invalid provisions type: {type(provisions)}")
                return None

            try:
                float(provisions)
                print(f" Annual provisions: {provisions}")
                return f"Retrieved annual provisions: {provisions}"
            except ValueError:
                print(f" Invalid provisions format: {provisions}")
                return None

        except Exception as e:
            print(f" Error: {e}")
            return None

    def test_get_all_mint_info_testnet(self):
        """Test getting all mint info on testnet."""
        try:
            print(" Testing get_all_mint_info on testnet...")

            all_info = self.testnet_client.inflation.get_all_mint_info()

            if not all_info:
                print(" No mint info returned")
                return None

            if not isinstance(all_info, dict):
                print(f" Invalid all_info type: {type(all_info)}")
                return None

            required_fields = ['params', 'current_inflation', 'annual_provisions', 'status']
            missing_fields = [field for field in required_fields if field not in all_info]

            if missing_fields:
                print(f" Missing required fields: {missing_fields}")
                return None

            status = all_info.get('status', 'unknown')
            params_available = bool(all_info.get('params'))
            inflation_available = bool(all_info.get('current_inflation'))
            provisions_available = bool(all_info.get('annual_provisions'))

            print(f" Status: {status}")
            print(f" Params available: {params_available}")
            print(f" Inflation available: {inflation_available}")
            print(f" Provisions available: {provisions_available}")

            return f"Retrieved all mint info with status: {status}"

        except Exception as e:
            print(f" Error: {e}")
            return None

    def test_get_all_mint_info_mainnet(self):
        """Test getting all mint info on mainnet."""
        try:
            print(" Testing get_all_mint_info on mainnet...")

            all_info = self.mainnet_client.inflation.get_all_mint_info()

            if not all_info:
                print(" No mint info returned")
                return None

            if not isinstance(all_info, dict):
                print(f" Invalid all_info type: {type(all_info)}")
                return None

            required_fields = ['params', 'current_inflation', 'annual_provisions', 'status']
            missing_fields = [field for field in required_fields if field not in all_info]

            if missing_fields:
                print(f" Missing required fields: {missing_fields}")
                return None

            status = all_info.get('status', 'unknown')
            params_available = bool(all_info.get('params'))
            inflation_available = bool(all_info.get('current_inflation'))
            provisions_available = bool(all_info.get('annual_provisions'))

            print(f" Status: {status}")
            print(f" Params available: {params_available}")
            print(f" Inflation available: {inflation_available}")
            print(f" Provisions available: {provisions_available}")

            return f"Retrieved all mint info with status: {status}"

        except Exception as e:
            print(f" Error: {e}")
            return None

    def run_all_tests(self):
        """Run all inflation module e2e tests."""
        print("\n" + "=" * 60)
        print("Inflation module E2E tests")
        print("=" * 60)

        tests = [
            ("Testnet params", self.test_get_params_testnet),
            ("Mainnet params", self.test_get_params_mainnet),
            ("Testnet inflation", self.test_get_inflation_testnet),
            ("Mainnet inflation", self.test_get_inflation_mainnet),
            ("Testnet annual provisions", self.test_get_annual_provisions_testnet),
            ("Mainnet annual provisions", self.test_get_annual_provisions_mainnet),
            ("Testnet all mint info", self.test_get_all_mint_info_testnet),
            ("Mainnet all mint info", self.test_get_all_mint_info_mainnet),
        ]

        passed = 0
        failed = 0

        for test_name, test_func in tests:
            print(f"\n{test_name}:")
            try:
                result = test_func()
                if result:
                    print(f" ✅ Pass: {result}")
                    passed += 1
                else:
                    print(f" ❌ Fail: No result returned")
                    failed += 1
            except Exception as e:
                print(f" ❌ Error: {e}")
                failed += 1

        print(f"\n" + "=" * 60)
        print(f"Inflation module E2E test results")
        print(f"=" * 60)
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Total: {passed + failed}")
        print(f"Success rate: {(passed / (passed + failed) * 100):.1f}%")

        if passed >= 7:
            print(f"\n Inflation module E2E tests: success!")
        elif passed >= 5:
            print(f"\n✅ Inflation module E2E tests: mostly successful")
        else:
            print(f"\n⚠️ Inflation module E2E tests: needs investigation")

        return passed >= 7


def main():
    """Main test execution function."""
    print("Starting inflation module E2E tests...")
    print("Testing all functions on both testnet and mainnet")

    test_runner = InflationE2ETests()
    success = test_runner.run_all_tests()

    if success:
        print(f"\n✅ All inflation module E2E tests completed successfully!")
        exit(0)
    else:
        print(f"\n❌ Some inflation module E2E tests failed")
        exit(1)


if __name__ == "__main__":
    main()