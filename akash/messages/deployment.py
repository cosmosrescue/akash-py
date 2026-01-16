"""
Deployment message conversions.

Converts dictionary representations to protobuf messages for deployment operations.
"""

from akash.proto.cosmos.base.v1beta1.coin_pb2 import Coin


def convert_msg_create_deployment(msg_dict, any_msg):
    """Convert MsgCreateDeployment dictionary to protobuf."""
    from akash.proto.akash.deployment.v1beta4.deploymentmsg_pb2 import (
        MsgCreateDeployment,
    )
    from akash.proto.akash.deployment.v1.deployment_pb2 import DeploymentID
    from akash.proto.akash.deployment.v1beta4.groupspec_pb2 import GroupSpec
    from akash.proto.akash.base.attributes.v1.attribute_pb2 import (
        PlacementRequirements,
        SignedBy,
    )
    from akash.proto.akash.deployment.v1beta4.resourceunit_pb2 import ResourceUnit
    from akash.proto.akash.base.resources.v1beta4.resources_pb2 import Resources
    from akash.proto.akash.base.resources.v1beta4.cpu_pb2 import CPU
    from akash.proto.akash.base.resources.v1beta4.memory_pb2 import Memory
    from akash.proto.akash.base.resources.v1beta4.storage_pb2 import Storage
    from akash.proto.akash.base.resources.v1beta4.resourcevalue_pb2 import ResourceValue
    from akash.proto.cosmos.base.v1beta1.coin_pb2 import DecCoin

    pb_msg = MsgCreateDeployment()

    deployment_id = DeploymentID()
    deployment_id.owner = msg_dict["id"]["owner"]
    deployment_id.dseq = int(msg_dict["id"]["dseq"])
    pb_msg.id.CopyFrom(deployment_id)

    # v1beta4: 'version' field renamed to 'hash'
    hash_field = msg_dict.get("hash") or msg_dict.get("version")
    if hash_field:
        if isinstance(hash_field, str):
            try:
                pb_msg.hash = bytes.fromhex(hash_field)
            except ValueError:
                import hashlib
                pb_msg.hash = hashlib.sha256(hash_field.encode("utf-8")).digest()
        else:
            pb_msg.hash = hash_field
    else:
        import hashlib
        import json
        deployment_data = json.dumps(msg_dict, sort_keys=True).encode("utf-8")
        version_hash = hashlib.sha256(deployment_data).digest()
        pb_msg.hash = version_hash

    # v1beta4: New deposit structure with amount and sources
    from akash.proto.akash.base.deposit.v1.deposit_pb2 import Deposit

    deposit = Deposit()
    deposit_amount = Coin()

    # Handle both old and new deposit formats
    if isinstance(msg_dict["deposit"], dict):
        if "amount" in msg_dict["deposit"] and isinstance(msg_dict["deposit"]["amount"], dict):
            # New format: deposit.amount.denom, deposit.amount.amount
            deposit_amount.denom = msg_dict["deposit"]["amount"]["denom"]
            deposit_amount.amount = msg_dict["deposit"]["amount"]["amount"]
            # Sources: default to SourceBalance (1) if not specified
            if "sources" in msg_dict["deposit"]:
                deposit.sources.extend([int(s) for s in msg_dict["deposit"]["sources"]])
            else:
                deposit.sources.append(1)  # Default: SourceBalance
        else:
            # Old format: deposit.denom, deposit.amount (for backward compatibility)
            deposit_amount.denom = msg_dict["deposit"]["denom"]
            deposit_amount.amount = msg_dict["deposit"]["amount"]
            deposit.sources.append(1)  # Default: SourceBalance

    deposit.amount.CopyFrom(deposit_amount)
    pb_msg.deposit.CopyFrom(deposit)

    for group_data in msg_dict["groups"]:
        group_spec = GroupSpec()
        group_spec.name = group_data["name"]

        signed_by = SignedBy()
        placement_reqs = PlacementRequirements(signed_by=signed_by)
        group_spec.requirements.CopyFrom(placement_reqs)

        for resource_data in group_data["resources"]:
            resource_unit = ResourceUnit()

            resources = Resources()
            resources.id = resource_data["resource"]["id"]

            cpu_val = ResourceValue(
                val=resource_data["resource"]["cpu"]["units"]["val"].encode("utf-8")
            )
            cpu = CPU(units=cpu_val)
            resources.cpu.CopyFrom(cpu)

            memory_val = ResourceValue(
                val=resource_data["resource"]["memory"]["quantity"]["val"].encode(
                    "utf-8"
                )
            )
            memory = Memory(quantity=memory_val)
            resources.memory.CopyFrom(memory)

            for storage_data in resource_data["resource"]["storage"]:
                storage_val = ResourceValue(
                    val=storage_data["quantity"]["val"].encode("utf-8")
                )
                storage = Storage(name=storage_data["name"], quantity=storage_val)

                if "attributes" in storage_data and storage_data["attributes"]:
                    from akash.proto.akash.base.attributes.v1.attribute_pb2 import Attribute
                    for attr_data in storage_data["attributes"]:
                        attr = Attribute()
                        attr.key = attr_data["key"]
                        attr.value = attr_data["value"]
                        storage.attributes.append(attr)

                resources.storage.append(storage)

            from akash.proto.akash.base.resources.v1beta4.gpu_pb2 import GPU

            gpu_units = resource_data["resource"].get("gpu", {}).get("units", {}).get("val", "0")
            gpu_val = ResourceValue(val=gpu_units.encode("utf-8"))
            gpu = GPU(units=gpu_val)

            gpu_attributes = resource_data["resource"].get("gpu", {}).get("attributes", [])
            if gpu_attributes:
                from akash.proto.akash.base.attributes.v1.attribute_pb2 import Attribute
                for attr_data in gpu_attributes:
                    attr = Attribute()
                    attr.key = attr_data["key"]
                    attr.value = attr_data["value"]
                    gpu.attributes.append(attr)

            resources.gpu.CopyFrom(gpu)

            if "endpoints" in resource_data["resource"]:
                from akash.proto.akash.base.resources.v1beta4.endpoint_pb2 import Endpoint

                for endpoint_data in resource_data["resource"]["endpoints"]:
                    endpoint = Endpoint()
                    endpoint.kind = endpoint_data.get("kind", 0)  # 0 = SHARED_HTTP
                    endpoint.sequence_number = endpoint_data.get("sequence_number", 0)
                    resources.endpoints.append(endpoint)

            resource_unit.resource.CopyFrom(resources)
            resource_unit.count = resource_data["count"]

            price_coin = DecCoin()
            price_coin.denom = resource_data["price"]["denom"]
            price_coin.amount = resource_data["price"]["amount"]
            resource_unit.price.CopyFrom(price_coin)

            group_spec.resources.append(resource_unit)

        pb_msg.groups.append(group_spec)

    any_msg.Pack(pb_msg, type_url_prefix="")
    return any_msg


def convert_msg_update_deployment(msg_dict, any_msg):
    """Convert MsgUpdateDeployment dictionary to protobuf."""
    from akash.proto.akash.deployment.v1beta4.deploymentmsg_pb2 import (
        MsgUpdateDeployment,
    )
    from akash.proto.akash.deployment.v1.deployment_pb2 import DeploymentID

    pb_msg = MsgUpdateDeployment()

    deployment_id = DeploymentID()
    deployment_id.owner = msg_dict["id"]["owner"]
    deployment_id.dseq = int(msg_dict["id"]["dseq"])
    pb_msg.id.CopyFrom(deployment_id)

    if "hash" or msg_dict.get("version") in msg_dict and msg_dict["hash" or msg_dict.get("version")]:
        if isinstance(msg_dict["hash" or msg_dict.get("version")], str):
            try:
                pb_msg.hash = bytes.fromhex(msg_dict["hash" or msg_dict.get("version")])
            except ValueError:
                import hashlib
                pb_msg.hash = hashlib.sha256(msg_dict["hash" or msg_dict.get("version")].encode("utf-8")).digest()
        else:
            pb_msg.hash = msg_dict["hash" or msg_dict.get("version")]
    else:
        import hashlib
        import json
        deployment_data = json.dumps(msg_dict, sort_keys=True).encode("utf-8")
        version_hash = hashlib.sha256(deployment_data).digest()
        pb_msg.hash = version_hash

    any_msg.Pack(pb_msg, type_url_prefix="")
    return any_msg


def convert_msg_close_deployment(msg_dict, any_msg):
    """Convert MsgCloseDeployment dictionary to protobuf."""
    from akash.proto.akash.deployment.v1beta4.deploymentmsg_pb2 import (
        MsgCloseDeployment,
    )
    from akash.proto.akash.deployment.v1.deployment_pb2 import DeploymentID

    pb_msg = MsgCloseDeployment()

    deployment_id = DeploymentID()
    deployment_id.owner = msg_dict["id"]["owner"]
    deployment_id.dseq = int(msg_dict["id"]["dseq"])
    pb_msg.id.CopyFrom(deployment_id)

    any_msg.Pack(pb_msg, type_url_prefix="")
    return any_msg


def convert_msg_deposit_deployment(msg_dict, any_msg):
    """Convert MsgDepositDeployment dictionary to protobuf."""
    from akash.proto.akash.deployment.v1beta4.deploymentmsg_pb2 import (
        MsgDepositDeployment,
    )
    from akash.proto.akash.deployment.v1.deployment_pb2 import DeploymentID
    from akash.proto.cosmos.base.v1beta1.coin_pb2 import Coin

    pb_msg = MsgDepositDeployment()

    deployment_id = DeploymentID()
    deployment_id.owner = msg_dict["id"]["owner"]
    deployment_id.dseq = int(msg_dict["id"]["dseq"])
    pb_msg.id.CopyFrom(deployment_id)

    amount_coin = Coin()
    amount_coin.denom = msg_dict["amount"]["denom"]
    amount_coin.amount = msg_dict["amount"]["amount"]
    pb_msg.amount.CopyFrom(amount_coin)

    pb_msg.depositor = msg_dict["depositor"]

    any_msg.Pack(pb_msg, type_url_prefix="")
    return any_msg


def convert_msg_close_group(msg_dict, any_msg):
    """Convert MsgCloseGroup dictionary to protobuf."""
    from akash.proto.akash.deployment.v1beta4.groupmsg_pb2 import MsgCloseGroup
    from akash.proto.akash.deployment.v1.group_pb2 import GroupID

    pb_msg = MsgCloseGroup()

    group_id = GroupID()
    group_id.owner = msg_dict["id"]["owner"]
    group_id.dseq = int(msg_dict["id"]["dseq"])
    group_id.gseq = msg_dict["id"]["gseq"]
    pb_msg.id.CopyFrom(group_id)

    any_msg.Pack(pb_msg, type_url_prefix="")
    return any_msg


def convert_msg_pause_group(msg_dict, any_msg):
    """Convert MsgPauseGroup dictionary to protobuf."""
    from akash.proto.akash.deployment.v1beta4.groupmsg_pb2 import MsgPauseGroup
    from akash.proto.akash.deployment.v1.group_pb2 import GroupID

    pb_msg = MsgPauseGroup()

    group_id = GroupID()
    group_id.owner = msg_dict["id"]["owner"]
    group_id.dseq = int(msg_dict["id"]["dseq"])
    group_id.gseq = msg_dict["id"]["gseq"]
    pb_msg.id.CopyFrom(group_id)

    any_msg.Pack(pb_msg, type_url_prefix="")
    return any_msg


def convert_msg_start_group(msg_dict, any_msg):
    """Convert MsgStartGroup dictionary to protobuf."""
    from akash.proto.akash.deployment.v1beta4.groupmsg_pb2 import MsgStartGroup
    from akash.proto.akash.deployment.v1.group_pb2 import GroupID

    pb_msg = MsgStartGroup()

    group_id = GroupID()
    group_id.owner = msg_dict["id"]["owner"]
    group_id.dseq = int(msg_dict["id"]["dseq"])
    group_id.gseq = msg_dict["id"]["gseq"]
    pb_msg.id.CopyFrom(group_id)

    any_msg.Pack(pb_msg, type_url_prefix="")
    return any_msg
