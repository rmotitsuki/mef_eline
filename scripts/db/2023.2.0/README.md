## MEF-ELine's migration scripts for Kytos version 2023.2.0

This folder contains MEF-ELine's related scripts.

### Change ``tag_type`` from integer to string type

[`000_vlan_type_string.py`](./000_vlan_type_string.py) is a script to change every ``tag_type`` instance from integer to string type. These istances are found in evcs collection from MongoDB.

```
    VLAN = 1 to 'vlan'
    VLAN_QINQ = 2 to 'vlan_qinq'
    MPLS = 3 to 'mpls'
```

#### Pre-requisites

- Make sure MongoDB replica set is up and running.
- Export the following MongnoDB variables accordingly in case your running outside of a container

```
export MONGO_USERNAME=
export MONGO_PASSWORD=
export MONGO_DBNAME=napps
export MONGO_HOST_SEEDS="mongo1:27017,mongo2:27018,mongo3:27099"
```

#### How to use

The following `CMD` commands are available:

```
CMD=aggregate_int_vlan python3 scripts/db/2023.2.0/000_vlan_type_string.py
```
`aggregate_int_vlan` command is to see which EVC needs to be changed whether they have an outdated value type for a TAG inside their `uni_a`, `uni_z`, `current_path`, `failover_path`, `backup_path` or `primary_path`.

```
CMD=update_database python3 scripts/db/2023.2.0/000_vlan_type_string.py
```
`update_database` changes the value of every outdated TAG from integer to their respective string value.
