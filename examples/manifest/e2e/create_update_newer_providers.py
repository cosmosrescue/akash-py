#!/usr/bin/env python3
"""
End-to-end deployment example demonstrating complete Akash deployment workflow with manifest updates.

This example demonstrates the full lifecycle of deploying and updating an application on Akash Network:
- Certificate management for mTLS communication with providers
- Deployment creation using SDL
- Market interaction: waiting for bids and selecting providers
- Lease creation with validated providers
- Manifest submission to providers for application deployment
- Manifest update with modified SDL configuration
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

    print("\n2. Create deployment")
    sdl_content = '''
version: "2.0"
services:
  nginx:
    image: nginx:alpine
    expose:
      - port: 80
        as: 80
        to:
          - global: true
profiles:
  compute:
    nginx:
      resources:
        cpu:
          units: 0.1
        memory:
          size: 128Mi
        storage:
          size: 512Mi
  placement:
    global:
      attributes:
        host: akash
      pricing:
        nginx:
          denom: uakt
          amount: 1000
deployment:
  nginx:
    global:
      profile: nginx
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

    print("\n4. Select Provider (v0.7+ only)")
    provider_addresses = [b['bid_id']['provider'] for b in bids]
    valid_providers = client.provider.filter_valid_providers(provider_addresses)
    if not valid_providers:
        print("No valid providers found")
        return False

    valid_bids = [b for b in bids if b['bid_id']['provider'] in valid_providers]

    import requests
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    modern_bids = []
    print(f"Checking {len(valid_bids)} valid bids for provider versions...")

    for bid in valid_bids:
        provider_addr = bid['bid_id']['provider']
        try:
            provider_info = client.provider.get_provider(provider_addr)
            if not provider_info or 'host_uri' not in provider_info:
                print(f"  ❌ {provider_addr}: No host_uri found")
                continue

            host_uri = provider_info['host_uri']

            response = requests.get(f"{host_uri}/version", timeout=3, verify=False)
            if response.status_code == 200:
                data = response.json()
                version = data.get('akash', {}).get('version', 'unknown')

                if version.startswith('v0.'):
                    version_parts = version[1:].split('.')
                    if len(version_parts) >= 2:
                        major, minor = int(version_parts[0]), int(version_parts[1].split('-')[0])
                        if major == 0 and minor >= 7:
                            print(f"  ✅ {provider_addr}: {version} (modern)")
                            modern_bids.append(bid)
                        else:
                            print(f"  {provider_addr}: {version} (legacy, skipped)")
                else:
                    print(f"  ⚠️  {provider_addr}: {version} (unknown format)")
            else:
                print(f"  ❌ {provider_addr}: HTTP {response.status_code}")
        except Exception as e:
            print(f"  ❌ {provider_addr}: {str(e)[:50]}")

    if not modern_bids:
        print("\n❌ No modern providers (v0.7+) found in bids")
        print(f" Total bids: {len(bids)}, Valid: {len(valid_bids)}, Modern: 0")
        return False

    print(f"\nFound {len(modern_bids)} modern provider(s)")
    best_bid = min(modern_bids, key=lambda b: float(b['price']['amount']))

    provider = best_bid['bid_id']['provider']
    price = best_bid['price']['amount']

    print(f"Selected provider: {provider}")
    print(f"Price: {float(price) / 1000000:.6f} AKT/block")

    print("\n5. Create lease")
    lease = client.market.create_lease_from_bid(wallet, best_bid)

    if not lease['success']:
        print(f"Lease failed: {lease['error']}")
        return False

    print("Lease created")
    print(f"Provider endpoint: {lease['provider_endpoint']}")
    print(f"Tx: {lease['tx_hash']}")

    print("\n6. Submit manifest")
    print("Waiting 10 seconds for lease...")
    time.sleep(10)

    manifest_result = client.manifest.submit_manifest(
        provider_endpoint=lease['provider_endpoint'],
        lease_id=lease['lease_id'],
        sdl_content=sdl_content,
        cert_pem=cert_pem,
        key_pem=key_pem
    )

    if manifest_result.get('status') != 'success':
        print(f"Manifest failed: {manifest_result.get('error')}")
        return False

    print("Manifest submitted successfully")
    print(f"Provider version: {manifest_result.get('provider_version')}")
    print(f"Method: {manifest_result.get('method')}")

    print("\n7. Manifest update test")
    print("Waiting 30 seconds before updating manifest...")
    time.sleep(30)

    updated_sdl_content = '''
version: "2.0"
services:
  nginx:
    image: nginx:alpine
    command: ["/bin/sh", "-c", "echo 'Updated container' && nginx -g 'daemon off;'"]
    env:
      - UPDATE_VERSION=v2
      - DEPLOYMENT_UPDATE=true
    expose:
      - port: 80
        as: 80
        to:
          - global: true
profiles:
  compute:
    nginx:
      resources:
        cpu:
          units: 0.1
        memory:
          size: 128Mi
        storage:
          size: 512Mi
  placement:
    global:
      attributes:
        host: akash
      pricing:
        nginx:
          denom: uakt
          amount: 1000
deployment:
  nginx:
    global:
      profile: nginx
      count: 1
'''

    print("Step 1: Updating deployment on-chain...")

    update_result = client.deployment.update_deployment(
        wallet=wallet,
        sdl_yaml=updated_sdl_content,
        owner=wallet.address,
        dseq=dseq,
        fee_amount="5000"
    )

    if not update_result.success:
        print(f"Deployment update transaction failed: {update_result.raw_log}")
        print("Cannot proceed with manifest update without on-chain update")
        return True

    print(f"Deployment updated on-chain: tx {update_result.tx_hash}")
    print("Waiting 10 seconds for transaction to propagate...")
    time.sleep(10)

    print("\nStep 2: Submitting updated manifest to provider...")

    updated_manifest_result = client.manifest.submit_manifest(
        provider_endpoint=lease['provider_endpoint'],
        lease_id=lease['lease_id'],
        sdl_content=updated_sdl_content,
        cert_pem=cert_pem,
        key_pem=key_pem
    )

    if updated_manifest_result.get('status') != 'success':
        print(f"Updated manifest submission failed: {updated_manifest_result.get('error')}")
    else:
        print("Updated manifest submitted successfully!")
        print(f"Update method: {updated_manifest_result.get('method')}")
        print(" env | grep -E 'UPDATE_VERSION|DEPLOYMENT_UPDATE'")

    print("\n" + "=" * 60)
    print("Deployment complete")
    print(f"Dseq: {dseq}")
    print(f"Provider: {lease['provider_endpoint']}")

    if updated_manifest_result.get('status') != 'success':
        print("\n⚠️  Manifest update failed - original deployment is still running")
    else:
        print("\n✅ Initial deployment and manifest update completed")

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
