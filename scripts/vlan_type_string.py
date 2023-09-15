from pymongo.operations import UpdateOne, UpdateMany
from kytos.core.db import mongo_client

tag_type = {
    1: "vlan",
    2: "vlan_qinq",
    3: "mpls",
}
client = mongo_client()
collection = client["napps"]["evcs"]

# Update paths
up_paths = []
for key, value in tag_type.items():
    up_paths.append(
        UpdateMany(
            {},
            {
                "$set": {
                    "current_path.$[current].metadata.s_vlan.tag_type": value,
                    "failover_path.$[fail].metadata.s_vlan.tag_type": value,
                    "backup_path.$[backup].metadata.s_vlan.tag_type": value,
                    "primary_path.$[primary].metadata.s_vlan.tag_type": value,
                }
            },
            array_filters = [
                {"current.metadata.s_vlan.tag_type": key},
                {"fail.metadata.s_vlan.tag_type": key},
                {"backup.metadata.s_vlan.tag_type": key},
                {"primary.metadata.s_vlan.tag_type": key},
            ]
        ),
    )
evcs = collection.bulk_write(up_paths)

# Update Uni_a
for key, value in tag_type.items():
    uni_a =collection.update_many(
        {"uni_a.tag.tag_type": key},
        {"$set": 
            {"uni_a.tag.tag_type": value}
        }
    )

# Update Uni_z
for key, value in tag_type.items():
    uni_z = collection.update_many(
        {"uni_z.tag.tag_type": key},
        {"$set":
            {"uni_z.tag.tag_type": value}
        }
    )
print(f"Finnished updating EVCs")