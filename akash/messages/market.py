"""
Market message conversions.

Converts dictionary representations to protobuf messages for market operations.
"""


def convert_msg_create_bid(msg_dict, any_msg):
    """Convert MsgCreateBid dictionary to protobuf."""
    from akash.proto.akash.market.v1beta5.bidmsg_pb2 import MsgCreateBid
    from akash.proto.akash.market.v1.bid_pb2 import BidID
    from akash.proto.cosmos.base.v1beta1.coin_pb2 import DecCoin, Coin
    from akash.proto.akash.base.deposit.v1.deposit_pb2 import Deposit

    pb_msg = MsgCreateBid()

    # v1beta5: order + provider combined into id (BidID)
    bid_id = BidID()
    # Support both old format (order + provider) and new format (id)
    if "id" in msg_dict:
        id_data = msg_dict["id"]
        bid_id.owner = id_data.get("owner", "")
        bid_id.dseq = int(id_data.get("dseq", 0))
        bid_id.gseq = int(id_data.get("gseq", 0))
        bid_id.oseq = int(id_data.get("oseq", 0))
        bid_id.provider = id_data.get("provider", "")
    else:
        # Old format compatibility
        order = msg_dict.get("order", {})
        bid_id.owner = order.get("owner", "")
        bid_id.dseq = int(order.get("dseq", 0))
        bid_id.gseq = int(order.get("gseq", 0))
        bid_id.oseq = int(order.get("oseq", 0))
        bid_id.provider = msg_dict.get("provider", "")
    pb_msg.id.CopyFrom(bid_id)

    price_data = msg_dict.get("price", {})
    price = DecCoin()
    price.denom = price_data.get("denom", "")
    price.amount = price_data.get("amount", "")
    pb_msg.price.CopyFrom(price)

    # v1beta5: deposit changed from Coin to Deposit structure
    deposit_data = msg_dict.get("deposit", {})
    if deposit_data:
        deposit = Deposit()
        # Handle both old Coin format and new Deposit format
        if "amount" in deposit_data and isinstance(deposit_data["amount"], dict):
            # New format
            deposit_amount = Coin()
            deposit_amount.denom = deposit_data["amount"]["denom"]
            deposit_amount.amount = deposit_data["amount"]["amount"]
            deposit.amount.CopyFrom(deposit_amount)
            if "sources" in deposit_data:
                deposit.sources.extend([int(s) for s in deposit_data["sources"]])
            else:
                deposit.sources.append(1)  # Default to SourceBalance
        else:
            # Old Coin format
            deposit_amount = Coin()
            deposit_amount.denom = deposit_data.get("denom", "")
            deposit_amount.amount = deposit_data.get("amount", "")
            deposit.amount.CopyFrom(deposit_amount)
            deposit.sources.append(1)  # Default to SourceBalance
        pb_msg.deposit.CopyFrom(deposit)

    any_msg.Pack(pb_msg, type_url_prefix="")
    return any_msg


def convert_msg_close_bid(msg_dict, any_msg):
    """Convert MsgCloseBid dictionary to protobuf."""
    from akash.proto.akash.market.v1beta5.bidmsg_pb2 import MsgCloseBid
    from akash.proto.akash.market.v1.bid_pb2 import BidID

    pb_msg = MsgCloseBid()

    id_data = msg_dict.get("id", {})
    bid_id = BidID()
    bid_id.owner = id_data.get("owner", "")
    bid_id.dseq = int(id_data.get("dseq", 0))
    bid_id.gseq = int(id_data.get("gseq", 0))
    bid_id.oseq = int(id_data.get("oseq", 0))
    bid_id.provider = id_data.get("provider", "")
    # v1beta5: field renamed from bid_id to id
    pb_msg.id.CopyFrom(bid_id)

    any_msg.Pack(pb_msg, type_url_prefix="")
    return any_msg


def convert_msg_create_lease(msg_dict, any_msg):
    """Convert MsgCreateLease dictionary to protobuf."""
    from akash.proto.akash.market.v1beta5.leasemsg_pb2 import MsgCreateLease
    from akash.proto.akash.market.v1.bid_pb2 import BidID

    pb_msg = MsgCreateLease()

    bid_id = BidID()
    bid_id.owner = msg_dict.get("owner", "")
    bid_id.dseq = int(msg_dict.get("dseq", 0))
    bid_id.gseq = int(msg_dict.get("gseq", 0))
    bid_id.oseq = int(msg_dict.get("oseq", 0))
    bid_id.provider = msg_dict.get("provider", "")
    # v1beta5: MsgCreateLease still uses bid_id field
    pb_msg.bid_id.CopyFrom(bid_id)

    any_msg.Pack(pb_msg, type_url_prefix="")
    return any_msg


def convert_msg_close_lease(msg_dict, any_msg):
    """Convert MsgCloseLease dictionary to protobuf."""
    from akash.proto.akash.market.v1beta5.leasemsg_pb2 import MsgCloseLease
    from akash.proto.akash.market.v1.lease_pb2 import LeaseID

    pb_msg = MsgCloseLease()

    id_data = msg_dict.get("id", {})
    lease_id = LeaseID()
    lease_id.owner = id_data.get("owner", "")
    lease_id.dseq = int(id_data.get("dseq", 0))
    lease_id.gseq = int(id_data.get("gseq", 0))
    lease_id.oseq = int(id_data.get("oseq", 0))
    lease_id.provider = id_data.get("provider", "")
    # v1beta5: field renamed from lease_id to id
    pb_msg.id.CopyFrom(lease_id)

    any_msg.Pack(pb_msg, type_url_prefix="")
    return any_msg


def convert_msg_withdraw_lease(msg_dict, any_msg):
    """Convert MsgWithdrawLease dictionary to protobuf."""
    from akash.proto.akash.market.v1beta5.leasemsg_pb2 import MsgWithdrawLease
    from akash.proto.akash.market.v1.lease_pb2 import LeaseID

    pb_msg = MsgWithdrawLease()

    id_data = msg_dict.get("id", {})
    lease_id = LeaseID()
    lease_id.owner = id_data.get("owner", "")
    lease_id.dseq = int(id_data.get("dseq", 0))
    lease_id.gseq = int(id_data.get("gseq", 0))
    lease_id.oseq = int(id_data.get("oseq", 0))
    lease_id.provider = id_data.get("provider", "")
    # v1beta5: field is named id (was incorrectly using bid_id before)
    pb_msg.id.CopyFrom(lease_id)

    any_msg.Pack(pb_msg, type_url_prefix="")
    return any_msg
