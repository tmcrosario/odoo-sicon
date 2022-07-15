from odoo import fields, models


class Partner(models.Model):

    _name = "res.partner"
    _inherit = "res.partner"

    concessionaire = fields.Boolean()

    event_ids = fields.One2many(
        comodel_name="sicon.event", inverse_name="concessionaire_id"
    )
