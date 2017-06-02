# -*- coding: utf-8 -*-

from odoo import models, fields


class Control_Note(models.Model):

    _name = 'sicon.control_note'

    _status_ = [
        ('pending', 'Pending'),
        ('done', 'Done')
    ]

    name = fields.Char(
        string='Title',
        required=True
    )

    concession_id = fields.Many2one(
        comodel_name='sicon.concession',
        required=True,
        ondelete='cascade'
    )

    date = fields.Date(
        required=True
    )

    details = fields.Html()

    status = fields.Selection(
        selection=_status_,
        default='pending',
        required=True
    )

    _order = 'date desc, write_date desc'
