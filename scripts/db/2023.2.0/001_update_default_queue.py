#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from kytos.core.db import Mongo



query = {"queue_id": None, "archived": False}
update = { "$set": { "queue_id": -1 }}

def update_default_queue_id(mongo: Mongo):
    db = mongo.client[mongo.db_name]
    count = db.evcs.update_many(
        query,
        update
    ).modified_count

    print(f"Change default queue_id from None to -1 updated: {count}")


def read_evcs(mongo: Mongo):
    db = mongo.client[mongo.db_name]
    cursor = db.evcs.find(
        query
    )
    print(f"EVCs that queue_id will be changed from None to -1:")
    for document in cursor:
        print("EVC ID: ", document["id"], "\n", document, "\n")



def main() -> None:
    """Main function."""
    mongo = Mongo()
    cmds = {
        "update_database": update_default_queue_id,
        "get_candidates": read_evcs,
    }
    try:
        cmd = os.environ["CMD"]
        cmds[cmd](mongo)
    except KeyError:
        print(
            f"Please set the 'CMD' env var. \nIt has to be one of these: {list(cmds.keys())}"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
