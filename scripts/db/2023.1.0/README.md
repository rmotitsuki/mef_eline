## MEF-ELine's migration scripts for Kytos version 2023.1.0

This folder contains MEF-ELine's related scripts.

### Unset default spf_attribute value

[`000_unset_spf_attribute.py`](./000_unset_spf_attribute.py) is a script to unset both `primary_constraints.spf_attribute` and `secondary_constraints.spf_attribute`. On version 2022.3, this value was explicitly set, so you can use this script to unset this value if you want that spf_attribute follows the default settings.SPF_ATTRIBUTE value.

#### How to use

- Here's an example trying to unset any `primary_constraints.spf_attribute` or  `secondary_constraints.spf_attribute` from all evcs:

```
priority python3 scripts/db/2022.3.0/000_unset_spf_attribute.py
```

- Here's an example trying to unset any `primary_constraints.spf_attribute` or  `secondary_constraints.spf_attribute` from all EVCs 'd33539656d8b40,095e1d6f43c745':

```
EVC_IDS='d33539656d8b40,095e1d6f43c745' priority python3 scripts/db/2022.3.0/000_unset_spf_attribute.py
```

- After that, `kytosd` should be restarted just so `mef_eline` EVCs can get fully reloaded in memory with the expected primary and secondary constraints, this would be the safest route.
