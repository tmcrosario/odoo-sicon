from odoo import fields, models


class Partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    concessionaire = fields.Boolean()

    event_ids = fields.One2many(comodel_name='sicon.event',
                                inverse_name='concessionaire_id')

    drei_ids = fields.One2many(comodel_name='municipal.drei',
                               inverse_name='partner_id')
