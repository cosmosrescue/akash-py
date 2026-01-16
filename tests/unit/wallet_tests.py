#!/usr/bin/env python3
"""
Wallet tests - validation and functional tests.

Validation tests: Validate AkashWallet class structures, BIP39/BIP44 patterns,
address generation compatibility, and cryptographic operation support without requiring
blockchain interactions. 

Functional tests: Test key derivation, address generation, mnemonic handling,
transaction signing, and cryptographic operations using mocking to isolate functionality
and test error handling scenarios.

Run: python wallet_tests.py
"""

import os

os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

import pytest
import sys
import os
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from akash.wallet import AkashWallet


class TestAkashWalletInitialization:
    """Test AkashWallet initialization and factory methods."""

    def test_wallet_from_mnemonic_standard(self):
        """Test wallet creation from standard test mnemonic."""
        test_mnemonic = ("poverty torch street hybrid estate message increase play negative "
                         "vibrant transfer six police tiny garment congress survey tired used "
                         "audit dolphin focus abstract appear")

        wallet = AkashWallet.from_mnemonic(test_mnemonic)

        assert wallet.address == "akash1qnnhhgzxj24f2kld5yhy4v4h4s9r295ak5gjw4"
        assert wallet.mnemonic == test_mnemonic
        assert wallet.public_key is not None
        assert len(wallet.public_key_bytes) == 33

    def test_wallet_from_mnemonic_with_passphrase(self):
        """Test wallet creation with BIP39 passphrase."""
        test_mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
        passphrase = "test_passphrase"

        wallet1 = AkashWallet.from_mnemonic(test_mnemonic)
        wallet2 = AkashWallet.from_mnemonic(test_mnemonic, passphrase)

        assert wallet1.address != wallet2.address
        assert wallet1.mnemonic == wallet2.mnemonic == test_mnemonic

    def test_wallet_from_private_key(self):
        """Test wallet creation from private key bytes."""
        private_key_bytes = b'\x01' * 32

        wallet = AkashWallet.from_private_key(private_key_bytes)

        assert wallet.address is not None
        assert wallet.address.startswith('akash1')
        assert wallet.mnemonic is None
        assert len(wallet.public_key_bytes) == 33

    def test_wallet_generate_default_strength(self):
        """Test generating new wallet with default entropy strength."""
        wallet = AkashWallet.generate()

        assert wallet.address is not None
        assert wallet.address.startswith('akash1')
        assert wallet.mnemonic is not None
        assert len(wallet.mnemonic.split()) == 12
        assert len(wallet.public_key_bytes) == 33

    def test_wallet_generate_different_strengths(self):
        """Test generating wallets with different entropy strengths."""
        strength_to_words = {
            128: 12,
            160: 15,
            192: 18,
            224: 21,
            256: 24
        }

        for strength, expected_words in strength_to_words.items():
            wallet = AkashWallet.generate(strength)
            word_count = len(wallet.mnemonic.split())
            assert word_count == expected_words

    def test_wallet_generate_unique_addresses(self):
        """Test that generated wallets have unique addresses."""
        wallet1 = AkashWallet.generate()
        wallet2 = AkashWallet.generate()

        assert wallet1.address != wallet2.address
        assert wallet1.mnemonic != wallet2.mnemonic


class TestAkashWalletMnemonicValidation:
    """Test mnemonic validation functionality."""

    def test_validate_mnemonic_valid(self):
        """Test validation of valid BIP39 mnemonics."""
        valid_mnemonics = [
            "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about",
            "poverty torch street hybrid estate message increase play negative vibrant transfer six police tiny garment congress survey tired used audit dolphin focus abstract appear",
            "legal winner thank year wave sausage worth useful legal winner thank yellow"
        ]

        for mnemonic in valid_mnemonics:
            assert AkashWallet.validate_mnemonic(mnemonic) is True

    def test_validate_mnemonic_invalid(self):
        """Test validation of invalid mnemonics."""
        invalid_mnemonics = [
            "invalid mnemonic phrase",
            "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon",
            "",
            "single",
            "abandon " * 11 + "invalid"
        ]

        for mnemonic in invalid_mnemonics:
            assert AkashWallet.validate_mnemonic(mnemonic) is False

    def test_from_mnemonic_invalid_phrase(self):
        """Test wallet creation with invalid mnemonic."""
        invalid_mnemonic = "invalid mnemonic phrase here"

        with pytest.raises(ValueError, match="Invalid mnemonic phrase"):
            AkashWallet.from_mnemonic(invalid_mnemonic)


class TestAkashWalletAddressValidation:
    """Test address validation functionality."""

    def test_validate_address_valid(self):
        """Test validation of valid Akash addresses."""
        valid_addresses = [
            "akash1qnnhhgzxj24f2kld5yhy4v4h4s9r295ak5gjw4"
        ]

        for address in valid_addresses:
            assert AkashWallet.validate_address(address) is True

    def test_validate_address_invalid(self):
        """Test validation of invalid addresses."""
        invalid_addresses = [
            "akash1",
            "cosmos1qnnhhgzxj24f2kld5yhy4v4h4s9r295ak5gjw4",
            "akash1invalid",
            "",
            "not_an_address",
            "akash1qnnhhgzxj24f2kld5yhy4v4h4s9r295ak5gjw4extra"
        ]

        for address in invalid_addresses:
            assert AkashWallet.validate_address(address) is False


class TestAkashWalletAddressDerivation:
    """Test address derivation functionality."""

    def test_address_derivation_consistency(self):
        """Test that address derivation is consistent."""
        mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"

        wallet1 = AkashWallet.from_mnemonic(mnemonic)
        wallet2 = AkashWallet.from_mnemonic(mnemonic)

        assert wallet1.address == wallet2.address

    def test_address_format(self):
        """Test address format correctness."""
        wallet = AkashWallet.generate()

        assert wallet.address.startswith('akash1')
        assert len(wallet.address) >= 39
        assert len(wallet.address) <= 59

    def test_address_derivation_with_ripemd160_available(self):
        """Test that address derivation works correctly with RIPEMD160."""
        wallet = AkashWallet.generate()

        assert wallet.address.startswith('akash1')
        assert len(wallet.address) == 44

        mnemonic = wallet.mnemonic
        wallet2 = AkashWallet.from_mnemonic(mnemonic)
        assert wallet.address == wallet2.address

    def test_public_key_compression(self):
        """Test public key is properly compressed."""
        wallet = AkashWallet.generate()

        assert len(wallet.public_key_bytes) == 33
        assert wallet.public_key_bytes[0] in [0x02, 0x03]


class TestAkashWalletSigning:
    """Test transaction and message signing functionality."""

    def test_sign_message(self):
        """Test message signing functionality."""
        wallet = AkashWallet.generate()
        message = "Hello Akash Network"

        signature = wallet.sign_message(message)

        assert isinstance(signature, str)
        assert len(signature) > 0
        bytes.fromhex(signature)

    def test_sign_message_verify(self):
        """Test message signing and verification."""
        wallet = AkashWallet.generate()
        message = "Test message for verification"

        signature = wallet.sign_message(message)

        is_valid = wallet.verify_signature(message, signature)
        assert is_valid is True

    def test_verify_signature_invalid(self):
        """Test signature verification with invalid signature."""
        wallet = AkashWallet.generate()
        message = "Test message"

        invalid_signature = "deadbeef" * 16

        is_valid = wallet.verify_signature(message, invalid_signature)
        assert is_valid is False

    def test_verify_signature_wrong_message(self):
        """Test signature verification with wrong message."""
        wallet = AkashWallet.generate()

        original_message = "Original message"
        different_message = "Different message"

        signature = wallet.sign_message(original_message)

        is_valid = wallet.verify_signature(different_message, signature)
        assert is_valid is False

    def test_sign_raw_data(self):
        """Test raw data signing."""
        wallet = AkashWallet.generate()
        test_data = b"raw test data for signing"

        signature = wallet.sign_raw(test_data)

        assert isinstance(signature, bytes)
        assert len(signature) > 0

    def test_sign_transaction_structure(self):
        """Test transaction signing returns proper structure."""
        wallet = AkashWallet.generate()

        tx_data = {
            "chain_id": "akashnet-2",
            "account_number": "123",
            "sequence": "1",
            "fee": {"amount": [{"denom": "uakt", "amount": "5000"}], "gas": "200000"},
            "msgs": [{"type": "cosmos-sdk/MsgSend", "value": {"from": "addr1", "to": "addr2"}}],
            "memo": "test transaction"
        }

        signed_tx = wallet.sign_transaction(tx_data)

        assert "tx" in signed_tx
        assert "signature" in signed_tx
        assert "mode" in signed_tx
        assert signed_tx["tx"] == tx_data
        assert "signature" in signed_tx["signature"]
        assert "pub_key" in signed_tx["signature"]


class TestAkashWalletCustomDerivationPaths:
    """Test custom derivation path functionality."""

    def test_default_derivation_path(self):
        """Test default derivation path is used when none specified."""
        mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"

        wallet_default = AkashWallet.from_mnemonic(mnemonic)
        wallet_explicit = AkashWallet.from_mnemonic(mnemonic, derivation_path="m/44'/118'/0'/0/0")

        assert wallet_default.address == wallet_explicit.address

    def test_custom_derivation_path_different_addresses(self):
        """Test custom derivation paths generate different addresses."""
        mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"

        wallet0 = AkashWallet.from_mnemonic(mnemonic, derivation_path="m/44'/118'/0'/0/0")
        wallet1 = AkashWallet.from_mnemonic(mnemonic, derivation_path="m/44'/118'/0'/0/1")
        wallet2 = AkashWallet.from_mnemonic(mnemonic, derivation_path="m/44'/118'/0'/0/2")

        addresses = {wallet0.address, wallet1.address, wallet2.address}
        assert len(addresses) == 3

    def test_custom_derivation_path_account_level(self):
        """Test custom derivation paths at account level."""
        mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"

        wallet_account0 = AkashWallet.from_mnemonic(mnemonic, derivation_path="m/44'/118'/0'/0/0")
        wallet_account1 = AkashWallet.from_mnemonic(mnemonic, derivation_path="m/44'/118'/1'/0/0")

        assert wallet_account0.address != wallet_account1.address

    def test_custom_derivation_path_consistency(self):
        """Test custom derivation paths are consistent across calls."""
        mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
        custom_path = "m/44'/118'/0'/0/5"

        wallet1 = AkashWallet.from_mnemonic(mnemonic, derivation_path=custom_path)
        wallet2 = AkashWallet.from_mnemonic(mnemonic, derivation_path=custom_path)

        assert wallet1.address == wallet2.address

    def test_parse_derivation_path_standard_formats(self):
        """Test parsing of standard derivation path formats."""
        test_cases = [
            ("m/44'/118'/0'/0/0", [44 + 0x80000000, 118 + 0x80000000, 0x80000000, 0, 0]),
            ("m/44'/118'/0'/0/1", [44 + 0x80000000, 118 + 0x80000000, 0x80000000, 0, 1]),
            ("m/44'/118'/1'/0/0", [44 + 0x80000000, 118 + 0x80000000, 1 + 0x80000000, 0, 0]),
            ("m/44'/60'/0'/0/0", [44 + 0x80000000, 60 + 0x80000000, 0x80000000, 0, 0]),
        ]

        for path_str, expected in test_cases:
            result = AkashWallet._parse_derivation_path(path_str)
            assert result == expected, f"Failed for path {path_str}"

    def test_parse_derivation_path_double_quotes(self):
        """Test parsing derivation paths with double quotes for hardened derivation."""
        test_cases = [
            ('m/44"/118"/0"/0/0', [44 + 0x80000000, 118 + 0x80000000, 0x80000000, 0, 0]),
            ('m/44"/118"/0"/0/1', [44 + 0x80000000, 118 + 0x80000000, 0x80000000, 0, 1]),
        ]

        for path_str, expected in test_cases:
            result = AkashWallet._parse_derivation_path(path_str)
            assert result == expected, f"Failed for path {path_str}"

    def test_parse_derivation_path_mixed_quotes(self):
        """Test parsing derivation paths with mixed quote styles."""
        path_with_mixed = 'm/44\'/118"/0\'/0/0'
        expected = [44 + 0x80000000, 118 + 0x80000000, 0x80000000, 0, 0]

        result = AkashWallet._parse_derivation_path(path_with_mixed)
        assert result == expected

    def test_parse_derivation_path_invalid_format(self):
        """Test parsing invalid derivation path formats."""
        invalid_paths = [
            ("44'/118'/0'/0/0", "Invalid derivation path"),
            ("", "Invalid derivation path"),
            ("invalid/path", "Invalid derivation path"),
            ("m/44'/invalid'/0'/0/0", "Invalid path component"),
            ("m/44'/118a'/0'/0/0", "Invalid path component"),
        ]

        for invalid_path, expected_error in invalid_paths:
            with pytest.raises(ValueError, match=expected_error):
                AkashWallet._parse_derivation_path(invalid_path)

    def test_parse_derivation_path_empty_valid(self):
        """Test parsing edge cases that are technically valid."""
        result = AkashWallet._parse_derivation_path("m/")
        assert result == []

    def test_parse_derivation_path_valid_non_hardened(self):
        """Test parsing valid non-hardened derivation paths."""
        valid_path = "m/44/118/0/0/0"
        result = AkashWallet._parse_derivation_path(valid_path)
        expected = [44, 118, 0, 0, 0]
        assert result == expected

    def test_parse_derivation_path_short_valid(self):
        """Test parsing shorter valid derivation paths."""
        test_cases = [
            ("m/44'", [44 + 0x80000000]),
            ("m/44'/118'", [44 + 0x80000000, 118 + 0x80000000]),
        ]

        for path_str, expected in test_cases:
            result = AkashWallet._parse_derivation_path(path_str)
            assert result == expected

    def test_different_coin_types(self):
        """Test derivation paths with different coin types."""
        mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"

        wallet_cosmos = AkashWallet.from_mnemonic(mnemonic, derivation_path="m/44'/118'/0'/0/0")
        wallet_type60 = AkashWallet.from_mnemonic(mnemonic, derivation_path="m/44'/60'/0'/0/0")
        wallet_type0 = AkashWallet.from_mnemonic(mnemonic, derivation_path="m/44'/0'/0'/0/0")

        addresses = {wallet_cosmos.address, wallet_type60.address, wallet_type0.address}
        assert len(addresses) == 3

    def test_derivation_path_with_passphrase(self):
        """Test custom derivation paths work with passphrases."""
        mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
        passphrase = "test_passphrase"

        wallet1 = AkashWallet.from_mnemonic(mnemonic, passphrase, "m/44'/118'/0'/0/0")
        wallet2 = AkashWallet.from_mnemonic(mnemonic, passphrase, "m/44'/118'/0'/0/1")

        assert wallet1.address != wallet2.address

    def test_wallet_properties_with_custom_path(self):
        """Test wallet properties are preserved with custom derivation paths."""
        mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
        custom_path = "m/44'/118'/0'/0/3"

        wallet = AkashWallet.from_mnemonic(mnemonic, derivation_path=custom_path)

        assert wallet.address.startswith('akash1')
        assert wallet.mnemonic == mnemonic
        assert wallet.public_key is not None
        assert len(wallet.public_key_bytes) == 33
        assert isinstance(wallet.address, str)

    def test_signing_with_custom_derivation_path(self):
        """Test message signing works with custom derivation paths."""
        mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
        custom_path = "m/44'/118'/0'/0/7"

        wallet = AkashWallet.from_mnemonic(mnemonic, derivation_path=custom_path)
        message = "Test message with custom derivation path"

        signature = wallet.sign_message(message)
        assert isinstance(signature, str)
        assert len(signature) > 0

        is_valid = wallet.verify_signature(message, signature)
        assert is_valid is True


class TestAkashWalletBIP32Derivation:
    """Test BIP32 hierarchical key derivation."""

    def test_derive_master_key(self):
        """Test master key derivation from seed."""
        test_seed = b"test seed for master key derivation" + b"\x00" * 32

        master_key, master_chain_code = AkashWallet._derive_master_key(test_seed)

        assert len(master_key) == 32
        assert len(master_chain_code) == 32
        assert isinstance(master_key, bytes)
        assert isinstance(master_chain_code, bytes)

    def test_derive_child_key_hardened(self):
        """Test hardened child key derivation."""
        parent_key = b'\x01' * 32
        parent_chain_code = b'\x02' * 32
        path = [0x80000000]

        child_key = AkashWallet._derive_child_key(parent_key, parent_chain_code, path)

        assert len(child_key) == 32
        assert child_key != parent_key

    def test_derive_child_key_non_hardened(self):
        """Test non-hardened child key derivation."""
        parent_key = b'\x01' * 32
        parent_chain_code = b'\x02' * 32
        path = [0]

        child_key = AkashWallet._derive_child_key(parent_key, parent_chain_code, path)

        assert len(child_key) == 32
        assert child_key != parent_key

    def test_derive_child_key_full_path(self):
        """Test full BIP44 path derivation."""
        parent_key = b'\x01' * 32
        parent_chain_code = b'\x02' * 32
        path = AkashWallet.COSMOS_DERIVATION_PATH

        child_key = AkashWallet._derive_child_key(parent_key, parent_chain_code, path)

        assert len(child_key) == 32
        assert child_key != parent_key

    def test_cosmos_derivation_path_structure(self):
        """Test COSMOS_DERIVATION_PATH has correct structure."""
        path = AkashWallet.COSMOS_DERIVATION_PATH

        assert len(path) == 5
        assert path[0] == 44 + 0x80000000
        assert path[1] == 118 + 0x80000000
        assert path[2] == 0x80000000
        assert path[3] == 0
        assert path[4] == 0

    def test_derive_private_key_from_mnemonic_consistency(self):
        """Test private key derivation consistency."""
        mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"

        key1 = AkashWallet._derive_private_key_from_mnemonic(mnemonic)
        key2 = AkashWallet._derive_private_key_from_mnemonic(mnemonic)

        assert key1.to_string() == key2.to_string()

    def test_derive_private_key_from_mnemonic_different_passphrases(self):
        """Test private key derivation with different passphrases."""
        mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"

        key1 = AkashWallet._derive_private_key_from_mnemonic(mnemonic, "")
        key2 = AkashWallet._derive_private_key_from_mnemonic(mnemonic, "passphrase")

        assert key1.to_string() != key2.to_string()


class TestAkashWalletProperties:
    """Test wallet property accessors."""

    def test_wallet_properties(self):
        """Test wallet property accessors."""
        mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
        wallet = AkashWallet.from_mnemonic(mnemonic)

        assert isinstance(wallet.address, str)
        assert wallet.address.startswith('akash1')
        assert wallet.mnemonic == mnemonic
        assert wallet.public_key is not None
        assert isinstance(wallet.public_key_bytes, bytes)
        assert len(wallet.public_key_bytes) == 33

    def test_wallet_properties_no_mnemonic(self):
        """Test wallet properties when created without mnemonic."""
        private_key_bytes = b'\x01' * 32
        wallet = AkashWallet.from_private_key(private_key_bytes)

        assert wallet.address is not None
        assert wallet.mnemonic is None
        assert wallet.public_key is not None
        assert wallet.public_key_bytes is not None


class TestAkashWalletStringRepresentation:
    """Test wallet string representations."""

    def test_wallet_str(self):
        """Test wallet string representation."""
        wallet = AkashWallet.generate()

        str_repr = str(wallet)
        assert "AkashWallet" in str_repr
        assert wallet.address in str_repr

    def test_wallet_repr(self):
        """Test wallet detailed representation."""
        mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
        wallet = AkashWallet.from_mnemonic(mnemonic)

        repr_str = repr(wallet)
        assert "AkashWallet" in repr_str
        assert wallet.address in repr_str
        assert "has_mnemonic=True" in repr_str

    def test_wallet_repr_no_mnemonic(self):
        """Test wallet representation without mnemonic."""
        private_key_bytes = b'\x01' * 32
        wallet = AkashWallet.from_private_key(private_key_bytes)

        repr_str = repr(wallet)
        assert "has_mnemonic=False" in repr_str


class TestAkashWalletErrorHandling:
    """Test wallet error handling and edge cases."""

    def test_sign_message_error_handling(self):
        """Test message signing error handling."""
        wallet = AkashWallet.generate()

        with patch.object(wallet, '_private_key') as mock_key:
            mock_key.sign.side_effect = Exception("Signing failed")

            with pytest.raises(Exception, match="Signing failed"):
                wallet.sign_message("test message")

    def test_verify_signature_error_handling(self):
        """Test signature verification error handling."""
        wallet = AkashWallet.generate()

        result = wallet.verify_signature("message", "invalid_hex")
        assert result is False

    def test_sign_raw_error_handling(self):
        """Test raw signing error handling."""
        wallet = AkashWallet.generate()

        with patch.object(wallet, '_private_key') as mock_key:
            mock_key.sign_deterministic.side_effect = Exception("Sign failed")

            with pytest.raises(Exception, match="Sign failed"):
                wallet.sign_raw(b"test data")

    def test_serialize_tx_for_signing(self):
        """Test transaction serialization for signing."""
        wallet = AkashWallet.generate()

        tx_data = {
            "chain_id": "test-chain",
            "account_number": "123",
            "sequence": "1",
            "fee": {"amount": [], "gas": "200000"},
            "msgs": [],
            "memo": "test"
        }

        result = wallet._serialize_tx_for_signing(tx_data)

        assert isinstance(result, bytes)
        import json
        json.loads(result.decode())

    def test_derive_child_key_invalid_key(self):
        """Test child key derivation with edge case."""
        parent_key = b'\x00' * 32
        parent_chain_code = b'\x01' * 32
        path = [0x80000000]

        try:
            child_key = AkashWallet._derive_child_key(parent_key, parent_chain_code, path)
            assert len(child_key) == 32
        except ValueError:
            pass


class TestAkashWalletImports:
    """Test that ALL wallet module imports actually work (not mocked)."""

    def test_all_module_imports(self):
        """Verify ALL wallet dependencies import successfully."""
        # Standard library imports
        import hashlib
        import hmac
        import logging
        import struct
        import json
        from typing import Dict, List, Optional, Tuple, Any

        # Third-party cryptographic libraries
        import bech32
        from ecdsa import SigningKey, VerifyingKey, SECP256k1
        from ecdsa.util import sigencode_string_canonize
        from mnemonic import Mnemonic

        # Internal imports
        from akash.modules.auth.utils import validate_address

        # Conditional import (RIPEMD160) - test both methods
        try:
            from Crypto.Hash import RIPEMD160
            # Test it works
            test_hash = RIPEMD160.new(b"test")
            assert test_hash is not None
        except ImportError:
            # Fallback to hashlib
            test_hash = hashlib.new("ripemd160", b"test")
            assert test_hash is not None

        # All imports succeeded if we reach here
        assert True

    def test_cryptographic_primitives(self):
        """Verify cryptographic primitives work correctly."""
        from ecdsa import SigningKey, VerifyingKey, SECP256k1
        from ecdsa.util import sigencode_string_canonize
        import hashlib

        # Test SECP256k1 key generation
        test_private_key = b'\x01' * 32
        signing_key = SigningKey.from_string(test_private_key, curve=SECP256k1)
        assert signing_key is not None

        # Test verifying key derivation
        verifying_key = signing_key.verifying_key
        assert verifying_key is not None
        assert isinstance(verifying_key, VerifyingKey)

        # Test compressed public key format
        compressed_pubkey = verifying_key.to_string("compressed")
        assert len(compressed_pubkey) == 33
        assert compressed_pubkey[0] in [0x02, 0x03]

        # Test signing with canonical encoding
        test_data = b"test message"
        test_hash = hashlib.sha256(test_data).digest()
        signature = signing_key.sign_deterministic(
            test_hash,
            hashfunc=hashlib.sha256,
            sigencode=sigencode_string_canonize
        )
        assert signature is not None
        assert isinstance(signature, bytes)

    def test_bip39_mnemonic_functionality(self):
        """Verify BIP39 mnemonic library works correctly."""
        from mnemonic import Mnemonic

        # Test mnemonic generation
        mnemo = Mnemonic("english")
        mnemonic_12 = mnemo.generate(strength=128)
        assert len(mnemonic_12.split()) == 12

        # Test mnemonic validation
        valid_mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
        assert mnemo.check(valid_mnemonic) is True

        invalid_mnemonic = "invalid mnemonic phrase"
        assert mnemo.check(invalid_mnemonic) is False

        # Test seed generation
        seed = mnemo.to_seed(valid_mnemonic, "")
        assert isinstance(seed, bytes)
        assert len(seed) == 64

    def test_bech32_encoding(self):
        """Verify bech32 library works correctly."""
        import bech32

        # Test bech32 encoding
        test_data = b'\x00' * 20
        converted = bech32.convertbits(test_data, 8, 5)
        assert converted is not None

        encoded = bech32.bech32_encode("akash", converted)
        assert encoded.startswith("akash1")

        # Test decoding
        hrp, decoded = bech32.bech32_decode(encoded)
        assert hrp == "akash"
        assert decoded is not None

    def test_address_validation_import(self):
        """Verify auth.utils.validate_address import works."""
        from akash.modules.auth.utils import validate_address

        # Test with valid address
        valid_address = "akash1qnnhhgzxj24f2kld5yhy4v4h4s9r295ak5gjw4"
        assert validate_address(valid_address) is True

        # Test with invalid address
        invalid_address = "invalid_address"
        assert validate_address(invalid_address) is False


class TestAkashWalletCryptographicProperties:
    """Test cryptographic properties and security."""

    def test_private_key_security(self):
        """Test private key is kept secure."""
        wallet = AkashWallet.generate()

        assert hasattr(wallet, '_private_key')
        assert "_private_key" not in str(wallet)
        assert "_private_key" not in repr(wallet)

    def test_public_key_derivation_correctness(self):
        """Test public key is correctly derived from private key."""
        wallet = AkashWallet.generate()

        expected_public_key = wallet._private_key.verifying_key
        assert wallet.public_key == expected_public_key

    def test_signature_generation_works(self):
        """Test signature generation produces valid output."""
        wallet = AkashWallet.generate()
        message = "test message for signing"

        signature = wallet.sign_message(message)

        assert isinstance(signature, str)
        assert len(signature) > 0
        bytes.fromhex(signature)

        assert wallet.verify_signature(message, signature) is True

    def test_different_wallets_different_signatures(self):
        """Test different wallets produce different signatures."""
        wallet1 = AkashWallet.generate()
        wallet2 = AkashWallet.generate()
        message = "same message for both wallets"

        sig1 = wallet1.sign_message(message)
        sig2 = wallet2.sign_message(message)

        assert sig1 != sig2


if __name__ == '__main__':
    print("✅ Running AkashWallet unit tests")
    print("=" * 50)
    print()
    print("Testing BIP39/BIP44 key derivation, address generation, mnemonic handling,")
    print("transaction signing, message verification, and cryptographic operations.")
    print()
    print("These tests use test vectors and mocking to isolate wallet functionality.")
    print()

    pytest.main([__file__, '-v'])
