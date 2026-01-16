#!/usr/bin/env python3
"""
Master Test Runner for Akash Python SDK Validation Tests

Runs all module validation tests and provides reporting.
These tests validate protobuf structures, message converters, and query patterns
without requiring blockchain interactions.

Usage:
    python run_all_tests.py              # Run all tests
    python run_all_tests.py --verbose    # Run with verbose output
    python run_all_tests.py market       # Run specific module
    python run_all_tests.py --summary    # Show summary only
"""

import argparse
import os
import subprocess
import sys
import time
from typing import Dict, List, Tuple

os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

TEST_MODULES = {
    # Import validation tests (CRITICAL)
    'imports': {'file': 'test_all_imports.py', 'converters': 0},
    'protobuf-imports': {'file': 'test_protobuf_imports.py', 'converters': 17},

    'client': {'file': 'client_tests.py', 'converters': 0},
    'wallet': {'file': 'wallet_tests.py', 'converters': 0},
    'tx': {'file': 'tx_tests.py', 'converters': 0},

    'market': {'file': 'market_tests.py', 'converters': 5},
    'deployment': {'file': 'deployment_tests.py', 'converters': 7},
    'escrow': {'file': 'escrow_tests.py', 'converters': 0},
    'provider': {'file': 'provider_tests.py', 'converters': 2},
    'cert': {'file': 'cert_tests.py', 'converters': 2},
    'audit': {'file': 'audit_tests.py', 'converters': 2},
    'inventory': {'file': 'inventory_tests.py', 'converters': 0},
    'cert-mtls': {'file': 'cert_mtls_tests.py', 'converters': 0},
    'grpc-client': {'file': 'grpc_client_tests.py', 'converters': 0},
    'manifest': {'file': 'manifest_tests.py', 'converters': 0},
    'discovery-grpc': {'file': 'discovery_grpc_tests.py', 'converters': 0},
    'grpc-standalone': {'file': 'grpc_standalone_tests.py', 'converters': 0},

    'auth': {'file': 'auth_tests.py', 'converters': 0},
    'bank': {'file': 'bank_tests.py', 'converters': 1},
    'staking': {'file': 'staking_tests.py', 'converters': 5},
    'distribution': {'file': 'distribution_tests.py', 'converters': 2},
    'slashing': {'file': 'slashing_tests.py', 'converters': 1},
    'authz': {'file': 'authz_tests.py', 'converters': 3},
    'feegrant': {'file': 'feegrant_tests.py', 'converters': 4},
    'gov': {'file': 'gov_tests.py', 'converters': 3},
    'evidence': {'file': 'evidence_tests.py', 'converters': 1},
    'inflation': {'file': 'inflation_tests.py', 'converters': 0},
    'ibc': {'file': 'ibc_tests.py', 'converters': 2},
}


class TestRunner:
    """Master test runner for all validation tests."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.results: Dict[str, Dict] = {}
        self.start_time = 0
        self.end_time = 0

    def run_module_test(self, module_name: str, module_config: Dict) -> Dict:
        """Run tests for a single module."""
        print(f"Testing {module_name.upper()} module...", end=" ")
        sys.stdout.flush()

        test_file = module_config['file']

        start = time.time()

        try:
            cmd = [
                sys.executable,
                '-m', 'pytest',
                test_file,
                '--tb=short',
                '-q'  # Quiet mode by default
            ]

            if self.verbose:
                cmd.extend(['-v', '--tb=long'])

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=os.path.dirname(os.path.abspath(__file__))
            )

            elapsed = time.time() - start

            output = result.stdout + result.stderr

            passed = 0
            failed = 0
            total_tests = 0

            import re
            if 'passed' in output:
                passed_match = re.search(r'(\d+) passed', output)
                if passed_match:
                    passed = int(passed_match.group(1))

            if 'failed' in output:
                failed_match = re.search(r'(\d+) failed', output)
                if failed_match:
                    failed = int(failed_match.group(1))

            total_tests = passed + failed

            success = result.returncode == 0

            if success:
                print(f"✅ {passed} tests passed ({elapsed:.2f}s)")
            else:
                print(f"❌ {passed} passed, {failed} failed ({elapsed:.2f}s)")

            return {
                'success': success,
                'passed': passed,
                'failed': failed,
                'total_tests': total_tests,
                'elapsed': elapsed,
                'output': output if self.verbose or not success else None,
                'converters': module_config['converters']
            }

        except Exception as e:
            elapsed = time.time() - start
            print(f"❌ ERROR: {str(e)}")
            return {
                'success': False,
                'passed': 0,
                'failed': 0,
                'total_tests': 0,
                'elapsed': elapsed,
                'output': str(e),
                'converters': module_config['converters']
            }

    def run_all_tests(self, modules_to_run: List[str] = None) -> bool:
        """Run all validation tests.

        Returns:
            bool: True if all tests passed, False otherwise
        """
        self.start_time = time.time()

        # Determine which modules to run
        if modules_to_run:
            modules = {k: v for k, v in TEST_MODULES.items() if k in modules_to_run}
            if not modules:
                print(f"❌ No valid modules found: {modules_to_run}")
                print(f"Available modules: {', '.join(TEST_MODULES.keys())}")
                return False
        else:
            modules = TEST_MODULES

        print("=" * 80)
        print("Akash python sdk - Validation test suite")
        print("=" * 80)
        print(f"Running {len(modules)} module test suites...")
        print()

        # Run tests for each module
        for module_name, module_config in modules.items():
            self.results[module_name] = self.run_module_test(module_name, module_config)

            # Show verbose output if requested
            if self.verbose and self.results[module_name]['output']:
                print("\nDetailed output:")
                print(self.results[module_name]['output'])
                print("-" * 40)

        self.end_time = time.time()

        # Display summary
        self.display_summary()

        # Return overall success
        total_modules = len(self.results)
        successful_modules = sum(1 for r in self.results.values() if r['success'])
        total_failed = sum(r['failed'] for r in self.results.values())

        return successful_modules == total_modules and total_failed == 0

    def display_summary(self) -> None:
        """Display test summary."""
        print("\n" + "=" * 80)
        print("Test summary")
        print("=" * 80)

        # Categorize results
        infrastructure_modules = []
        akash_modules = []
        cosmos_modules = []

        for module_name, result in self.results.items():
            if module_name in ['imports', 'protobuf-imports', 'client', 'wallet', 'tx']:
                infrastructure_modules.append((module_name, result))
            elif module_name in ['market', 'deployment', 'escrow', 'provider', 'cert', 'audit', 'inventory',
                                 'cert-mtls', 'grpc-client', 'manifest', 'discovery-grpc', 'grpc-standalone']:
                akash_modules.append((module_name, result))
            else:
                cosmos_modules.append((module_name, result))

        if infrastructure_modules:
            print("\nINFRASTRUCTURE Modules:")
            print("-" * 40)
            self._display_module_group(infrastructure_modules)

        if akash_modules:
            print("\nAKASH Modules:")
            print("-" * 40)
            self._display_module_group(akash_modules)

        if cosmos_modules:
            print("\nCOSMOS Modules:")
            print("-" * 40)
            self._display_module_group(cosmos_modules)

        print("\n" + "=" * 80)
        print("Overall statistics")
        print("-" * 40)

        total_modules = len(self.results)
        successful_modules = sum(1 for r in self.results.values() if r['success'])
        total_tests = sum(r['total_tests'] for r in self.results.values())
        total_passed = sum(r['passed'] for r in self.results.values())
        total_failed = sum(r['failed'] for r in self.results.values())
        total_converters = sum(r['converters'] for r in self.results.values())
        total_elapsed = self.end_time - self.start_time

        print(f"Modules tested:      {successful_modules}/{total_modules}")
        print(f"Tests passed:        {total_passed}/{total_tests}")
        print(f"Tests failed:        {total_failed}")
        print(f"Success rate:        {(total_passed / total_tests) * 100:.1f}%")
        print(f"Message converters:  {total_converters}")
        print(f"Total time:          {total_elapsed:.2f}s")

        print("\n" + "=" * 80)
        if successful_modules == total_modules and total_failed == 0:
            print("✅ all Tests passed! SDK validation complete.")
        else:
            print(f"⚠️  {total_failed} tests failed across {total_modules - successful_modules} modules.")

            # Show failed modules
            failed_modules = [m for m, r in self.results.items() if not r['success']]
            if failed_modules:
                print(f"Failed modules: {', '.join(failed_modules)}")
        print("=" * 80)

    def _display_module_group(self, modules: List[Tuple[str, Dict]]) -> None:
        """Display a group of module results."""
        # Sort by module name
        modules.sort(key=lambda x: x[0])

        max_name_len = max(len(name) for name, _ in modules)

        print(f"{'Module':<{max_name_len + 2}} {'Tests':>8} {'Status':>10} {'Time':>8} {'Converters':>10}")
        print("-" * (max_name_len + 40))

        # Module results
        for module_name, result in modules:
            status = "✅ PASS" if result['success'] else f"❌ FAIL"
            tests = f"{result['passed']}" if result[
                'success'] else f"{result['passed']}/{result['passed'] + result['failed']}"
            time_str = f"{result['elapsed']:.2f}s"
            converters = str(result['converters'])

            print(
                f"{module_name.capitalize():<{max_name_len + 2}} {tests:>8} {status:>10} {time_str:>8} {converters:>10}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Run Akash Python SDK validation tests',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_all_tests.py                    # Run all tests
  python run_all_tests.py --verbose          # Run with detailed output
  python run_all_tests.py market deployment  # Run specific modules
  python run_all_tests.py --summary          # Show available modules

Available modules:
  Infrastructure: imports, protobuf-imports, client, wallet, tx
  Akash:         market, deployment, escrow, provider, cert, audit, inventory, cert-mtls, grpc-client, manifest, discovery-grpc, grpc-standalone
  Cosmos:        bank, staking, distribution, slashing, authz, feegrant, gov, evidence, inflation, ibc
        """
    )

    parser.add_argument(
        'modules',
        nargs='*',
        default=[],
        help='Specific modules to test (default: all)'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show detailed test output'
    )

    parser.add_argument(
        '--summary',
        action='store_true',
        help='Show module summary without running tests'
    )

    args = parser.parse_args()

    if args.summary:
        print("=" * 80)
        print("Available test modules")
        print("=" * 80)

        print("\nINFRASTRUCTURE Modules:")
        for module in ['imports', 'protobuf-imports', 'client', 'wallet', 'tx']:
            config = TEST_MODULES[module]
            print(f"  {module:<20} - {config['converters']} converters")

        print("\nAKASH Modules:")
        for module in ['market', 'deployment', 'escrow', 'provider', 'cert', 'audit', 'inventory',
                       'cert-mtls', 'grpc-client', 'manifest', 'discovery-grpc', 'grpc-standalone']:
            config = TEST_MODULES[module]
            print(f"  {module:<15} - {config['converters']} converters")

        print("\nCOSMOS Modules:")
        for module in ['auth', 'bank', 'staking', 'distribution', 'slashing', 'authz', 'feegrant', 'gov', 'evidence',
                       'inflation', 'ibc']:
            config = TEST_MODULES[module]
            print(f"  {module:<15} - {config['converters']} converters")

        total_converters = sum(m['converters'] for m in TEST_MODULES.values())
        print(f"\nTotal: {len(TEST_MODULES)} modules, {total_converters} converters")
        return

    # Run tests
    runner = TestRunner(verbose=args.verbose)

    modules_to_run = None
    if args.modules:
        invalid_modules = [m for m in args.modules if m not in TEST_MODULES and m != 'all']
        if invalid_modules:
            print(f"❌ Invalid modules: {', '.join(invalid_modules)}")
            print(f"Available modules: {', '.join(TEST_MODULES.keys())}")
            sys.exit(1)

        if 'all' in args.modules:
            modules_to_run = None  # Run all
        else:
            modules_to_run = args.modules

    all_passed = runner.run_all_tests(modules_to_run)

    # Exit with non-zero code if any tests failed
    sys.exit(0 if all_passed else 1)


if __name__ == '__main__':
    main()
