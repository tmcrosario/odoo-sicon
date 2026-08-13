from psycopg2 import IntegrityError

from odoo.tests.common import TransactionCase
from odoo.tools import mute_logger


class TestZone(TransactionCase):
    def setUp(self):
        super().setUp()
        self.zone_model = self.env["sicon.zone"]

    def test_zone_creation(self):
        zone_data = {"name": "Test Zone"}
        zone = self.zone_model.create(zone_data)

        self.assertEqual(zone.name, "Test Zone", "Zone name should be 'Test Zone'")

    @mute_logger("odoo.sql_db")
    def test_zone_duplicate_name(self):
        self.zone_model.create({"name": "Duplicate Zone"})

        # 19.0: ORM writes are deferred, so the unique-constraint violation only
        # surfaces on flush; flush_all() forces it inside assertRaises.
        with self.assertRaises(IntegrityError):
            self.zone_model.create({"name": "Duplicate Zone"})
            self.env.flush_all()
