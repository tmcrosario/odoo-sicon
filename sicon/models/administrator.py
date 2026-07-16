from odoo import fields, models


class Administrator(models.Model):
    _name = "sicon.administrator"
    _description = "Concession Administrator"

    name = fields.Char(required=True)

    _name_unique = models.Constraint("UNIQUE(name)", "Administrator name must be unique")
