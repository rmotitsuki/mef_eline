"""Tests for the DB controller."""
from unittest import TestCase
from unittest.mock import MagicMock

from controllers import ELineController


class TestControllers(TestCase):
    """Test DB Controllers"""

    def setUp(self) -> None:
        self.eline = ELineController(MagicMock())
        self.evc_dict = {
            "id": "1234",
            "uni_a": {
                "interface_id": "00:00:00:00:00:00:00:01:1",
                "tag": {
                    "tag_type": 1,
                    "value": 200,
                }
            },
            "uni_z": {
                "interface_id": "00:00:00:00:00:00:00:02:2",
                "tag": {
                    "tag_type": 1,
                    "value": 200,
                }
            },
            "name": "EVC 1",
            "dynamic_backup_path": True,
            "creation_time": "2022-05-06T21:34:10",
            "priority": 100,
            "active": False,
            "enabled": True,
            "circuit_scheduler": []
        }

    def test_bootstrap_indexes(self):
        """Test bootstrap_indexes"""
        self.eline.bootstrap_indexes()
        expected_indexes = [
            ("evcs", [("circuit_scheduler", 1)]),
            ("evcs", [("archived", 1)]),
        ]
        mock = self.eline.mongo.bootstrap_index
        assert mock.call_count == len(expected_indexes)

    def test_get_circuits(self):
        """Test get_circuits"""

        assert "circuits" in self.eline.get_circuits()
        assert self.eline.db.evcs.aggregate.call_count == 1

    def test_get_circuits_archived(self):
        """Test get_circuits archived filter"""

        self.eline.get_circuits(archived=None)
        arg1 = self.eline.db.evcs.aggregate.call_args[0]
        assert "$match" not in arg1[0][0]

        self.eline.get_circuits(archived=True)
        arg1 = self.eline.db.evcs.aggregate.call_args[0]
        assert arg1[0][0]["$match"] == {'archived': True}

    def test_upsert_evc(self):
        """Test upsert_evc"""

        self.eline.upsert_evc(self.evc_dict)
        assert self.eline.db.evcs.find_one_and_update.call_count == 1

    def test_update_bulk_evc(self):
        """Test update_bulk_evc"""
        circuit_ids = ["123", "456", "789"]
        metadata = {"$set": {"metadata.info": "testing"}}
        self.eline.update_bulk_evc(circuit_ids, metadata)
        arg = self.eline.db.evcs.bulk_write.call_args[0][0]
        assert len(arg) == 3
        assert self.eline.db.evcs.bulk_write.call_count == 1
