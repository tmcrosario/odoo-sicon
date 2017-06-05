# -*- coding: utf-8 -*-

from odoo import fields, models


class Partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    concessionaire = fields.Boolean()

    drei = fields.Char(
        size=10
    )

    drei_mgmt_code = fields.Char(
        size=10
    )

    event_ids = fields.One2many(
        comodel_name='sicon.event',
        inverse_name='concessionaire_id'
    )

    drei_ids = fields.One2many(
        comodel_name='sicon.drei',
        inverse_name='concessionaire_id'
    )
