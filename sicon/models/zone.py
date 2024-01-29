from odoo import _, fields, models


class Zone(models.Model):
    _name = "sicon.zone"
    _description = "Concession Zone"

    name = fields.Char(required=True)

    _sql_constraints = [("name_unique", "UNIQUE(name)", _("Zone name must be unique"))]
