#!/usr/bin/env python3
"""
Wallet module example demonstrating all wallet functionality.

Tests all wallet module functions with mnemonic and address derivation.
Cryptographic module with key management and transaction signing.
"""

import os
import sys
import time
import secrets
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


class WalletE2ETests:
    """E2E tests for Wallet module including all functions."""

    def __init__(self):
        self.test_mnemonic = "poverty torch street hybrid estate message increase play negative vibrant transfer six police tiny garment congress survey tired used audit dolphin focus abstract appear"
        self.expected_address = "akash1qnnhhgzxj24f2kld5yhy4v4h4s9r295ak5gjw4"
        self.test_results = {'passed': 0, 'failed': 0, 'tests': []}

    def test_mnemonic_wallet_creation_lifecycle(self):
        """Test complete mnemonic-based wallet creation lifecycle."""
        print(" Testing mnemonic wallet creation lifecycle...")

        print(" Step 1: Creating wallet from test mnemonic...")
        try:
            wallet = AkashWallet.from_mnemonic(self.test_mnemonic)
            if wallet.address == self.expected_address:
                print(f" Address derivation correct: {wallet.address}")
                step1_success = True
            else:
                print(f" Address mismatch: got {wallet.address}, expected {self.expected_address}")
                return None
        except Exception as e:
            print(f" Wallet creation failed: {str(e)}")
            return None

        print(" Step 2: Validating mnemonic preservation...")
        try:
            if wallet.mnemonic == self.test_mnemonic:
                print(f" Mnemonic preserved: {len(wallet.mnemonic.split())} words")
                step2_success = True
            else:
                print(" Mnemonic not preserved correctly")
                return None
        except Exception as e:
            print(f" Mnemonic validation failed: {str(e)}")
            return None

        print(" Step 3: Validating public key generation...")
        try:
            pub_key_bytes = wallet.public_key_bytes
            if len(pub_key_bytes) == 33:
                print(f" Public key: {len(pub_key_bytes)} bytes (compressed)")
                step3_success = True
            else:
                print(f" Invalid public key length: {len(pub_key_bytes)}")
                return None
        except Exception as e:
            print(f" Public key validation failed: {str(e)}")
            return None

        if step1_success and step2_success and step3_success:
            return f"Mnemonic lifecycle: create -> validate_address -> preserve_mnemonic -> generate_pubkey"
        return None

    def test_new_wallet_generation_lifecycle(self):
        """Test complete new wallet generation lifecycle."""
        print(" Testing new wallet generation lifecycle...")

        print(" Step 1: Generating new 12-word wallet...")
        try:
            new_wallet_12 = AkashWallet.generate(128)  # 128 bits = 12 words
            mnemonic_words = new_wallet_12.mnemonic.split()
            if len(mnemonic_words) == 12:
                print(f" 12-word wallet: {len(mnemonic_words)} words, address: {new_wallet_12.address}")
                step1_success = True
            else:
                print(f" Wrong word count: {len(mnemonic_words)}")
                return None
        except Exception as e:
            print(f" 12-word generation failed: {str(e)}")
            return None

        print(" Step 2: Generating new 24-word wallet...")
        try:
            new_wallet_24 = AkashWallet.generate(256)  # 256 bits = 24 words
            mnemonic_words = new_wallet_24.mnemonic.split()
            if len(mnemonic_words) == 24:
                print(f" 24-word wallet: {len(mnemonic_words)} words, address: {new_wallet_24.address}")
                step2_success = True
            else:
                print(f" Wrong word count: {len(mnemonic_words)}")
                return None
        except Exception as e:
            print(f" 24-word generation failed: {str(e)}")
            return None

        print(" Step 3: Validating wallet uniqueness...")
        try:
            if (new_wallet_12.address != new_wallet_24.address and
                    new_wallet_12.mnemonic != new_wallet_24.mnemonic):
                print(f" Wallets are unique: addresses differ")
                step3_success = True
            else:
                print(" Wallets are not unique")
                return None
        except Exception as e:
            print(f" Uniqueness validation failed: {str(e)}")
            return None

        if step1_success and step2_success and step3_success:
            return f"Generation lifecycle: 12_words -> 24_words -> validate_uniqueness"
        return None

    def test_message_signing_lifecycle(self):
        """Test complete message signing and verification lifecycle."""
        print(" Testing message signing lifecycle...")

        print(" Step 1: Creating wallet for signing...")
        try:
            wallet = AkashWallet.from_mnemonic(self.test_mnemonic)
            test_message = "Hello Akash Network - E2E Test Message"
            print(f" Wallet ready: {wallet.address}")
            print(f" Test message: {test_message}")
            step1_success = True
        except Exception as e:
            print(f" Wallet creation for signing failed: {str(e)}")
            return None

        print(" Step 2: Signing test message...")
        try:
            signature = wallet.sign_message(test_message)
            if signature and len(signature) > 100:
                print(f" Signature: {signature}{signature[-16:]} ({len(signature)} chars)")
                step2_success = True
            else:
                print(f" Invalid signature: {signature}")
                return None
        except Exception as e:
            print(f" Message signing failed: {str(e)}")
            return None

        print(" Step 3: Verifying signature...")
        try:
            is_valid = wallet.verify_signature(test_message, signature)
            if is_valid:
                print(f" Signature verification: VALID")
                step3_success = True
            else:
                print(f" Signature verification: Invalid")
                return None
        except Exception as e:
            print(f" Signature verification failed: {str(e)}")
            return None

        print(" Step 4: Testing invalid signature detection...")
        try:
            corrupted_signature = signature[:-2] + "00"
            is_invalid = wallet.verify_signature(test_message, corrupted_signature)
            if not is_invalid:
                print(f" Corrupted signature correctly rejected")
                step4_success = True
            else:
                print(f" Corrupted signature incorrectly accepted")
                return None
        except Exception as e:
            print(f" Invalid signature test failed: {str(e)}")
            return None

        if step1_success and step2_success and step3_success and step4_success:
            return f"Signing lifecycle: create_wallet -> sign_message -> verify_valid -> reject_invalid"
        return None

    def test_raw_signing_lifecycle(self):
        """Test complete raw data signing lifecycle."""
        print(" Testing raw data signing lifecycle...")

        print(" Step 1: Preparing raw data and wallet...")
        try:
            wallet = AkashWallet.from_mnemonic(self.test_mnemonic)
            test_data = b"Raw transaction data for Akash blockchain"
            print(f" Wallet ready: {wallet.address}")
            print(f" Test data: {len(test_data)} bytes")
            step1_success = True
        except Exception as e:
            print(f" Raw data preparation failed: {str(e)}")
            return None

        print(" Step 2: Signing raw data...")
        try:
            raw_signature = wallet.sign_raw(test_data)
            if raw_signature and len(raw_signature) > 60:
                print(f" Raw signature: {len(raw_signature)} bytes")
                step2_success = True
            else:
                print(f" Invalid raw signature: {raw_signature}")
                return None
        except Exception as e:
            print(f" Raw data signing failed: {str(e)}")
            return None

        print(" Step 3: Testing deterministic signing...")
        try:
            raw_signature2 = wallet.sign_raw(test_data)
            if raw_signature == raw_signature2:
                print(f" Deterministic signing: Consistent")
                step3_success = True
            else:
                print(f" Deterministic signing: Inconsistent")
                return None
        except Exception as e:
            print(f" Deterministic signing test failed: {str(e)}")
            return None

        if step1_success and step2_success and step3_success:
            return f"Raw signing lifecycle: prepare_data -> sign_raw -> verify_deterministic"
        return None

    def test_validation_functions_lifecycle(self):
        """Test complete validation functions lifecycle."""
        print(" Testing validation functions lifecycle...")

        print(" Step 1: Testing mnemonic validation...")
        try:
            valid_result = AkashWallet.validate_mnemonic(self.test_mnemonic)
            invalid_mnemonic = "invalid mnemonic phrase that should not work"
            invalid_result = AkashWallet.validate_mnemonic(invalid_mnemonic)

            if valid_result and not invalid_result:
                print(f" Mnemonic validation: valid=True, invalid=False")
                step1_success = True
            else:
                print(f" Mnemonic validation failed: valid={valid_result}, invalid={invalid_result}")
                return None
        except Exception as e:
            print(f" Mnemonic validation failed: {str(e)}")
            return None

        print(" Step 2: Testing address validation...")
        try:
            valid_addr_result = AkashWallet.validate_address(self.expected_address)
            invalid_addresses = [
                "cosmos1invalid",
                "akash1tooshort",
                "invalid-format",
                "akash1" + "0" * 100
            ]

            invalid_results = [AkashWallet.validate_address(addr) for addr in invalid_addresses]
            all_invalid = not any(invalid_results)

            if valid_addr_result and all_invalid:
                print(f" Address validation: valid=True, all_invalid=False")
                step2_success = True
            else:
                print(f" Address validation failed: valid={valid_addr_result}, invalid_results={invalid_results}")
                return None
        except Exception as e:
            print(f" Address validation failed: {str(e)}")
            return None

        print(" Step 3: Testing private key wallet creation...")
        try:
            private_key_bytes = secrets.token_bytes(32)
            wallet_from_key = AkashWallet.from_private_key(private_key_bytes)

            if wallet_from_key.address.startswith('akash1') and len(wallet_from_key.address) > 40:
                print(f" Private key wallet: {wallet_from_key.address}")
                step3_success = True
            else:
                print(f" Invalid private key wallet: {wallet_from_key.address}")
                return None
        except Exception as e:
            print(f" Private key wallet creation failed: {str(e)}")
            return None

        if step1_success and step2_success and step3_success:
            return f"Validation lifecycle: mnemonic_validation -> address_validation -> private_key_creation"
        return None

    def test_transaction_signing_capability(self):
        """Test transaction signing capability."""
        print(" Testing transaction signing capability...")

        print(" Step 1: Preparing transaction signing...")
        try:
            wallet = AkashWallet.from_mnemonic(self.test_mnemonic)

            tx_data = {
                "chain_id": "sandbox-01",
                "account_number": "123",
                "sequence": "1",
                "fee": {
                    "amount": [{"denom": "uakt", "amount": "5000"}],
                    "gas": "200000"
                },
                "msgs": [{
                    "type": "cosmos-sdk/MsgSend",
                    "value": {
                        "from_address": wallet.address,
                        "to_address": wallet.address,
                        "amount": [{"denom": "uakt", "amount": "1000"}]
                    }
                }],
                "memo": "E2E transaction signing test"
            }
            print(f" Transaction prepared: {tx_data['chain_id']}, sequence {tx_data['sequence']}")
            step1_success = True
        except Exception as e:
            print(f" Transaction preparation failed: {str(e)}")
            return None

        print(" Step 2: Signing transaction...")
        try:
            signed_tx = wallet.sign_transaction(tx_data)

            if (signed_tx and 'signature' in signed_tx and
                    'signature' in signed_tx['signature'] and
                    len(signed_tx['signature']['signature']) > 100):
                print(f" Transaction signed: signature length {len(signed_tx['signature']['signature'])}")
                step2_success = True
            else:
                print(f" Invalid signed transaction: {signed_tx}")
                return None
        except Exception as e:
            print(f" Transaction signing failed: {str(e)}")
            return None

        print(" Step 3: Validating signature format...")
        try:
            signature_data = signed_tx['signature']

            required_fields = ['signature', 'pub_key']
            has_all_fields = all(field in signature_data for field in required_fields)

            pub_key_data = signature_data['pub_key']
            valid_pub_key = (pub_key_data.get('type') == 'tendermint/PubKeySecp256k1' and
                             'value' in pub_key_data and len(pub_key_data['value']) > 60)

            if has_all_fields and valid_pub_key:
                print(f" Signature format: VALID (type: {pub_key_data['type']})")
                step3_success = True
            else:
                print(f" Invalid signature format: fields={has_all_fields}, pubkey={valid_pub_key}")
                return None
        except Exception as e:
            print(f" Signature format validation failed: {str(e)}")
            return None

        if step1_success and step2_success and step3_success:
            return f"Transaction signing: prepare_tx -> sign -> validate_format"
        return None

    def run_all_tests(self):
        """Run all wallet E2E tests."""
        print("Wallet module E2E tests")
        print("=" * 50)

        test_methods = [
            self.test_mnemonic_wallet_creation_lifecycle,
            self.test_new_wallet_generation_lifecycle,
            self.test_message_signing_lifecycle,
            self.test_raw_signing_lifecycle,
            self.test_validation_functions_lifecycle,
            self.test_transaction_signing_capability
        ]

        for test_method in test_methods:
            test_name = test_method.__name__.replace('test_', '').replace('_', ' ')
            print(f"\n{test_name}:")

            try:
                result = test_method()
                if result:
                    print(f" ✅ PASS: {result}")
                    self.test_results['passed'] += 1
                    self.test_results['tests'].append((test_name, 'PASS', result))
                else:
                    print(f" ❌ FAIL: Test did not complete successfully")
                    self.test_results['failed'] += 1
                    self.test_results['tests'].append((test_name, 'FAIL', 'Test incomplete'))
            except Exception as e:
                print(f" ❌ ERROR: {str(e)}")
                self.test_results['failed'] += 1
                self.test_results['tests'].append((test_name, 'ERROR', str(e)[:100]))

            time.sleep(0.5)

        print("\n Test summary")
        print("=" * 30)

        total = self.test_results['passed'] + self.test_results['failed']
        if total > 0:
            success_rate = (self.test_results['passed'] / total) * 100
            print(f"Wallet tests: {self.test_results['passed']}/{total} passed ({success_rate:.1f}%)")

            for test_name, status, details in self.test_results['tests']:
                status_emoji = "✅" if status == "PASS" else "❌"
                print(f" {status_emoji} {test_name}: {details}")
        else:
            print("Wallet tests: no tests completed")

        if total > 0:
            overall_rate = (self.test_results['passed'] / total) * 100
            print(f"\nOVERALL: {self.test_results['passed']}/{total} passed ({overall_rate:.1f}%)")

            if overall_rate >= 95:
                print(" Wallet module: great success!")
                print("✅ All cryptographic functions working")
                print("✅ BIP39/BIP44 derivation working")
                print("✅ Address derivation matches expected")
                print("✅ Message signing and verification working")
                print("✅ Transaction signing capability working")
            elif overall_rate >= 80:
                print("✅ Wallet module: good success!")
                print("Most functionality working correctly")
            else:
                print("⚠️ Wallet module: partial success")
        else:
            print("\n❌ NO tests completed")


def main():
    """Run wallet E2E tests."""
    test_runner = WalletE2ETests()
    test_runner.run_all_tests()


if __name__ == "__main__":
    main()
