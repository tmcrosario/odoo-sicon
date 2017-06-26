# -*- coding: utf-8 -*-

from odoo import fields, models


class Document(models.Model):
    _name = 'tmc.document'
    _inherit = 'tmc.document'

    event_id = fields.Many2one(
        comodel_name='sicon.event'
    )
