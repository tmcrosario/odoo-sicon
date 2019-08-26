
from odoo import fields, models


class Highlight(models.Model):

    _inherit = 'tmc.highlight'

    concession_id = fields.Many2one(
        comodel_name='sicon.concession',
        ondelete='cascade'
    )
