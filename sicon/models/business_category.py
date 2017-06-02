# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import Warning


class Business_Category(models.Model):

    _name = 'sicon.business_category'

    @api.one
    def unlink(self):
        concession_model = self.env['sicon.concession']
        if concession_model.search([('business_category_ids', 'in', self.ids)]):
            raise Warning(_(
                "You are trying to delete a record that is still referenced!"))
        return super(Business_Category, self).unlink()

    name = fields.Char(
        required=True
    )

    _sql_constraints = [(
        'name_unique',
        'UNIQUE(name)',
        _('Business Category must be unique')
    )]
