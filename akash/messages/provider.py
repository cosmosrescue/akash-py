"""
Provider message conversions.

Converts dictionary representations to protobuf messages for provider operations.
"""


def convert_msg_create_provider(msg_dict, any_msg):
    """Convert MsgCreateProvider dictionary to protobuf."""
    # v1beta4: Msg types moved to msg_pb2
    from akash.proto.akash.provider.v1beta4.msg_pb2 import MsgCreateProvider

    pb_msg = MsgCreateProvider()
    pb_msg.owner = msg_dict.get("owner", "")
    pb_msg.host_uri = msg_dict.get("host_uri", "")

    for attr in msg_dict.get("attributes", []):
        attr_pb = pb_msg.attributes.add()
        attr_pb.key = attr.get("key", "")
        attr_pb.value = attr.get("value", "")

    info_data = msg_dict.get("info", {})
    if info_data:
        pb_msg.info.email = info_data.get("email", "")
        pb_msg.info.website = info_data.get("website", "")

    any_msg.Pack(pb_msg, type_url_prefix="")
    return any_msg


def convert_msg_update_provider(msg_dict, any_msg):
    """Convert MsgUpdateProvider dictionary to protobuf."""
    # v1beta4: Msg types moved to msg_pb2
    from akash.proto.akash.provider.v1beta4.msg_pb2 import MsgUpdateProvider

    pb_msg = MsgUpdateProvider()
    pb_msg.owner = msg_dict.get("owner", "")
    pb_msg.host_uri = msg_dict.get("host_uri", "")

    for attr in msg_dict.get("attributes", []):
        attr_pb = pb_msg.attributes.add()
        attr_pb.key = attr.get("key", "")
        attr_pb.value = attr.get("value", "")

    info_data = msg_dict.get("info", {})
    if info_data:
        pb_msg.info.email = info_data.get("email", "")
        pb_msg.info.website = info_data.get("website", "")

    any_msg.Pack(pb_msg, type_url_prefix="")
    return any_msg
