from odoo import fields, models


class EventType(models.Model):
    _name = "sicon.event_type"
    _description = "Event Type"

    name = fields.Char(required=True)

    description = fields.Text()

    _name_unique = models.Constraint("UNIQUE(name)", "Event type name must be unique")
