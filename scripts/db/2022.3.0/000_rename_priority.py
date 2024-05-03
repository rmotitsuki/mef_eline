#!/usr/bin/env python
# -*- coding: utf-8 -*-
from napps.kytos.mef_eline.controllers import ELineController


def rename_evc_priority_to_sb_priority() -> int:
    """Rename evcs priority to sb_priority."""
    controller = ELineController()
    db = controller.db
    return db.evcs.update_many(
        {}, {"$rename": {"priority": "sb_priority"}}
    ).modified_count


def main() -> None:
    """Main function."""
    count = rename_evc_priority_to_sb_priority()
    print(f"Rename evc priority as sb_priority updated: {count}")


if __name__ == "__main__":
    main()
