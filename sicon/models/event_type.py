# -*- coding: utf-8 -*-

from odoo import _, fields, models


class EventType(models.Model):

    _name = 'sicon.event_type'

    name = fields.Char(
        required=True
    )

    description = fields.Text()

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         _('Event type name must be unique'))
    ]
