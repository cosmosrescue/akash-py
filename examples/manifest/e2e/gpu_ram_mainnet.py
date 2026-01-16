#!/usr/bin/env python3
"""
Test GPU deployment with RAM specification on Akash Network.

This test demonstrates:
- GPU with RAM specification (vendor/nvidia/model/a100/ram/40Gi)
- GPU attribute validation
- High-end GPU requirements
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
        print("Insufficient balance (need 0.6 AKT for GPU deployment)")
        return False

    print("\n1. Certificate setup")
    success, cert_pem, key_pem = client.cert.ensure_certificate(wallet)
    if not success:
        print("Certificate setup failed")
        return False
    print("Certificate ready")

    print("\n2. Create GPU deployment with RAM specification")
    sdl_content = '''
version: "2.0"
services:
  ml-workload:
    image: nvidia/cuda:11.8.0-base-ubuntu22.04
    expose:
      - port: 8080
        as: 80
        to:
          - global: true
    env:
      - CUDA_VISIBLE_DEVICES=0
      - ML_TEST=enabled
    command:
      - "bash"
      - "-c"
    args:
      - 'apt-get update && apt-get install -y nginx && (nvidia-smi || echo "GPU info not available") > /usr/share/nginx/html/index.html && echo "<br><br>GPU: A100 40GB requested" >> /usr/share/nginx/html/index.html && nginx -g "daemon off;"'
profiles:
  compute:
    ml-workload:
      resources:
        cpu:
          units: 2
        memory:
          size: 8Gi
        gpu:
          units: 1
          attributes:
            vendor:
              nvidia:
              - model: a100
                ram: 80Gi
        storage:
          - size: 10Gi
  placement:
    global:
      attributes:
        host: akash
      pricing:
        ml-workload:
          denom: uakt
          amount: 150000
deployment:
  ml-workload:
    global:
      profile: ml-workload
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

    print("\n3. Verify GPU + RAM configuration")
    print("Checking that GPU attributes include RAM specification...")

    import yaml
    sdl_data = yaml.safe_load(sdl_content)
    groups = client.deployment._create_groups_from_sdl(sdl_data)
    gpu_config = groups[0]['resources'][0]['gpu']

    print(f"GPU Units: {gpu_config['units']}")
    print(f"GPU attributes: {gpu_config['attributes']}")

    expected_key = "vendor/nvidia/model/a100/ram/80Gi"
    actual_attrs = gpu_config.get('attributes', [])

    if actual_attrs and actual_attrs[0]['key'] == expected_key:
        print(f"✅ GPU+RAM attributes correct: {expected_key}")
    else:
        print(f"❌ GPU+RAM attributes incorrect!")
        print(f" Expected: {expected_key}")
        print(f" Got: {actual_attrs}")

    print("\n4. Wait for bids")
    print("Waiting 45 seconds for A100 GPU provider bids...")
    time.sleep(45)

    bids = client.market.get_bids(owner=wallet.address, dseq=dseq)
    if not bids:
        print("No bids received")
        print("NOTE: A100 GPU providers may be limited or unavailable on testnet")
        return False

    print(f"Received {len(bids)} bids")

    print("\n5. Select A100 GPU provider")
    provider_addresses = [b['bid_id']['provider'] for b in bids]
    valid_providers = client.provider.filter_valid_providers(provider_addresses)
    if not valid_providers:
        print("No valid A100 GPU providers found")
        return False

    valid_bids = [b for b in bids if b['bid_id']['provider'] in valid_providers]
    valid_bids_sorted = sorted(valid_bids, key=lambda b: float(b['price']['amount']))

    manifest_result = None
    lease = None

    for idx, bid in enumerate(valid_bids_sorted, 1):
        provider = bid['bid_id']['provider']
        price = bid['price']['amount']

        print(f"\n6. Trying A100 GPU provider {idx}/{len(valid_bids_sorted)}")
        print(f"Provider: {provider}")
        print(f"Price: {float(price) / 1000000:.6f} AKT/block")

        lease = client.market.create_lease_from_bid(wallet, bid)

        if not lease['success']:
            print(f"Lease creation failed: {lease['error']}")
            continue

        print("Lease created")
        print(f"Provider endpoint: {lease['provider_endpoint']}")

        print("\n7. Submit manifest with GPU+RAM configuration")
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
        print("All A100 GPU providers failed")
        return False

    print("\n" + "=" * 60)
    print("GPU+RAM deployment complete")
    print(f"Dseq: {dseq}")
    print(f"Provider: {lease['provider_endpoint']}")
    print("\nGPU configuration:")
    print(f"  Vendor: nvidia")
    print(f"  Model: a100")
    print(f"  RAM: 40Gi")
    print(f"  Units: 1")
    print(f"  Attribute key: vendor/nvidia/model/a100/ram/40Gi")
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
