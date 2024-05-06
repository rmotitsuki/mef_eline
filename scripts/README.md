
### Redeploy symmetric UNI vlans EVPLs

[`001_redeploy_evpls_same_vlans.py`](./001_redeploy_evpls_same_vlans.py) is a CLI script to list and redeploy symmetric (same vlan on both UNIs) EVPLs.

You should use this script if you want to avoid a redundant `set_vlan` instruction that used to be present in the instruction set and if you are upgrading from `2023.1.0`. This script by triggering an EVC redeploy will force that all flows get pushed and overwritten again, it'll temporarily create traffic disruption. The redeploy in this case is just to force that the flows are pushed right away instead of waiting for a network convergence that might result in the flows getting pushed again.

#### Pre-requisites

- `kytosd` must be running
- There's no additional dependency other than the existing core ones

#### How to use

This script exposes two commands: `list` and `update`.

- First you want to `list` to double check which symmetric EVPLs have been found. If you need to just include a subset you can use the ``--included_evcs_filter`` string passing a string of evc ids separated by comma value.

```shell
python scripts/db/2023.2.0/001_redeploy_evpls_same_vlans.py list --included_evcs_filter 'dc533ac942a541,eab1fedf3d654f' | jq

{
  "dc533ac942a541": {
    "name": "1046-1046",
    "uni_a": {
      "tag": {
        "tag_type": "vlan",
        "value": 1046
      },
      "interface_id": "00:00:00:00:00:00:00:01:1"
    },
    "uni_z": {
      "tag": {
        "tag_type": "vlan",
        "value": 1046
      },
      "interface_id": "00:00:00:00:00:00:00:03:1"
    }
  },
  "eab1fedf3d654f": {
    "name": "1070-1070",
    "uni_a": {
      "tag": {
        "tag_type": "vlan",
        "value": 1070
      },
      "interface_id": "00:00:00:00:00:00:00:01:1"
    },
    "uni_z": {
      "tag": {
        "tag_type": "vlan",
        "value": 1070
      },
      "interface_id": "00:00:00:00:00:00:00:03:1"
    }
  }
}
```

- If you're OK with the EVPLs listed on `list`, then you can proceed to `update` to trigger a redeploy. You can also set ``--batch_size`` and ``--batch_sleep_secs`` to control respectively how many EVPLs will be redeployed concurrently and how long to wait after each batch is sent:

```
python scripts/db/2023.2.0/001_redeploy_evpls_same_vlans.py update --batch_size 10 --batch_sleep_secs 5 --included_evcs_filter 'dc533ac942a541,eab1fedf3d654f'

2023-11-01 16:29:45,980 - INFO - It'll redeploy 2 EVPL(s) using batch_size 10 and batch_sleep 5
2023-11-01 16:29:46,123 - INFO - Redeployed evc_id dc533ac942a541
2023-11-01 16:29:46,143 - INFO - Redeployed evc_id eab1fedf3d654f
```

- If you want to redeploy all symmetric EVPLs batching 10 EVCs concurrently and waiting for 5 seconds per batch:

```
python scripts/db/2023.2.0/001_redeploy_evpls_same_vlans.py update --batch_size 10 --batch_sleep_secs 5


2023-11-01 16:23:11,081 - INFO - It'll redeploy 100 EVPL(s) using batch_size 10 and batch_sleep 5
2023-11-01 16:23:11,724 - INFO - Redeployed evc_id 0ca460bafb7442
2023-11-01 16:23:11,725 - INFO - Redeployed evc_id 0645d179d9174f
2023-11-01 16:23:11,752 - INFO - Redeployed evc_id 0b45959b6a484b
2023-11-01 16:23:11,763 - INFO - Redeployed evc_id 0a270fd5a2ce47
2023-11-01 16:23:11,779 - INFO - Redeployed evc_id 08a72e3c1ecb40
2023-11-01 16:23:11,780 - INFO - Redeployed evc_id 09a5a3b14f9048
2023-11-01 16:23:11,780 - INFO - Redeployed evc_id 0e658df33a9d46
2023-11-01 16:23:11,783 - INFO - Redeployed evc_id 1096fff414c649
2023-11-01 16:23:11,789 - INFO - Redeployed evc_id 0a5702d65da64c
2023-11-01 16:23:11,802 - INFO - Redeployed evc_id 07e3c962346947
2023-11-01 16:23:11,802 - INFO - Sleeping for 5...
2023-11-01 16:23:17,498 - INFO - Redeployed evc_id 1b884a1dd8f147
2023-11-01 16:23:17,538 - INFO - Redeployed evc_id 23270946ce1044
2023-11-01 16:23:17,541 - INFO - Redeployed evc_id 18610fbbcfe54e
2023-11-01 16:23:17,543 - INFO - Redeployed evc_id 1a10cb2638d746
2023-11-01 16:23:17,543 - INFO - Redeployed evc_id 25f2269466cc42
2023-11-01 16:23:17,544 - INFO - Redeployed evc_id 2c332447842b42
2023-11-01 16:23:17,546 - INFO - Redeployed evc_id 2ddf3e33b5fd4b
2023-11-01 16:23:17,547 - INFO - Redeployed evc_id 168346ab0be845
2023-11-01 16:23:17,554 - INFO - Redeployed evc_id 21aff155f11e49
2023-11-01 16:23:17,555 - INFO - Redeployed evc_id 215aeb07f34543
2023-11-01 16:23:17,555 - INFO - Sleeping for 5...

```
