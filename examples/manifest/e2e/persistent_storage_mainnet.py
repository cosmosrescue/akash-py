#!/usr/bin/env python3
"""
Test persistent storage deployment on Akash Network mainnet with minimal resources.

This test demonstrates:
- Persistent storage with class attribute (beta3)
- Storage mount configuration
- Minimal resource deployment for cost efficiency
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
    if TENANT_MNEMONIC == "YOUR_MAINNET_MNEMONIC_HERE":
        print("ERROR: Please set TENANT_MNEMONIC to your mainnet wallet mnemonic")
        return False

    client = AkashClient(MAINNET_RPC, MAINNET_CHAIN)
    wallet = AkashWallet.from_mnemonic(TENANT_MNEMONIC)

    print(f"Wallet: {wallet.address}")

    balance = client.bank.get_balance(wallet.address, "uakt")
    akt_balance = int(balance) / 1_000_000
    print(f"Balance: {akt_balance:.6f} AKT")

    if akt_balance < 0.6:
        print("Insufficient balance (need at least 6 AKT for mainnet deployment)")
        return False

    print("\n1. Certificate setup")
    success, cert_pem, key_pem = client.cert.ensure_certificate(wallet)
    if not success:
        print("Certificate setup failed")
        return False
    print("Certificate ready")

    print("\n2. Create deployment with persistent storage (minimal resources)")
    # Using minimal resources to reduce cost:
    # - Alpine-based image (smaller)
    # - 0.1 CPU (minimum)
    # - 256Mi RAM (minimum)
    # - 512Mi persistent storage (minimal persistent)
    sdl_content = '''
version: "2.0"
services:
  storage-test:
    image: alpine:latest
    expose:
      - port: 8080
        as: 80
        to:
          - global: true
    command:
      - "sh"
      - "-c"
    args:
      - 'echo "Persistent Storage Test - $(date)" > /data/test.txt && echo "Data written to /data/test.txt" && while true; do echo -e "HTTP/1.1 200 OK\r\n\r\nPersistent Storage OK - $(cat /data/test.txt)" | nc -l -p 8080; done'
    params:
      storage:
        data:
          mount: /data
          readOnly: false
profiles:
  compute:
    storage-test:
      resources:
        cpu:
          units: 0.1
        memory:
          size: 256Mi
        storage:
          - size: 512Mi
          - name: data
            size: 512Mi
            attributes:
              persistent: true
              class: beta3
  placement:
    global:
      attributes:
        host: akash
      pricing:
        storage-test:
          denom: uakt
          amount: 10000
deployment:
  storage-test:
    global:
      profile: storage-test
      count: 1
'''

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

    print("\n3. Wait for bids")
    print("Waiting 30 seconds...")
    time.sleep(30)

    bids = client.market.get_bids(owner=wallet.address, dseq=dseq)
    if not bids:
        print("No bids received")
        return False

    print(f"Received {len(bids)} bids")

    print("\n4. Select provider")
    provider_addresses = [b['bid_id']['provider'] for b in bids]
    valid_providers = client.provider.filter_valid_providers(provider_addresses)
    if not valid_providers:
        print("No valid providers found")
        return False

    valid_bids = [b for b in bids if b['bid_id']['provider'] in valid_providers]
    valid_bids_sorted = sorted(valid_bids, key=lambda b: float(b['price']['amount']))

    print(f"\nFound {len(valid_bids_sorted)} valid bids")
    print(f"Lowest bid: {float(valid_bids_sorted[0]['price']['amount']) / 1000000:.6f} AKT/block")

    manifest_result = None
    lease = None

    for idx, bid in enumerate(valid_bids_sorted, 1):
        provider = bid['bid_id']['provider']
        price = bid['price']['amount']

        print(f"\n5. Trying provider {idx}/{len(valid_bids_sorted)}")
        print(f"Provider: {provider}")
        print(f"Price: {float(price) / 1000000:.6f} AKT/block")

        lease = client.market.create_lease_from_bid(wallet, bid)

        if not lease['success']:
            print(f"Lease creation failed: {lease['error']}")
            continue

        print("Lease created")
        print(f"Provider endpoint: {lease['provider_endpoint']}")

        print("\n6. Submit manifest")
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
    print("Persistent storage deployment complete")
    print(f"Dseq: {dseq}")
    print(f"Provider: {lease['provider_endpoint']}")
    print(f"\nResources (minimal):")
    print(f"  - CPU: 0.1 cores")
    print(f"  - RAM: 256Mi")
    print(f"  - Ephemeral Storage: 512Mi")
    print(f"  - Persistent Storage: 512Mi (beta3)")
    print(f"\nEstimated cost: ~{float(valid_bids_sorted[0]['price']['amount']) / 1000000:.6f} AKT/block")
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
