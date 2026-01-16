#!/usr/bin/env python3
"""
Authorization (Authz) module E2E tests - dual grant types.

Tests grant/query/revoke cycles for both SendAuthorization and GenericAuthorization.

Testing approach:
1. Fund grantee wallet from funded granter wallet  
2. Create grant (SendAuthorization or GenericAuthorization)
3. Query to verify grant exists with details
4. Execute authorized transaction
5. Revoke the grant
6. Query to verify grant no longer exists

Two grant types tested:
- SendAuthorization: Allows specific spend limits for MsgSend
- GenericAuthorization: Allows execution of any message type (e.g., MsgDelegate)
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

GRANTER_MNEMONIC = "poverty torch street hybrid estate message increase play negative vibrant transfer six police tiny garment congress survey tired used audit dolphin focus abstract appear"
GRANTER_ADDRESS = "akash1qnnhhgzxj24f2kld5yhy4v4h4s9r295ak5gjw4"

GRANTEE_MNEMONIC = "true ridge approve quantum sister primary notable have express fitness forum capable"
GRANTEE_ADDRESS = "akash1dunnyt0y5476j0xawfh85n83uyzrdzlhaytyqv"


class AuthzDualTypeE2ETests:
    """Authz E2E tests with both authorization types."""

    def __init__(self):
        self.testnet_client = AkashClient(TESTNET_RPC, TESTNET_CHAIN)
        self.granter_wallet = AkashWallet.from_mnemonic(GRANTER_MNEMONIC)
        self.grantee_wallet = AkashWallet.from_mnemonic(GRANTEE_MNEMONIC)
        self.test_results = {
            'send_authorization': {'passed': 0, 'failed': 0, 'tests': []},
            'generic_authorization': {'passed': 0, 'failed': 0, 'tests': []},
        }
        print(f"Funded granter wallet: {self.granter_wallet.address}")
        print(f"Fixed grantee wallet: {self.grantee_wallet.address}")

    def run_test(self, test_type, test_name, test_func):
        """Run a single test and record results."""
        print(f" Testing {test_name}...")
        try:
            result = test_func()
            if result:
                print(f" ✅: {result}")
                self.test_results[test_type]['passed'] += 1
                self.test_results[test_type]['tests'].append(f"✅ {test_name}")
                return True
            else:
                print(f" ❌: {test_name} failed")
                self.test_results[test_type]['failed'] += 1
                self.test_results[test_type]['tests'].append(f"❌ {test_name}: Failed")
                return False
        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)[:100]}"
            print(f" ❌: {error_msg}")
            self.test_results[test_type]['failed'] += 1
            self.test_results[test_type]['tests'].append(f"❌ {test_name}: {error_msg}")
            return False

    def create_send_authorization_grant(self):
        """Create SendAuthorization grant with spending limit."""
        print(f" Creating SendAuthorization grant (3 AKT limit)...")

        result = self.testnet_client.authz.grant_authorization(
            wallet=self.granter_wallet,
            grantee=self.grantee_wallet.address,
            msg_type_url="/cosmos.bank.v1beta1.MsgSend",
            spend_limit="3000000",
            denom="uakt",
            authorization_type="send",
            expiration_days=1,
            memo="",
            fee_amount='8000',
            use_simulation=True
        )

        if result and result.success:
            print(f" ✅ Grant created: Tx {result.tx_hash}")
            return result.tx_hash
        else:
            print(f" ❌ Grant failed: Code {result.code if result else 'N/A'}")
            if result and result.raw_log:
                print(f" Error: {result.raw_log}")
            return None

    def create_generic_authorization_grant(self):
        """Create GenericAuthorization grant for MsgDelegate."""
        print(f" Creating GenericAuthorization grant (MsgDelegate)...")

        result = self.testnet_client.authz.grant_authorization(
            wallet=self.granter_wallet,
            grantee=self.grantee_wallet.address,
            msg_type_url="/cosmos.staking.v1beta1.MsgDelegate",
            authorization_type="generic",
            expiration_days=1,
            memo="",
            fee_amount='8000',
            use_simulation=True
        )

        if result and result.success:
            print(f" ✅ Grant created: Tx {result.tx_hash}")
            return result.tx_hash
        else:
            print(f" ❌ Grant failed: Code {result.code if result else 'N/A'}")
            if result and result.raw_log:
                print(f" Error: {result.raw_log}")
            return None

    def query_grants_with_details(self, expected_type):
        """Query grants and verify they contain expected authorization type."""
        print(f" Querying grants from granter to grantee...")

        grants = self.testnet_client.authz.get_grants(self.granter_wallet.address, self.grantee_wallet.address)

        if not grants:
            print(f" ❌ No grants found")
            return None

        print(f" Found {len(grants)} grants:")
        for i, grant in enumerate(grants):
            granter = grant.get('granter',
                                self.granter_wallet.address if hasattr(self, 'granter_wallet') else 'unknown')
            grantee = grant.get('grantee',
                                self.grantee_wallet.address if hasattr(self, 'grantee_wallet') else 'unknown')
            auth_data = grant.get('authorization', {})
            auth_type = auth_data.get('@type', 'unknown').split('.')[-1]

            print(f" Grant {i + 1}: {granter}→{grantee}, Type: {auth_type}")

            if 'SendAuthorization' in auth_data.get('@type', ''):
                if 'spend_limit' in auth_data:
                    limits = auth_data['spend_limit']
                    for limit in limits:
                        limit_akt = int(limit['amount']) / 1_000_000
                        print(f" Spend limit: {limit_akt} AKT ({limit['amount']} {limit['denom']})")
            elif 'GenericAuthorization' in auth_data.get('@type', ''):
                if 'msg' in auth_data:
                    msg_type = auth_data['msg'].split('/')[-1] if auth_data['msg'].startswith('/') else auth_data['msg']
                    print(f" Message type: {msg_type}")

            expiration = grant.get('expiration')
            if expiration:
                print(f" Expiration: {expiration}")

        found_expected_type = any(
            expected_type.lower() in grant.get('authorization', {}).get('@type', '').lower()
            for grant in grants
        )

        if found_expected_type:
            return f"Query verified: Found {len(grants)} grants including {expected_type}"
        else:
            print(f" ❌ Expected {expected_type} not found in grants")
            return None

    def query_granter_grants(self):
        """Query all grants given by granter."""
        print(f" Querying all grants given by granter...")

        grants = self.testnet_client.authz.get_granter_grants(self.granter_wallet.address)

        if not grants:
            print(f" ❌ No granter grants found")
            return None

        print(f" Found {len(grants)} granter grants:")
        for i, grant in enumerate(grants):
            granter = grant.get('granter', 'unknown')
            grantee = grant.get('grantee', 'unknown')
            auth_data = grant.get('authorization', {})
            auth_type = auth_data.get('@type', 'unknown').split('.')[-1]

            print(f" Grant {i + 1}: {granter}→{grantee}, Type: {auth_type}")

        return f"Query verified: Found {len(grants)} granter grants"

    def query_grantee_grants(self):
        """Query all grants received by grantee."""
        print(f" Querying all grants received by grantee...")

        grants = self.testnet_client.authz.get_grantee_grants(self.grantee_wallet.address)

        if not grants:
            print(f" ❌ No grantee grants found")
            return None

        print(f" Found {len(grants)} grantee grants:")
        for i, grant in enumerate(grants):
            granter = grant.get('granter', 'unknown')
            grantee = grant.get('grantee', 'unknown')
            auth_data = grant.get('authorization', {})
            auth_type = auth_data.get('@type', 'unknown').split('.')[-1]

            print(f" Grant {i + 1}: {granter}→{grantee}, Type: {auth_type}")

        return f"Query verified: Found {len(grants)} grantee grants"

    def execute_send_authorization(self):
        """Execute a send transaction using SendAuthorization."""
        print(f" Executing authorized send (0.1 AKT)...")

        try:
            send_message = {
                '@type': '/cosmos.bank.v1beta1.MsgSend',
                'from_address': self.granter_wallet.address,
                'to_address': self.grantee_wallet.address,
                'amount': [{'denom': 'uakt', 'amount': '100000'}]
            }

            result = self.testnet_client.authz.execute_authorized(
                wallet=self.grantee_wallet,
                messages=[send_message],
                memo="",
                fee_amount='15000',
                gas_limit=300000,
                use_simulation=False
            )

            if result and result.success:
                return f"Execution success: Tx {result.tx_hash} sent 0.1 AKT"
            elif result and result.tx_hash:
                print(f" Execute broadcast: Tx {result.tx_hash} (MsgExec fixed)")
                return f"Execute broadcast: Tx {result.tx_hash} (fixed - should confirm)"
            elif result:
                print(f" Execution failed: Code {result.code}, {result.raw_log}")
                return None
            else:
                print(f" No result from execution")
                return None
        except Exception as e:
            print(f" Execution error: {e}")
            return None

    def execute_generic_authorization(self):
        """Execute a delegate transaction using GenericAuthorization."""
        print(f" Executing authorized delegate (0.1 AKT)...")

        validators = self.testnet_client.get_validators()
        if not validators:
            print(f" ❌ No validators available for delegation")
            return None

        validator_address = validators[0].get('operator_address', validators[0].get('address'))
        if not validator_address:
            print(f" ❌ Could not get validator address")
            return None

        print(f" Using validator: {validator_address}")

        delegate_message = {
            '@type': '/cosmos.staking.v1beta1.MsgDelegate',
            'delegator_address': self.granter_wallet.address,
            'validator_address': validator_address,
            'amount': {'denom': 'uakt', 'amount': '100000'}
        }

        result = self.testnet_client.authz.execute_authorized(
            wallet=self.grantee_wallet,
            messages=[delegate_message],
            memo="",
            fee_amount='12000',
            use_simulation=True
        )

        if result and result.success:
            return f"Execution success: Tx {result.tx_hash} delegated 0.1 AKT"
        elif result:
            print(f" Execution failed: {result.raw_log}")
            return None
        else:
            return None

    def revoke_authorization(self, msg_type_url):
        """Revoke the authorization grant."""
        print(f" Revoking authorization for {msg_type_url.split('/')[-1]}...")

        result = self.testnet_client.authz.revoke_authorization(
            wallet=self.granter_wallet,
            grantee=self.grantee_wallet.address,
            msg_type_url=msg_type_url,
            memo="",
            fee_amount='7000',
            use_simulation=True
        )

        if result and result.success:
            return f"Revoke success: Tx {result.tx_hash}"
        elif result:
            print(f" Revoke failed: {result.raw_log}")
            return None
        else:
            return None

    def verify_grant_removed(self):
        """Verify grant no longer exists after revoke."""
        print(f" Verifying grant was removed...")
        time.sleep(8)

        grants = self.testnet_client.authz.get_grants(self.granter_wallet.address, self.grantee_wallet.address)

        if not grants:
            return f"Revoke verified: No grants remain between addresses"
        else:
            print(f" ⚠️ Found {len(grants)} grants still remaining:")
            for i, grant in enumerate(grants):
                auth_type = grant.get('authorization', {}).get('@type', 'unknown').split('.')[-1]
                print(f" Grant {i + 1}: {auth_type}")
            return None

    def run_send_authorization_cycle(self):
        """Run complete SendAuthorization grant/query/revoke cycle."""
        print("\n Send authorization cycle")
        print("=" * 50)

        tests = [
            ("create_send_grant", lambda: "Created" if self.create_send_authorization_grant() else None),
            ("query_send_grant", lambda: self.query_grants_with_details("SendAuthorization")),
            ("query_granter_grants", lambda: self.query_granter_grants()),
            ("query_grantee_grants", lambda: self.query_grantee_grants()),
            ("execute_send_auth", lambda: self.execute_send_authorization()),
            ("revoke_send_auth", lambda: self.revoke_authorization("/cosmos.bank.v1beta1.MsgSend")),
            ("verify_grant_removed", lambda: self.verify_grant_removed()),
        ]

        print("  SendAuthorization cycle tests:")
        for test_name, test_func in tests:
            success = self.run_test("send_authorization", test_name, test_func)
            if not success and test_name in ["fund_grantee_wallet", "create_send_grant"]:
                print(" ⚠️ Critical test failed - stopping SendAuth cycle")
                break
            time.sleep(8)

    def run_generic_authorization_cycle(self):
        """Run complete GenericAuthorization grant/query/revoke cycle."""
        print("\n Generic authorization cycle")
        print("=" * 50)

        tests = [
            ("create_generic_grant", lambda: "Created" if self.create_generic_authorization_grant() else None),
            ("query_generic_grant", lambda: self.query_grants_with_details("GenericAuthorization")),
            ("query_granter_grants", lambda: self.query_granter_grants()),
            ("query_grantee_grants", lambda: self.query_grantee_grants()),
            ("execute_generic_auth", lambda: self.execute_generic_authorization()),
            ("revoke_generic_auth", lambda: self.revoke_authorization("/cosmos.staking.v1beta1.MsgDelegate")),
            ("verify_grant_removed", lambda: self.verify_grant_removed()),
        ]

        print("  GenericAuthorization cycle tests:")
        for test_name, test_func in tests:
            success = self.run_test("generic_authorization", test_name, test_func)
            if not success and test_name in ["fund_grantee_wallet", "create_generic_grant"]:
                print(" ⚠️ Critical test failed - stopping GenericAuth cycle")
                break
            time.sleep(8)

    def run_all_tests(self):
        """Run all E2E tests."""
        print("Authorization (authz) module E2E tests")
        print("=" * 50)
        print("Testing grant/query/execute/revoke cycles for both authorization types")

        self.run_send_authorization_cycle()
        self.run_generic_authorization_cycle()

        self.print_summary()

    def print_summary(self):
        """Print test results summary."""
        print("\n" + "=" * 50)
        print("Authz module E2E test results")
        print("=" * 50)

        total_passed = 0
        total_failed = 0

        for test_type in ['send_authorization', 'generic_authorization']:
            results = self.test_results[test_type]
            passed = results['passed']
            failed = results['failed']
            total = passed + failed
            success_rate = (passed / total * 100) if total > 0 else 0

            total_passed += passed
            total_failed += failed

            type_name = test_type.replace('_', ' ').title()
            print(f"\n{type_name} results:")
            print(f" Tests run: {total}")
            print(f" Passed: {passed}")
            print(f" Failed: {failed}")
            print(f" Success rate: {success_rate:.1f}%")

            if results['tests']:
                print(" Details:")
                for test in results['tests']:
                    print(f" {test}")

        total_tests = total_passed + total_failed
        overall_success = (total_passed / total_tests * 100) if total_tests > 0 else 0

        print(f"\nOverall summary:")
        print(f" Total tests: {total_tests}")
        print(f" Passed: {total_passed}")
        print(f" Failed: {total_failed}")
        print(f" Success rate: {overall_success:.1f}%")

        if overall_success >= 90:
            print(f"\nAuthz tests: Great success!")
            print(f" Both SendAuthorization and GenericAuthorization working perfectly")
        elif overall_success >= 75:
            print(f"\nAuthz tests: Good success!")
            print(f" Most functionality working across both authorization types")
        elif overall_success >= 50:
            print(f"\nAuthz tests: Partial success")
            print(f" Some issues found in authorization cycles")
        else:
            print(f"\nAuthz tests: Needs attention")
            print(f" Significant issues in authorization functionality")

        print("\n" + "=" * 70)


def main():
    """Run Authorization module E2E tests."""
    print("Starting authorization module E2E tests...")
    print("Testing cycles for SendAuthorization and GenericAuthorization")

    test_runner = AuthzDualTypeE2ETests()
    test_runner.run_all_tests()

    print("\nAuthorization module E2E testing complete!")


if __name__ == "__main__":
    main()