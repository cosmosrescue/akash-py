#!/usr/bin/env python3
"""
End-to-end deployment using USDC denomination on Akash mainnet.

This test validates that the SDK correctly handles:
- USDC IBC denomination in SDL pricing
- Deployment creation with USDC pricing
- Provider bid handling with USDC
- Manifest submission with USDC-priced deployment

USDC Denom: ibc/170C677610AC31DF0904FFE09CD3B5C657492170E7E52372E48756B71E56F2F1
Note: Transaction fees are still paid in AKT (uakt)
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
USDC_DENOM = "ibc/170C677610AC31DF0904FFE09CD3B5C657492170E7E52372E48756B71E56F2F1"


def run_deployment():
    client = AkashClient(MAINNET_RPC, MAINNET_CHAIN)
    wallet = AkashWallet.from_mnemonic(TENANT_MNEMONIC)

    print(f"Wallet: {wallet.address}")

    # Check AKT balance for transaction fees
    akt_balance_raw = client.bank.get_balance(wallet.address, "uakt")
    akt_balance = int(akt_balance_raw) / 1_000_000
    print(f"AKT Balance: {akt_balance:.6f} AKT (for transaction fees)")

    if akt_balance < 0.1:
        print("Insufficient AKT balance for transaction fees (need 0.1 AKT)")
        return False

    # Check USDC balance for deployment pricing
    usdc_balance_raw = client.bank.get_balance(wallet.address, USDC_DENOM)
    usdc_balance = int(usdc_balance_raw) / 1_000_000
    print(f"USDC Balance: {usdc_balance:.6f} USDC")

    if usdc_balance < 0.5:
        print("Insufficient USDC balance (need 5 USDC)")
        return False

    print("\n1. Certificate setup")
    success, cert_pem, key_pem = client.cert.ensure_certificate(wallet)
    if not success:
        print("Certificate setup failed")
        return False
    print("Certificate ready")

    print("\n2. Create USDC-denominated deployment")
    sdl_content = f'''
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
          denom: ibc/170C677610AC31DF0904FFE09CD3B5C657492170E7E52372E48756B71E56F2F1
          amount: 100
deployment:
  nginx:
    global:
      profile: nginx
      count: 1
'''

    deployment = client.deployment.create_deployment(
        sdl_yaml=sdl_content,
        wallet=wallet,
        deposit="5000000",  # 5 USDC
        deposit_denom=USDC_DENOM,
        fee_amount="7000",
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
    for bid in bids:
        provider = bid['bid_id']['provider']
        price = bid['price']['amount']
        denom = bid['price']['denom']

        if denom == USDC_DENOM:
            price_usdc = float(price) / 1_000_000
            print(f"  Provider {provider[:10]}...: {price_usdc:.6f} USDC/block")
        else:
            print(f"  Provider {provider[:10]}...: {price} {denom}/block")

    print("\n4. Select provider")
    provider_addresses = [b['bid_id']['provider'] for b in bids]
    valid_providers = client.provider.filter_valid_providers(provider_addresses)
    if not valid_providers:
        print("No valid providers found")
        return False

    valid_bids = [b for b in bids if b['bid_id']['provider'] in valid_providers]
    best_bid = min(valid_bids, key=lambda b: float(b['price']['amount']))

    provider = best_bid['bid_id']['provider']
    price = best_bid['price']['amount']
    denom = best_bid['price']['denom']

    print(f"Selected provider: {provider}")
    if denom == USDC_DENOM:
        print(f"Price: {float(price) / 1_000_000:.6f} USDC/block")
    else:
        print(f"Price: {price} {denom}/block")

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

    print("\n" + "=" * 60)
    print("USDC denomination deployment complete")
    print(f"Dseq: {dseq}")
    print(f"Provider: {lease['provider_endpoint']}")
    print(f"Pricing: USDC (IBC denom)")
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
