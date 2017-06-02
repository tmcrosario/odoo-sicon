# -*- coding: utf-8 -*-

from odoo import models, fields


class Partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    concessionaire = fields.Boolean(
        string='Concessionaire'
    )

    drei = fields.Char(
        string='DREI',
        size=10
    )

    drei_mgmt_code = fields.Char(
        string='DREI Management Code',
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
