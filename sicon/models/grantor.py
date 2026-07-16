from odoo import fields, models


class Grantor(models.Model):
    _name = "sicon.grantor"
    _description = "Concession Grantor"

    name = fields.Char(required=True)

    _name_unique = models.Constraint("UNIQUE(name)", "Grantor name must be unique")
