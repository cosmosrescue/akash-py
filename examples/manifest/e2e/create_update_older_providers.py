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


def print_manifest(manifest, title):
    """Print manifest in a readable format."""
    print(f"\n{'=' * 60}")
    print(f"{title}")
    print('=' * 60)

    if not manifest or (isinstance(manifest, dict) and manifest.get("status") == "failed"):
        print(f"Error: {manifest.get('error', 'No manifest') if isinstance(manifest, dict) else 'No manifest'}")
        return

    group_name = manifest.get('name')
    if not group_name:
        print("No manifest found")
        return

    print(f"\nGroup: {group_name}")
    if 'status' in manifest:
        print(f"Status: {manifest['status']}")
    if 'retrieved_at' in manifest:
        print(f"Retrieved: {manifest['retrieved_at']}")

    services = manifest.get('services', [])
    print(f"\nServices ({len(services)}):")
    for service in services:
        print(f"\n Service: {service.get('name', 'unknown')}")
        print(f" Image: {service.get('image', 'unknown')}")
        print(f" Count: {service.get('count', 0)}")

        if 'command' in service and service['command']:
            print(f" Command: {service['command']}")

        if 'args' in service and service['args']:
            print(f" Args: {service['args']}")

        if 'env' in service and service['env']:
            print(f" Environment: {service['env']}")

        if 'resources' in service:
            resources = service['resources']
            print(f" Resources:")
            if 'cpu' in resources:
                cpu_val = resources['cpu'].get('units', {}).get('val', '0')
                print(f" CPU: {cpu_val} millicores")

            if 'memory' in resources:
                mem_val = resources['memory'].get('size', {}).get('val', '0')
                print(f" Memory: {mem_val} bytes")

            if 'storage' in resources:
                for storage in resources['storage']:
                    storage_name = storage.get('name', 'default')
                    storage_val = storage.get('size', {}).get('val', '0')
                    print(f" Storage ({storage_name}): {storage_val} bytes")

            if 'gpu' in resources:
                gpu_val = resources['gpu'].get('units', {}).get('val', '0')
                print(f" GPU: {gpu_val} units")

        if 'expose' in service:
            print(f" Exposed ports ({len(service['expose'])}):")
            for expose in service['expose']:
                proto = expose.get('proto', 'TCP')
                print(f" Port {expose.get('port')} ({proto}) - Global: {expose.get('global', False)}")

        if 'params' in service and service['params']:
            print(f" Params:")
            if 'storage' in service['params']:
                for sp in service['params']['storage']:
                    print(f" Storage: {sp.get('name', '')} -> {sp.get('mount', '')} (read_only: {sp.get('read_only', False)})")

        if 'credentials' in service and service['credentials']:
            print(f" Credentials: host={service['credentials'].get('host', '')}, username={service['credentials'].get('username', '')}")


def compare_manifests(manifest1, manifest2):
    """Compare two manifests and show differences."""
    print(f"\n{'=' * 60}")
    print("MANIFEST COMPARISON")
    print('=' * 60)

    if manifest1.get("status") == "failed" or manifest2.get("status") == "failed":
        print("Cannot compare - one or both manifests failed to load")
        return

    if "name" not in manifest1 or "name" not in manifest2:
        print("Cannot compare - one or both manifests not found")
        return

    services1 = {s['name']: s for s in manifest1.get('services', [])}
    services2 = {s['name']: s for s in manifest2.get('services', [])}

    all_services = set(services1.keys()) | set(services2.keys())

    for service_name in sorted(all_services):
        print(f"\nService: {service_name}")

        s1 = services1.get(service_name)
        s2 = services2.get(service_name)

        if not s1:
            print(" Added in updated manifest")
            continue
        if not s2:
            print(" Removed in updated manifest")
            continue

        if s1.get('image') != s2.get('image'):
            print(f" Image changed:")
            print(f" Before: {s1.get('image')}")
            print(f" After: {s2.get('image')}")

        if s1.get('count') != s2.get('count'):
            print(f" Count changed:")
            print(f" Before: {s1.get('count')}")
            print(f" After: {s2.get('count')}")

        cmd1 = s1.get('command')
        cmd2 = s2.get('command')
        if cmd1 != cmd2:
            print(f" Command changed:")
            print(f" Before: {cmd1 if cmd1 else 'Not set'}")
            print(f" After: {cmd2 if cmd2 else 'Not set'}")

        args1 = s1.get('args')
        args2 = s2.get('args')
        if args1 != args2:
            print(f" Args changed:")
            print(f" Before: {args1 if args1 else 'Not set'}")
            print(f" After: {args2 if args2 else 'Not set'}")

        env1 = s1.get('env')
        env2 = s2.get('env')
        if env1 != env2:
            print(f" Environment changed:")
            print(f" Before: {env1 if env1 else 'Not set'}")
            print(f" After: {env2 if env2 else 'Not set'}")

        params1 = s1.get('params')
        params2 = s2.get('params')
        if params1 != params2:
            print(f" Params changed:")
            print(f" Before: {params1 if params1 else 'Not set'}")
            print(f" After: {params2 if params2 else 'Not set'}")

        creds1 = s1.get('credentials')
        creds2 = s2.get('credentials')
        if creds1 != creds2:
            print(f" Credentials changed:")
            print(f" Before: {creds1 if creds1 else 'Not set'}")
            print(f" After: {creds2 if creds2 else 'Not set'}")

        res1 = s1.get('resources', {})
        res2 = s2.get('resources', {})

        if res1 != res2:
            print(f" Resources changed:")
            for resource_type in ['cpu', 'memory', 'gpu']:
                r1 = res1.get(resource_type, {}).get('units')
                r2 = res2.get(resource_type, {}).get('units')
                if r1 != r2:
                    print(f" {resource_type.upper()}:")
                    print(f" Before: {r1 if r1 else 'Not set'}")
                    print(f" After: {r2 if r2 else 'Not set'}")

            storage1 = res1.get('storage', [])
            storage2 = res2.get('storage', [])
            if storage1 != storage2:
                print(f" Storage:")
                print(f" Before: {storage1}")
                print(f" After: {storage2}")

    if all(services1.get(name) == services2.get(name) for name in all_services if name in services1 and name in services2):
        print("\nNo changes detected between manifests")


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

    print("\n7. Query initial manifest from provider")
    print("Waiting 10 seconds for manifest to be available...")
    time.sleep(10)

    initial_manifest = client.manifest.get_deployment_manifest(
        provider_endpoint=lease['provider_endpoint'],
        lease_id=lease['lease_id'],
        cert_pem=cert_pem,
        key_pem=key_pem
    )

    if initial_manifest.get("status") == "success":
        manifest_groups = initial_manifest.get("manifest", [])
        if manifest_groups:
            print_manifest(manifest_groups[0], "INITIAL MANIFEST (from provider)")
    else:
        print(f"Failed to query initial manifest: {initial_manifest.get('error')}")

    print("\n8. Manifest update test")
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

        print("\nStep 3: Query updated manifest from provider...")
        print("Waiting 10 seconds for manifest to propagate...")
        time.sleep(10)

        updated_manifest_query = client.manifest.get_deployment_manifest(
            provider_endpoint=lease['provider_endpoint'],
            lease_id=lease['lease_id'],
            cert_pem=cert_pem,
            key_pem=key_pem
        )

        if updated_manifest_query.get("status") == "success":
            manifest_groups = updated_manifest_query.get("manifest", [])
            if manifest_groups:
                updated_manifest = manifest_groups[0]
                print_manifest(updated_manifest, "UPDATED MANIFEST (from provider)")

                if initial_manifest.get("status") == "success":
                    initial_groups = initial_manifest.get("manifest", [])
                    if initial_groups:
                        compare_manifests(initial_groups[0], updated_manifest)
        else:
            print(f"Failed to query updated manifest: {updated_manifest_query.get('error')}")

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
