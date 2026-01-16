"""
Certificate message conversions.

Converts dictionary representations to protobuf messages for certificate operations.
"""

import base64
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


def encode_msg_create_certificate(msg_data: Dict[str, Any], msg_bytes=None) -> bytes:
    """
    Encode MsgCreateCertificate message.

    Args:
        msg_data: Dictionary containing certificate creation data

    Returns:
        bytes: Encoded message
    """
    try:
        from akash.proto.akash.cert.v1.cert_pb2 import MsgCreateCertificate

        msg = MsgCreateCertificate()
        msg.owner = msg_data["owner"]
        msg.cert = base64.b64decode(msg_data["cert"])
        msg.pubkey = base64.b64decode(msg_data["pubkey"])

        from google.protobuf.any_pb2 import Any

        any_msg = Any()
        any_msg.type_url = "/akash.cert.v1.MsgCreateCertificate"
        any_msg.value = msg.SerializeToString()

        logger.debug(
            f"Encoded MsgCreateCertificate: owner={msg.owner}, cert_len={len(msg.cert)}, pubkey_len={len(msg.pubkey)}"
        )
        return any_msg

    except ImportError as e:
        logger.error(f"Missing cert protobuf imports: {e}")
        raise
    except Exception as e:
        logger.error(f"Failed to encode MsgCreateCertificate: {e}")
        raise


def encode_msg_revoke_certificate(msg_data: Dict[str, Any], msg_bytes=None) -> bytes:
    """
    Encode MsgRevokeCertificate message.

    Args:
        msg_data: Dictionary containing certificate revocation data

    Returns:
        bytes: Encoded message
    """
    try:
        from akash.proto.akash.cert.v1.cert_pb2 import (
            MsgRevokeCertificate,
            ID,
        )

        msg = MsgRevokeCertificate()

        # v1: CertificateID renamed to ID
        cert_id = ID()
        cert_id.owner = msg_data["id"]["owner"]
        cert_id.serial = msg_data["id"]["serial"]
        msg.id.CopyFrom(cert_id)

        from google.protobuf.any_pb2 import Any

        any_msg = Any()
        any_msg.type_url = "/akash.cert.v1.MsgRevokeCertificate"
        any_msg.value = msg.SerializeToString()

        logger.debug(
            f"Encoded MsgRevokeCertificate: owner={cert_id.owner}, serial={cert_id.serial}"
        )
        return any_msg

    except ImportError as e:
        logger.error(f"Missing cert protobuf imports: {e}")
        raise
    except Exception as e:
        logger.error(f"Failed to encode MsgRevokeCertificate: {e}")
        raise
