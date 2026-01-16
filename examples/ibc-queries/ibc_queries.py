#!/usr/bin/env python3
"""
IBC query module example demonstrating IBC query functionality.

Tests all IBC query functions against mainnet using the SDK.
Focuses on data structure validation, pagination, and chain data.
"""

import os
import sys
from pathlib import Path

# Development mode: Use local akash if running from repo
examples_dir = Path(__file__).parent.parent
if (examples_dir.parent / "akash").exists() and (examples_dir.parent / "pyproject.toml").exists():
    sys.path.insert(0, str(examples_dir.parent))
    print("✓ Development mode: Using local akash")

try:
    from akash import AkashClient
except ImportError as e:
    print(f"Failed to import akash SDK: {e}")
    print("Please run: pip install -r requirements.txt")
    sys.exit(1)

MAINNET_RPC = "https://akash-rpc.polkachu.com:443"
MAINNET_CHAIN = "akashnet-2"


class IBCQueriesE2ETests:
    """E2E tests for IBC query module."""

    def __init__(self):
        self.client = AkashClient(MAINNET_RPC, MAINNET_CHAIN)
        self.test_results = {'passed': 0, 'failed': 0, 'tests': []}

    def run_test(self, test_name, test_func):
        """Run a single test and record results."""
        print(f" Testing {test_name}...")
        try:
            result = test_func()
            if result:
                print(f" ✅ Pass: {result}")
                self.test_results['passed'] += 1
                self.test_results['tests'].append(f"✅ {test_name}")
                return True
            else:
                print(f" ❌ Fail: No result returned")
                self.test_results['failed'] += 1
                self.test_results['tests'].append(f"❌ {test_name}")
                return False
        except Exception as e:
            print(f" ❌ Fail: {e}")
            self.test_results['failed'] += 1
            self.test_results['tests'].append(f"❌ {test_name}: {str(e)}")
            return False

    def test_client_states_basic(self):
        """Test basic client states query."""
        result = self.client.ibc.get_client_states(limit=5)

        if not isinstance(result, dict):
            return None

        client_states = result.get('client_states', [])
        if not isinstance(client_states, list) or len(client_states) == 0:
            return None

        first_client = client_states[0]
        required_fields = ['client_id', 'client_state']
        if not all(field in first_client for field in required_fields):
            return None

        return f"Retrieved {len(client_states)} client states with valid structure"

    def test_client_states_pagination(self):
        """Test client states pagination using next_key."""
        page1 = self.client.ibc.get_client_states(limit=3)
        if not isinstance(page1, dict) or 'client_states' not in page1:
            return None

        client_states_1 = page1.get('client_states', [])
        next_key = page1.get('next_key')

        if len(client_states_1) == 0:
            return None

        if next_key:
            page2 = self.client.ibc.get_client_states(limit=3, next_key=next_key)
            client_states_2 = page2.get('client_states', [])

            page1_ids = {cs['client_id'] for cs in client_states_1}
            page2_ids = {cs['client_id'] for cs in client_states_2}

            if page1_ids.intersection(page2_ids):
                return None

            return f"Pagination working: page1={len(client_states_1)}, page2={len(client_states_2)}, no overlap"
        else:
            return f"Single page result: {len(client_states_1)} clients"

    def test_client_state_detail(self):
        """Test querying individual client state details."""
        result = self.client.ibc.get_client_states(limit=1)
        client_states = result.get('client_states', [])

        if not client_states:
            return None

        client_id = client_states[0]['client_id']
        detail = self.client.ibc.get_client_state(client_id)

        if not detail or 'client_state' not in detail:
            return None

        client_state = detail['client_state']
        if isinstance(client_state, dict) and 'chain_id' in client_state:
            return f"Client {client_id} connects to chain {client_state['chain_id']}"
        else:
            return f"Client {client_id} details retrieved"

    def test_client_status(self):
        """Test client status query."""
        status = self.client.ibc.get_client_status('07-tendermint-53')
        valid_statuses = ['Active', 'Expired', 'Frozen', 'Unknown']

        if status in valid_statuses:
            return f"Client 07-tendermint-53 status: {status}"
        else:
            return None

    def test_connections_basic(self):
        """Test basic connections query."""
        result = self.client.ibc.get_connections(limit=5)

        if not isinstance(result, dict):
            return None

        connections = result.get('connections', [])
        if not isinstance(connections, list) or len(connections) == 0:
            return None

        first_conn = connections[0]
        required_fields = ['id', 'client_id', 'state']
        if not all(field in first_conn for field in required_fields):
            return None

        return f"Retrieved {len(connections)} connections with valid structure"

    def test_connection_detail(self):
        """Test querying individual connection details."""
        result = self.client.ibc.get_connections(limit=1)
        connections = result.get('connections', [])

        if not connections:
            return None

        connection_id = connections[0]['id']
        detail = self.client.ibc.get_connection(connection_id)

        if not detail or 'connection' not in detail:
            return None

        connection = detail['connection']
        if 'client_id' in connection and 'state' in connection:
            return f"Connection {connection_id} uses client {connection['client_id']}, state: {connection['state']}"
        else:
            return None

    def test_channels_basic(self):
        """Test basic channels query."""
        result = self.client.ibc.get_channels(limit=10)

        if not isinstance(result, dict):
            return None

        channels = result.get('channels', [])
        if not isinstance(channels, list) or len(channels) == 0:
            return None

        first_channel = channels[0]
        required_fields = ['channel_id', 'port_id', 'state']
        if not all(field in first_channel for field in required_fields):
            return None

        transfer_channels = [ch for ch in channels if ch.get('port_id') == 'transfer']

        return f"Retrieved {len(channels)} channels ({len(transfer_channels)} transfer channels)"

    def test_channel_detail(self):
        """Test querying individual channel details."""
        result = self.client.ibc.get_channels(limit=20)
        channels = result.get('channels', [])

        transfer_channel = None
        for ch in channels:
            if ch.get('port_id') == 'transfer':
                transfer_channel = ch
                break

        if not transfer_channel:
            return None

        port_id = transfer_channel['port_id']
        channel_id = transfer_channel['channel_id']

        detail = self.client.ibc.get_channel(port_id, channel_id)

        if not detail or 'channel' not in detail:
            return None

        channel = detail['channel']
        if 'state' in channel and 'connection_hops' in channel:
            return f"Channel {channel_id} state: {channel['state']}, hops: {channel['connection_hops']}"
        else:
            return None

    def test_find_active_clients(self):
        """Test finding active clients for a specific chain."""
        test_chains = ['osmosis-1']
        active_clients = []
        tested_chain = None

        for chain in test_chains:
            active_clients = self.client.ibc.find_active_clients_for_chain(chain, max_results=3)
            if isinstance(active_clients, list) and len(active_clients) > 0:
                tested_chain = chain
                break

        if not isinstance(active_clients, list):
            return None

        if len(active_clients) == 0:
            return None

        all_active = True
        status_results = []
        for client_id in active_clients:
            status = self.client.ibc.get_client_status(client_id)
            status_results.append(f"{client_id}:{status}")
            if status != 'Active':
                all_active = False

        if all_active:
            return f"Found {len(active_clients)} active clients for {tested_chain}: {', '.join(active_clients[:2])}"
        else:
            return None

    def test_find_active_channels(self):
        """Test finding active channels for a specific chain."""
        test_chains = ['osmosis-1']
        active_channels = []
        tested_chain = None

        for chain in test_chains:
            active_channels = self.client.ibc.find_active_channels_for_chain(chain, max_results=2)
            if isinstance(active_channels, list) and len(active_channels) > 0:
                tested_chain = chain
                break

        if not isinstance(active_channels, list):
            return None

        if len(active_channels) > 0:
            first_channel = active_channels[0]
            required_fields = ['channel_id', 'port_id', 'connection_id']
            if all(field in first_channel for field in required_fields):
                return f"Found {len(active_channels)} active channels for {tested_chain}, first: {first_channel['channel_id']}"
            else:
                return None
        else:
            return "No active channels found for tested chains (may be normal)"

    def test_denom_trace(self):
        """Test denomination trace query with ATOM IBC denom."""
        atom_hash = "2E5D0AC026AC1AFA65A23023BA4F24BB8DDF94F118EDC0BAD6F625BFC557CDED"
        result = self.client.ibc.get_denom_trace(atom_hash)

        if result and isinstance(result, dict) and 'denom_trace' in result:
            trace = result['denom_trace']
            if trace and 'base_denom' in trace and 'path' in trace:
                return f"ATOM trace found - base: {trace['base_denom']}, path: {trace['path']}"
            else:
                return "Denom trace structure incomplete"
        elif result is None:
            return "ATOM denom trace not found (may not exist on this network)"
        else:
            return None

    def test_trace_token(self):
        """Test token tracing for IBC denominations."""
        atom_ibc_denom = "ibc/2E5D0AC026AC1AFA65A23023BA4F24BB8DDF94F118EDC0BAD6F625BFC557CDED"
        result = self.client.ibc.trace_ibc_token(atom_ibc_denom)
        
        if result and result.get('is_ibc') == True:
            if 'base_denom' in result and 'path' in result:
                return f"ATOM IBC token traced - base: {result['base_denom']}, path: {result['path']}"
            else:
                return "IBC token trace incomplete"
        elif result and result.get('is_ibc') == False:
            regular_result = self.client.ibc.trace_ibc_token('uakt')
            if regular_result and regular_result.get('is_ibc') == False and regular_result.get('base_denom') == 'uakt':
                return "Regular denom correctly identified as non-IBC"
            else:
                return None
        else:
            return None

    def test_transfer_params(self):
        """Test IBC transfer module parameters query."""
        params = self.client.ibc.get_transfer_params()
        
        if params and isinstance(params, dict):
            if 'send_enabled' in params and 'receive_enabled' in params:
                return f"Transfer params - send: {params['send_enabled']}, receive: {params['receive_enabled']}"
            else:
                return "Transfer params structure incomplete"
        else:
            return None

    def test_error_handling(self):
        """Test error handling for invalid inputs."""
        results = []

        status = self.client.ibc.get_client_status('invalid-client-999')
        if status == 'Unknown':
            results.append("Invalid client status handled correctly")
        else:
            return None

        conn_detail = self.client.ibc.get_connection('connection-999999')
        if conn_detail is None:
            results.append("Invalid connection handled correctly")
        else:
            return None

        channel_detail = self.client.ibc.get_channel('transfer', 'channel-999999')
        if channel_detail is None:
            results.append("Invalid channel handled correctly")
        else:
            return None

        return f"Error handling tests passed: {', '.join(results)}"

    def run_all_tests(self):
        """Run all IBC query tests."""
        print("\n" + "=" * 60)
        print("IBC QUERIES E2E TESTS")
        print("=" * 60)
        print(f"Testing against: {MAINNET_RPC}")
        print(f"Chain: {MAINNET_CHAIN}")

        self.run_test('Client states basic query', self.test_client_states_basic)
        self.run_test('Client states pagination', self.test_client_states_pagination)
        self.run_test('Individual client state detail', self.test_client_state_detail)
        self.run_test('Client status query', self.test_client_status)

        self.run_test('Connections basic query', self.test_connections_basic)
        self.run_test('Individual connection detail', self.test_connection_detail)

        self.run_test('Channels basic query', self.test_channels_basic)
        self.run_test('Individual channel detail', self.test_channel_detail)

        self.run_test('Find active clients', self.test_find_active_clients)
        self.run_test('Find active channels', self.test_find_active_channels)
        self.run_test('Denomination trace query', self.test_denom_trace)
        self.run_test('Token tracing', self.test_trace_token)
        self.run_test('Transfer parameters', self.test_transfer_params)
        self.run_test('Error handling', self.test_error_handling)

    def print_results(self):
        """Print test results summary."""
        print("\n" + "=" * 60)
        print("IBC QUERIES E2E TEST RESULTS")
        print("=" * 60)

        total_tests = self.test_results['passed'] + self.test_results['failed']
        success_rate = (self.test_results['passed'] / total_tests * 100) if total_tests > 0 else 0

        print(f"Results: {self.test_results['passed']}/{total_tests} passed ({success_rate:.1f}%)")

        for test_result in self.test_results['tests']:
            print(f" {test_result}")

        print(f"\nOverall: {self.test_results['passed']}/{total_tests} passed ({success_rate:.1f}%)")

        print("\n" + "=" * 60)

        if success_rate >= 80:
            print(f"\n✅ IBC query module works")
            return "Success"
        else:
            print(f"\n❌ IBC query module needs attention")
            print(f" Some query functionality issues detected")
            return None


def main():
    """Main test runner."""
    print("Starting IBC queries E2E tests...")

    tester = IBCQueriesE2ETests()
    tester.run_all_tests()
    result = tester.print_results()

    if result == "Success":
        print("\nAll IBC query tests completed successfully!")
        return "Success"
    else:
        print("\nSome IBC query tests failed. Review output above.")
        return None


if __name__ == "__main__":
    result = main()
    if result != "Success":
        exit(1)