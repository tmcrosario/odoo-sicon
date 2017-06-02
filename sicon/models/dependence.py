# -*- coding: utf-8 -*-

from odoo import models, fields


class Dependence(models.Model):

    _inherit = 'tmc.dependence'

    sicon = fields.Boolean(
        string='SICON'
    )
