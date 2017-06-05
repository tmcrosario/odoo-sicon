# -*- coding: utf-8 -*-

from odoo import fields, models


class Dependence(models.Model):

    _inherit = 'tmc.dependence'

    sicon = fields.Boolean()
