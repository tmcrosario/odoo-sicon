# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import Warning


class Business_Category(models.Model):

    _name = 'sicon.business_category'

    name = fields.Char(
        required=True
    )

    @api.one
    def unlink(self):
        if self.env['sicon.concession'].search([
            ('business_category_ids', 'in', self.ids)
        ]):
            raise Warning(_(
                "You are trying to delete a record that is still referenced!"))
        return super(Business_Category, self).unlink()

    _sql_constraints = [(
        'name_unique',
        'UNIQUE(name)',
        _('Business Category must be unique')
    )]
