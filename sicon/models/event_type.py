# -*- coding: utf-8 -*-

from odoo import models, fields


class Event_Type(models.Model):

    _name = 'sicon.event_type'

    name = fields.Char(
        required=True
    )

    description = fields.Text()
