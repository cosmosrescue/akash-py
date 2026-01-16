#!/usr/bin/env python3
"""
Test IP lease endpoint deployment on Akash Network testnet.

This test demonstrates:
- SHARED_HTTP endpoint (TCP port 80) - kind 0
- LEASED_IP endpoint - kind 2 with sequence number
- IP endpoint definition in SDL
- Correct endpoint kind determination with IP lease
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

MAINNET_RPC = "https://akash-rpc.polkachu.com:443"
MAINNET_CHAIN = "akashnet-2"
TENANT_MNEMONIC = "poverty torch street hybrid estate message increase play negative vibrant transfer six police tiny garment congress survey tired used audit dolphin focus abstract appear"


def run_deployment():
    client = AkashClient(MAINNET_RPC, MAINNET_CHAIN)
    wallet = AkashWallet.from_mnemonic(TENANT_MNEMONIC)

    print(f"Wallet: {wallet.address}")

    balance = client.bank.get_balance(wallet.address, "uakt")
    akt_balance = int(balance) / 1_000_000
    print(f"Balance: {akt_balance:.6f} AKT")

    if akt_balance < 0.6:
        print("Insufficient balance (need 0.6 AKT)")
        return False

    print("\n1. Certificate setup")
    success, cert_pem, key_pem = client.cert.ensure_certificate(wallet)
    if not success:
        print("Certificate setup failed")
        return False
    print("Certificate ready")

    print("\n2. Create IP lease deployment")
    sdl_content = '''
version: "2.0"

endpoints:
  myendpoint:
    kind: ip

services:
  web:
    image: nginx:alpine
    expose:
      - port: 80
        as: 80
        to:
          - global: true
            ip: "myendpoint"

profiles:
  compute:
    web:
      resources:
        cpu:
          units: 0.5
        memory:
          size: 512Mi
        storage:
          size: 1Gi
  placement:
    global:
      attributes:
        host: akash
      pricing:
        web:
          denom: uakt
          amount: 1000

deployment:
  web:
    global:
      profile: web
      count: 1
'''

    print("\n3. Verify endpoint configuration")
    import yaml
    sdl_data = yaml.safe_load(sdl_content)
    groups = client.deployment._create_groups_from_sdl(sdl_data)
    endpoints = groups[0]['resources'][0]['endpoints']

    print("Generated endpoints:")
    import json
    print(json.dumps(endpoints, indent=2))

    expected_endpoints = [
        {"sequence_number": 0},           # HTTP on port 80 - SHARED_HTTP (kind 0, omitted)
        {"kind": 2, "sequence_number": 1}  # IP lease "myendpoint" - LEASED_IP (kind 2, seq 1)
    ]

    if endpoints == expected_endpoints:
        print("✅ Endpoints match expected configuration")
        print("   - HTTP (TCP:80) → SHARED_HTTP endpoint (kind 0)")
        print("   - IP lease 'myendpoint' → LEASED_IP endpoint (kind 2, seq 1)")
    else:
        print("❌ Endpoint mismatch!")
        print(f"Expected: {json.dumps(expected_endpoints, indent=2)}")
        return False

    print("\n4. Create deployment")
    deployment = client.deployment.create_deployment(
        sdl_yaml=sdl_content,
        wallet=wallet,
        deposit="500000",
        fee_amount="5000",
        memo=""
    )

    if not deployment.success:
        print(f"Deployment failed: {deployment.raw_log}")
        return False

    dseq = deployment.dseq
    print(f"Deployment created: dseq {dseq}")
    print(f"Tx: {deployment.tx_hash}")

    print("\n5. Wait for bids")
    print("Waiting 30 seconds...")
    time.sleep(30)

    bids = client.market.get_bids(owner=wallet.address, dseq=dseq)
    if not bids:
        print("No bids received")
        return False

    print(f"Received {len(bids)} bids")

    print("\n6. Select provider")
    provider_addresses = [b['bid_id']['provider'] for b in bids]
    valid_providers = client.provider.filter_valid_providers(provider_addresses)
    if not valid_providers:
        print("No valid providers found")
        return False

    valid_bids = [b for b in bids if b['bid_id']['provider'] in valid_providers]
    valid_bids_sorted = sorted(valid_bids, key=lambda b: float(b['price']['amount']))

    manifest_result = None
    lease = None

    for idx, bid in enumerate(valid_bids_sorted, 1):
        provider = bid['bid_id']['provider']
        price = bid['price']['amount']

        print(f"\n7. Trying provider {idx}/{len(valid_bids_sorted)}")
        print(f"Provider: {provider}")
        print(f"Price: {float(price) / 1000000:.6f} AKT/block")

        lease = client.market.create_lease_from_bid(wallet, bid)

        if not lease['success']:
            print(f"Lease creation failed: {lease['error']}")
            continue

        print("Lease created")
        print(f"Provider endpoint: {lease['provider_endpoint']}")

        print("\n8. Verify manifest endpoints")
        manifest_parse = client.manifest.parse_sdl(sdl_content)
        if manifest_parse['status'] == 'success':
            manifest_endpoints = manifest_parse['manifest_data'][0]['Services'][0]['resources']['endpoints']
            print("Manifest endpoints:")
            print(json.dumps(manifest_endpoints, indent=2))

            if manifest_endpoints == expected_endpoints:
                print("✅ Manifest endpoints match deployment message")
            else:
                print("❌ Manifest endpoint mismatch!")
                return False

        print("\n9. Submit manifest")
        print("Waiting 10 seconds...")
        time.sleep(10)

        manifest_result = client.manifest.submit_manifest(
            provider_endpoint=lease['provider_endpoint'],
            lease_id=lease['lease_id'],
            sdl_content=sdl_content,
            cert_pem=cert_pem,
            key_pem=key_pem
        )

        if manifest_result.get('status') == 'success':
            print(f"Manifest submitted successfully")
            print(f"Provider version: {manifest_result.get('provider_version')}")
            print(f"Method: {manifest_result.get('method')}")
            break
        else:
            print(f"Manifest submission failed: {manifest_result.get('error')}")

    if not manifest_result or manifest_result.get('status') != 'success':
        print("All providers failed")
        return False

    print("\n" + "=" * 60)
    print("IP lease endpoint deployment complete")
    print(f"Dseq: {dseq}")
    print(f"Provider: {lease['provider_endpoint']}")
    print("\nEndpoint configuration:")
    print("  HTTP (TCP):  Port 80  → SHARED_HTTP (kind 0)")
    print("  IP Lease:    'myendpoint' → LEASED_IP (kind 2, sequence 1)")
    print("\nBoth deployment message and manifest have correct endpoint kinds")
    print("=" * 60)

    return True


if __name__ == "__main__":
    try:
        success = run_deployment()
        if not success:
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
