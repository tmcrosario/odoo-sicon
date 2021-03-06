from odoo import _, fields, models


class EventType(models.Model):

    _name = 'sicon.event_type'
    _description = 'Event Type'

    name = fields.Char(required=True)

    description = fields.Text()

    _sql_constraints = [('name_unique', 'UNIQUE(name)',
                         _('Event type name must be unique'))]
