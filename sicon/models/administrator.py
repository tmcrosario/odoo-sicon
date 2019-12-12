from odoo import _, fields, models


class Administrator(models.Model):

    _name = 'sicon.administrator'
    _description = 'Concession Administrator'

    name = fields.Char(required=True)

    _sql_constraints = [('name_unique', 'UNIQUE(name)',
                         _('Administrator name must be unique'))]
