import os
import sys
from pymongo.operations import UpdateOne, UpdateMany
from kytos.core.db import mongo_client, Mongo


TAG_TYPE = {
    1: "vlan",
    2: "vlan_qinq",
    3: "mpls",
}

def update_database(mongo: Mongo):
    db = mongo.client[mongo.db_name]

    # Update paths
    up_paths = []
    for key, value in TAG_TYPE.items():
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
    evcs = db.evcs.bulk_write(up_paths)
    print(f"{evcs.modified_count} documents where PATH are modified")

    # Update Uni_a
    for key, value in TAG_TYPE.items():
        uni_a =db.evcs.update_many(
            {"uni_a.tag.tag_type": key},
            {"$set": 
                {"uni_a.tag.tag_type": value}
            }
        )
        print(f"{uni_a.modified_count} documents where UNI_A tag_type {key}"
              f" are modified to {value}")

    # Update Uni_z
    for key, value in TAG_TYPE.items():
        uni_z = db.evcs.update_many(
            {"uni_z.tag.tag_type": key},
            {"$set":
                {"uni_z.tag.tag_type": value}
            }
        )
        print(f"{uni_z.modified_count} documents where UNI_Z tag_type {key}"
              f" are modified to {value}")

def aggregate_int_vlan(mongo: Mongo):
    db = mongo.client[mongo.db_name]
    for key, value in TAG_TYPE.items():
        matching_documents = db.evcs.aggregate([
            {
                "$match": {
                    "$or": [
                        {"current_path": {"$elemMatch": {"metadata.s_vlan.tag_type": key}}},
                        {"failover_path": {"$elemMatch": {"metadata.s_vlan.tag_type": key}}},
                        {"backup_path": {"$elemMatch": {"metadata.s_vlan.tag_type": key}}},
                        {"primary_path": {"$elemMatch": {"metadata.s_vlan.tag_type": key}}},
                        {"uni_a.tag.tag_type": key},
                        {"uni_z.tag.tag_type": key},
                    ]
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "id": 1,
                    "current_path": 1,
                    "failover_path": 1,
                    "backup_path": 1,
                    "primary_path": 1,
                    "uni_a": 1,
                    "uni_z": 1
                }
            }
        ])
        result = list(matching_documents)
        if result:
            print(f"EVCs that their tag_type {key} will be change to {value}:")
            for document in result:
                print("EVC ID: ", document["id"], "\n", document)
                print()

if __name__ == "__main__":
    mongo = Mongo()
    cmds = {
        "aggregate_int_vlan": aggregate_int_vlan,
        "update_database": update_database,
    }
    try:
        cmd = os.environ["CMD"]
        cmds[cmd](mongo)
    except KeyError:
        print(
            f"Please set the 'CMD' env var. \nIt has to be one of these: {list(cmds.keys())}"
        )
        sys.exit(1)
