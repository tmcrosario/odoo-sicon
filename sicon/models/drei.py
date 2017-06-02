# -*- coding: utf-8 -*-

from odoo import models, fields


class Drei(models.Model):

    _name = 'sicon.drei'

    account = fields.Char(
        size=10,
        required=True
    )

    management_code = fields.Char(
        string='Personal Management Code',
        size=10
    )

    business_category_ids = fields.Many2many(
        comodel_name='sicon.business_category',
        required=True
    )

    concessionaire_id = fields.Many2one(
        comodel_name='res.partner',
        domain=[('concessionaire', '=', 'True')],
        required=True
    )
