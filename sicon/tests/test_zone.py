from odoo.tests.common import TransactionCase
from psycopg2 import IntegrityError


class TestZone(TransactionCase):
    def setUp(self):
        super(TestZone, self).setUp()
        self.zone_model = self.env["sicon.zone"]

    def test_zone_creation(self):
        zone_data = {"name": "Test Zone"}
        zone = self.zone_model.create(zone_data)

        self.assertEqual(zone.name, "Test Zone", "Zone name should be 'Test Zone'")

    def test_zone_duplicate_name(self):
        zone_data_1 = {"name": "Duplicate Zone"}
        zone_data_2 = {"name": "Duplicate Zone"}

        self.zone_model.create(zone_data_1)

        with self.assertRaises(
            IntegrityError, msg="duplicate key value violates unique constraint"
        ):
            self.zone_model.create(zone_data_2)
