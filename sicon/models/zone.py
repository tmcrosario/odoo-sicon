from odoo import fields, models


class Zone(models.Model):
    _name = "sicon.zone"
    _description = "Concession Zone"

    name = fields.Char(required=True)

    _name_unique = models.Constraint("UNIQUE(name)", "Zone name must be unique")
