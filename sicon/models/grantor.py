from odoo import _, fields, models


class Grantor(models.Model):
    _name = "sicon.grantor"
    _description = "Concession Grantor"

    name = fields.Char(required=True)

    _sql_constraints = [
        ("name_unique", "UNIQUE(name)", _("Grantor name must be unique"))
    ]
