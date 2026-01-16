"""
Transaction broadcasting implementation for Akash network.
"""

import base64
import hashlib
import json
import logging
import time

logger = logging.getLogger(__name__)


class BroadcastResult:
    def __init__(self, tx_hash, code, raw_log, success, events=None):
        self.tx_hash = tx_hash
        self.code = code
        self.raw_log = raw_log
        self.success = success
        self.events = events or []

    def get_event_attribute(self, event_type, attribute_key):
        """
        Extract attribute value from transaction events.

        Args:
            event_type: Event type to search for (e.g. 'akash.v1')
            attribute_key: Attribute key to find (e.g. 'dseq')

        Returns:
            str: Attribute value or None if not found
        """
        try:
            import json

            if self.raw_log:
                log_data = json.loads(self.raw_log)
                if isinstance(log_data, list) and log_data:
                    events = log_data[0].get("events", [])

                    for event in events:
                        if event.get("type") == event_type:
                            attributes = event.get("attributes", [])
                            for attr in attributes:
                                if attr.get("key") == attribute_key:
                                    return attr.get("value")

            if self.events:
                for event in self.events:
                    if event.get("type") == event_type:
                        attributes = event.get("attributes", [])
                        for attr in attributes:
                            if attr.get("key") == attribute_key:
                                return attr.get("value")

            return None
        except Exception:
            return None

    def get_dseq(self):
        """
        Extract deployment sequence number from deployment creation transaction.

        Returns:
            int: DSEQ or None if not found
        """
        dseq_str = self.get_event_attribute("akash.v1", "dseq")
        if dseq_str:
            try:
                return int(dseq_str)
            except ValueError:
                pass
        return None


    def get_provider_address(self):
        """
        Extract provider address from provider creation transaction.

        Returns:
            str: Provider address or None if not found
        """
        return self.get_event_attribute("akash.v1", "owner")

    def get_bid_info(self):
        """
        Extract bid information from bid creation transaction.

        Returns:
            dict: Bid info with provider, dseq, gseq, oseq or None if not found
        """
        try:
            provider = self.get_event_attribute("akash.v1", "provider")
            dseq = self.get_event_attribute("akash.v1", "dseq")
            gseq = self.get_event_attribute("akash.v1", "gseq")
            oseq = self.get_event_attribute("akash.v1", "oseq")

            if provider and dseq and gseq and oseq:
                return {
                    "provider": provider,
                    "dseq": int(dseq),
                    "gseq": int(gseq),
                    "oseq": int(oseq),
                }
        except ValueError:
            pass
        return None

    def get_order_info(self):
        """
        Extract order information from deployment creation transaction.

        Returns:
            dict: Order info with owner, dseq, gseq, oseq or None if not found
        """
        try:
            owner = self.get_event_attribute("akash.v1", "owner")
            dseq = self.get_event_attribute("akash.v1", "dseq")
            gseq = self.get_event_attribute("akash.v1", "gseq")
            oseq = self.get_event_attribute("akash.v1", "oseq")

            if all([owner, dseq, gseq, oseq]):
                return {
                    "owner": owner,
                    "dseq": int(dseq),
                    "gseq": int(gseq),
                    "oseq": int(oseq),
                }
        except (ValueError, TypeError):
            pass
        return None


type_mapping = {
    "MsgSend": "/cosmos.bank.v1beta1.MsgSend",
    "MsgDelegate": "/cosmos.staking.v1beta1.MsgDelegate",
    "MsgUndelegate": "/cosmos.staking.v1beta1.MsgUndelegate",
    "MsgBeginRedelegate": "/cosmos.staking.v1beta1.MsgBeginRedelegate",
    "MsgCreateValidator": "/cosmos.staking.v1beta1.MsgCreateValidator",
    "MsgEditValidator": "/cosmos.staking.v1beta1.MsgEditValidator",
    "MsgWithdrawDelegatorReward": "/cosmos.distribution.v1beta1.MsgWithdrawDelegatorReward",
    "MsgSetWithdrawAddress": "/cosmos.distribution.v1beta1.MsgSetWithdrawAddress",
    "MsgSubmitProposal": "/cosmos.gov.v1beta1.MsgSubmitProposal",
    "MsgDeposit": "/cosmos.gov.v1beta1.MsgDeposit",
    "MsgVote": "/cosmos.gov.v1beta1.MsgVote",
    "MsgGrant": "/cosmos.authz.v1beta1.MsgGrant",
    "MsgRevoke": "/cosmos.authz.v1beta1.MsgRevoke",
    "MsgExec": "/cosmos.authz.v1beta1.MsgExec",
    "MsgGrantAllowance": "/cosmos.feegrant.v1beta1.MsgGrantAllowance",
    "MsgRevokeAllowance": "/cosmos.feegrant.v1beta1.MsgRevokeAllowance",
    "BasicAllowance": "/cosmos.feegrant.v1beta1.BasicAllowance",
    "PeriodicAllowance": "/cosmos.feegrant.v1beta1.PeriodicAllowance",
}

_MESSAGE_CONVERTERS = {}


def register_message_converter(type_url, converter_func):
    """Register a message converter function for a specific type URL."""
    _MESSAGE_CONVERTERS[type_url] = converter_func


def _initialize_message_converters():
    """Initialize all message converters from the messages/ modules."""
    try:
        from akash.messages.bank import convert_msg_send

        register_message_converter("/cosmos.bank.v1beta1.MsgSend", convert_msg_send)
    except ImportError:
        pass

    try:
        from akash.messages.staking import (
            convert_msg_delegate,
            convert_msg_undelegate,
            convert_msg_begin_redelegate,
            convert_msg_create_validator,
            convert_msg_edit_validator,
        )

        register_message_converter(
            "/cosmos.staking.v1beta1.MsgDelegate", convert_msg_delegate
        )
        register_message_converter(
            "/cosmos.staking.v1beta1.MsgUndelegate", convert_msg_undelegate
        )
        register_message_converter(
            "/cosmos.staking.v1beta1.MsgBeginRedelegate", convert_msg_begin_redelegate
        )
        register_message_converter(
            "/cosmos.staking.v1beta1.MsgCreateValidator", convert_msg_create_validator
        )
        register_message_converter(
            "/cosmos.staking.v1beta1.MsgEditValidator", convert_msg_edit_validator
        )
    except ImportError:
        pass

    try:
        from akash.messages.distribution import (
            convert_msg_withdraw_delegator_reward,
            convert_msg_set_withdraw_address,
        )

        register_message_converter(
            "/cosmos.distribution.v1beta1.MsgWithdrawDelegatorReward",
            convert_msg_withdraw_delegator_reward,
        )
        register_message_converter(
            "/cosmos.distribution.v1beta1.MsgSetWithdrawAddress",
            convert_msg_set_withdraw_address,
        )
    except ImportError:
        pass

    try:
        from akash.messages.evidence import convert_msg_submit_evidence

        register_message_converter(
            "/cosmos.evidence.v1beta1.MsgSubmitEvidence", convert_msg_submit_evidence
        )
    except ImportError:
        pass

    try:
        from akash.messages.governance import (
            convert_msg_submit_proposal,
            convert_msg_deposit,
            convert_msg_vote,
        )

        register_message_converter(
            "/cosmos.gov.v1beta1.MsgSubmitProposal", convert_msg_submit_proposal
        )
        register_message_converter(
            "/cosmos.gov.v1beta1.MsgDeposit", convert_msg_deposit
        )
        register_message_converter("/cosmos.gov.v1beta1.MsgVote", convert_msg_vote)
    except ImportError:
        pass

    try:
        from akash.messages.authz import (
            convert_msg_grant,
            convert_msg_revoke,
            convert_msg_exec,
        )

        register_message_converter("/cosmos.authz.v1beta1.MsgGrant", convert_msg_grant)
        register_message_converter(
            "/cosmos.authz.v1beta1.MsgRevoke", convert_msg_revoke
        )
        register_message_converter("/cosmos.authz.v1beta1.MsgExec", convert_msg_exec)
    except ImportError:
        pass

    try:
        from akash.messages.feegrant import (
            convert_msg_grant_allowance,
            convert_msg_revoke_allowance,
            convert_basic_allowance,
            convert_periodic_allowance,
        )

        register_message_converter(
            "/cosmos.feegrant.v1beta1.MsgGrantAllowance", convert_msg_grant_allowance
        )
        register_message_converter(
            "/cosmos.feegrant.v1beta1.MsgRevokeAllowance", convert_msg_revoke_allowance
        )
        register_message_converter(
            "/cosmos.feegrant.v1beta1.BasicAllowance", convert_basic_allowance
        )
        register_message_converter(
            "/cosmos.feegrant.v1beta1.PeriodicAllowance", convert_periodic_allowance
        )
    except ImportError:
        pass

    try:
        from akash.messages.slashing import convert_msg_unjail

        register_message_converter(
            "/cosmos.slashing.v1beta1.MsgUnjail", convert_msg_unjail
        )
    except ImportError:
        pass

    try:
        from akash.messages.market import (
            convert_msg_create_bid,
            convert_msg_close_bid,
            convert_msg_create_lease,
            convert_msg_close_lease,
            convert_msg_withdraw_lease,
        )

        register_message_converter(
            "/akash.market.v1beta5.MsgCreateBid", convert_msg_create_bid
        )
        register_message_converter(
            "/akash.market.v1beta5.MsgCloseBid", convert_msg_close_bid
        )
        register_message_converter(
            "/akash.market.v1beta5.MsgCreateLease", convert_msg_create_lease
        )
        register_message_converter(
            "/akash.market.v1beta5.MsgCloseLease", convert_msg_close_lease
        )
        register_message_converter(
            "/akash.market.v1beta5.MsgWithdrawLease", convert_msg_withdraw_lease
        )
    except ImportError:
        pass

    try:
        from akash.messages.provider import (
            convert_msg_create_provider,
            convert_msg_update_provider,
        )

        register_message_converter(
            "/akash.provider.v1beta4.MsgCreateProvider", convert_msg_create_provider
        )
        register_message_converter(
            "/akash.provider.v1beta4.MsgUpdateProvider", convert_msg_update_provider
        )
    except ImportError:
        pass

    try:
        from akash.messages.audit import (
            convert_msg_sign_provider_attributes,
            convert_msg_delete_provider_attributes,
        )

        register_message_converter(
            "/akash.audit.v1.MsgSignProviderAttributes",
            convert_msg_sign_provider_attributes,
        )
        register_message_converter(
            "/akash.audit.v1.MsgDeleteProviderAttributes",
            convert_msg_delete_provider_attributes,
        )
    except ImportError:
        pass
    try:
        from akash.messages.cert import (
            encode_msg_create_certificate,
            encode_msg_revoke_certificate,
        )

        register_message_converter(
            "/akash.cert.v1.MsgCreateCertificate", encode_msg_create_certificate
        )
        register_message_converter(
            "/akash.cert.v1.MsgRevokeCertificate", encode_msg_revoke_certificate
        )
    except ImportError:
        pass

    try:
        from akash.messages.deployment import (
            convert_msg_create_deployment,
            convert_msg_update_deployment,
            convert_msg_close_deployment,
            convert_msg_deposit_deployment,
            convert_msg_close_group,
            convert_msg_pause_group,
            convert_msg_start_group,
        )

        register_message_converter(
            "/akash.deployment.v1beta4.MsgCreateDeployment",
            convert_msg_create_deployment,
        )
        register_message_converter(
            "/akash.deployment.v1beta4.MsgUpdateDeployment",
            convert_msg_update_deployment,
        )
        register_message_converter(
            "/akash.deployment.v1beta4.MsgCloseDeployment", convert_msg_close_deployment
        )
        register_message_converter(
            "/akash.deployment.v1beta4.MsgDepositDeployment",
            convert_msg_deposit_deployment,
        )
        register_message_converter(
            "/akash.deployment.v1beta4.MsgCloseGroup", convert_msg_close_group
        )
        register_message_converter(
            "/akash.deployment.v1beta4.MsgPauseGroup", convert_msg_pause_group
        )
        register_message_converter(
            "/akash.deployment.v1beta4.MsgStartGroup", convert_msg_start_group
        )
    except ImportError:
        pass

    try:
        from akash.messages.ibc import (
            convert_msg_transfer,
            convert_msg_create_client,
            convert_msg_update_client,
        )

        register_message_converter(
            "/ibc.applications.transfer.v1.MsgTransfer", convert_msg_transfer
        )
        register_message_converter(
            "/ibc.core.client.v1.MsgCreateClient", convert_msg_create_client
        )
        register_message_converter(
            "/ibc.core.client.v1.MsgUpdateClient", convert_msg_update_client
        )
    except ImportError:
        pass


def _sign_bytes(wallet, sign_bytes: bytes) -> str:
    """Sign the transaction bytes."""
    try:
        from ecdsa.util import sigencode_string_canonize
        import hashlib

        signature = wallet._private_key.sign_deterministic(
            sign_bytes, hashfunc=hashlib.sha256, sigencode=sigencode_string_canonize
        )

        return base64.b64encode(signature).decode()

    except ImportError:
        sign_hash = hashlib.sha256(sign_bytes).digest()
        signature = wallet._private_key.sign(sign_hash)
        return base64.b64encode(signature).decode()


def _convert_dict_to_any(msg_dict):
    """
    Convert dictionary message to protobuf Any using the message converter registry.
    """
    try:
        from google.protobuf.any_pb2 import Any

        if not _MESSAGE_CONVERTERS:
            _initialize_message_converters()

        type_key = msg_dict.get("@type") or msg_dict.get("type")
        if not type_key:
            raise ValueError("Message missing @type or type field")

        logger.debug(f"_convert_dict_to_any: Input type_key={type_key}")

        type_url = type_key if type_key.startswith("/") else type_mapping.get(type_key)
        if not type_url:
            raise ValueError(f"Unknown message type: {type_key}")

        logger.debug(f"_convert_dict_to_any: Resolved type_url={type_url}")

        converter_func = _MESSAGE_CONVERTERS.get(type_url)
        if converter_func:
            any_msg = Any()
            result = converter_func(msg_dict, any_msg)
            logger.debug(
                f"_convert_dict_to_any: Output any_msg.type_url={result.type_url}"
            )
            return result
        else:
            raise ValueError(f"Unsupported message type: {type_url}")

    except Exception as e:
        logger.error(f"_convert_dict_to_any failed: {str(e)}")
        raise


def broadcast_transaction_rpc(
    client,
    wallet,
    messages,
    memo="",
    fee_amount=None,
    gas_limit=None,
    gas_adjustment=1.2,
    use_simulation=True,
    wait_for_confirmation=True,
    confirmation_timeout=30,
):
    """
    Broadcast a transaction via RPC.

    Args:
        client: AkashClient instance
        wallet: AkashWallet instance
        messages: List of message dictionaries or Any messages
        memo: Transaction memo
        fee_amount: Fee amount in uakt
        gas_limit: Gas limit override
        gas_adjustment: Multiplier for simulated gas
        use_simulation: Enable gas simulation
        wait_for_confirmation: Wait for transaction confirmation
        confirmation_timeout: Timeout for confirmation in seconds

    Returns:
        BroadcastResult with transaction details
    """
    try:
        account_info = client.get_account_info(wallet.address)
        sequence = account_info.get("sequence", 0)
        account_number = account_info.get("account_number", 0)

        default_gas = 200000
        final_fee_amount = fee_amount or "5000"
        if gas_limit:
            final_gas_limit = gas_limit
        elif use_simulation:
            final_gas_limit = int(
                simulate_transaction(client, wallet, messages, memo, final_fee_amount)
                * gas_adjustment
            )
        else:
            final_gas_limit = default_gas

        if fee_amount is None and final_gas_limit != default_gas:
            fee_ratio = min(final_gas_limit / default_gas, 2.0)
            final_fee_amount = str(int(int(final_fee_amount) * fee_ratio))

        tx = {
            "body": {
                "messages": messages,  # Pass messages directly, _encode_body will handle conversion
                "memo": memo,
                "timeout_height": "0",
                "extension_options": [],
                "non_critical_extension_options": [],
            },
            "auth_info": {
                "signer_infos": [
                    {
                        "public_key": {
                            "@type": "/cosmos.crypto.secp256k1.PubKey",
                            "key": base64.b64encode(wallet.public_key_bytes).decode(),
                        },
                        "mode_info": {"single": {"mode": 1}},
                        "sequence": str(sequence),
                    }
                ],
                "fee": {
                    "amount": [{"denom": "uakt", "amount": final_fee_amount}],
                    "gas_limit": str(final_gas_limit),
                    "payer": "",
                    "granter": "",
                },
            },
            "signatures": [],
        }

        from akash.proto.cosmos.tx.v1beta1.tx_pb2 import SignDoc

        body_bytes_for_signing = encode_body(tx["body"])
        auth_info_bytes_for_signing = encode_auth_info(tx["auth_info"])

        sign_doc = {
            "body_bytes": base64.b64encode(body_bytes_for_signing).decode(),
            "auth_info_bytes": base64.b64encode(auth_info_bytes_for_signing).decode(),
            "chain_id": client.chain_id,
            "account_number": str(account_number),
        }

        sign_doc_pb = SignDoc(
            body_bytes=base64.b64decode(sign_doc["body_bytes"]),
            auth_info_bytes=base64.b64decode(sign_doc["auth_info_bytes"]),
            chain_id=sign_doc["chain_id"],
            account_number=int(sign_doc["account_number"]),
        )
        sign_bytes = sign_doc_pb.SerializeToString()

        from ecdsa.util import sigencode_string_canonize

        signature = wallet._private_key.sign_deterministic(
            sign_bytes, hashfunc=hashlib.sha256, sigencode=sigencode_string_canonize
        )
        tx["signatures"] = [base64.b64encode(signature).decode()]

        from akash.proto.cosmos.tx.v1beta1.tx_pb2 import TxRaw

        tx_raw = TxRaw(
            body_bytes=body_bytes_for_signing,
            auth_info_bytes=auth_info_bytes_for_signing,
            signatures=[base64.b64decode(sig) for sig in tx["signatures"]],
        )
        tx_bytes = tx_raw.SerializeToString()
        tx_base64 = base64.b64encode(tx_bytes).decode()

        result = client.rpc_query("broadcast_tx_sync", [tx_base64])

        if not result or "hash" not in result:
            return BroadcastResult(
                "", 1, "Failed to broadcast transaction: missing hash", False
            )

        tx_hash = result["hash"]
        code = result.get("code", 0)
        log = result.get("raw_log", result.get("log", ""))
        success = code == 0

        if success and wait_for_confirmation:
            confirmed_result = wait_for_transaction_confirmation(
                client, tx_hash, confirmation_timeout
            )
            if confirmed_result:
                tx_result = confirmed_result.get("tx_result", {})
                final_code = tx_result.get("code", 0)
                final_log = tx_result.get("raw_log", tx_result.get("log", log))
                return BroadcastResult(tx_hash, final_code, final_log, final_code == 0)
            return BroadcastResult(tx_hash, 1, f"{log} (confirmation timeout)", False)

        return BroadcastResult(tx_hash, code, log, success)

    except Exception as e:
        return BroadcastResult("", 1, str(e), False)


def simulate_transaction(
    client, wallet, messages, memo, fee_amount, default_gas=200000
):
    """
    Simulate a transaction to estimate gas needed.
    """
    try:
        account_info = client.get_account_info(wallet.address)
        sequence = account_info.get("sequence", 0)

        from akash.proto.cosmos.tx.v1beta1.service_pb2 import SimulateRequest

        tx = {
            "body": {"messages": messages, "memo": memo, "timeout_height": "0"},
            "auth_info": {
                "signer_infos": [
                    {
                        "public_key": {
                            "@type": "/cosmos.crypto.secp256k1.PubKey",
                            "key": base64.b64encode(wallet.public_key_bytes).decode(),
                        },
                        "mode_info": {"single": {"mode": 1}},
                        "sequence": str(sequence),
                    }
                ],
                "fee": {
                    "amount": [{"denom": "uakt", "amount": fee_amount}],
                    "gas_limit": "0",
                },
            },
            "signatures": [""],
        }
        from akash.proto.cosmos.tx.v1beta1.tx_pb2 import TxRaw

        tx_raw = TxRaw(
            body_bytes=encode_body(tx["body"]),
            auth_info_bytes=encode_auth_info(tx["auth_info"]),
            signatures=[b""],
        )

        sim_request = SimulateRequest(tx_bytes=tx_raw.SerializeToString())
        result = client.rpc_query(
            "abci_query",
            [
                "/cosmos.tx.v1beta1.Service/Simulate",
                sim_request.SerializeToString().hex().upper(),
                "0",
                False,
            ],
        )

        if result and "response" in result:
            response_code = result["response"].get("code", 0)
            if response_code == 0:
                from akash.proto.cosmos.tx.v1beta1.service_pb2 import SimulateResponse

                sim_response = SimulateResponse()
                sim_response.ParseFromString(
                    base64.b64decode(result["response"]["value"])
                )
                if sim_response.gas_info and sim_response.gas_info.gas_used:
                    return int(sim_response.gas_info.gas_used)
            else:
                error_log = result["response"].get("log", "No error details")
                raise Exception(
                    f"Transaction validation failed - Code {response_code}: {error_log}"
                )

        return default_gas

    except Exception as e:
        logger.error(f"Simulation failed: {str(e)}")
        return default_gas


def encode_body(body):
    """
    Encode transaction body using protobuf, handling message conversion.
    """
    try:
        from akash.proto.cosmos.tx.v1beta1.tx_pb2 import TxBody

        tx_body = TxBody(
            memo=body.get("memo", ""),
            timeout_height=int(body.get("timeout_height", "0")),
        )

        for msg in body.get("messages", []):
            if isinstance(msg, dict):
                tx_body.messages.append(_convert_dict_to_any(msg))
            else:
                tx_body.messages.append(msg)

        return tx_body.SerializeToString()

    except Exception as e:
        logger.error(f"encode_body failed: {str(e)}")
        return json.dumps(body, sort_keys=True).encode("utf-8")


def encode_auth_info(auth_info):
    """
    Encode auth info using protobuf.
    """
    try:
        from akash.proto.cosmos.tx.v1beta1.tx_pb2 import (
            AuthInfo,
            SignerInfo,
            ModeInfo,
            Fee,
        )
        from akash.proto.cosmos.crypto.secp256k1.keys_pb2 import PubKey
        from akash.proto.cosmos.base.v1beta1.coin_pb2 import Coin
        from google.protobuf.any_pb2 import Any

        auth_info_pb = AuthInfo()

        for signer_data in auth_info.get("signer_infos", []):
            signer_info = SignerInfo(
                public_key=Any(
                    type_url="/cosmos.crypto.secp256k1.PubKey",
                    value=PubKey(
                        key=base64.b64decode(signer_data["public_key"]["key"])
                    ).SerializeToString(),
                ),
                mode_info=ModeInfo(single=ModeInfo.Single(mode=1)),
                sequence=int(signer_data.get("sequence", "0")),
            )
            auth_info_pb.signer_infos.append(signer_info)

        fee_data = auth_info.get("fee", {})
        fee = Fee(gas_limit=int(fee_data.get("gas_limit", "200000")))
        for coin_data in fee_data.get("amount", []):
            coin = Coin(denom=coin_data["denom"], amount=coin_data["amount"])
            fee.amount.append(coin)
        auth_info_pb.fee.CopyFrom(fee)

        return auth_info_pb.SerializeToString()

    except Exception as e:
        logger.error(f"encode_auth_info failed: {str(e)}")
        return json.dumps(auth_info, sort_keys=True).encode("utf-8")


def wait_for_transaction_confirmation(client, tx_hash, timeout):
    """
    Wait for transaction confirmation using tx_search.
    """
    try:
        start_time = time.time()
        poll_interval = 1.0

        tx_hash = tx_hash.upper()

        while time.time() - start_time < timeout:
            result = client.rpc_query(
                "tx_search",
                {
                    "query": f"tx.hash='{tx_hash}'",
                    "prove": False,
                    "page": "1",
                    "per_page": "1",
                },
            )

            if result and "txs" in result and result["txs"]:
                tx_data = result["txs"][0]
                return {
                    "height": tx_data.get("height", "0"),
                    "tx_result": tx_data.get("tx_result", {}),
                }

            time.sleep(poll_interval)

        return None
    except Exception as e:
        logger.error(f"wait_for_transaction_confirmation failed: {str(e)}")
        return None
