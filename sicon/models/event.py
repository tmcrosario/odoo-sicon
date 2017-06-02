# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Event(models.Model):

    _name = 'sicon.event'

    @api.multi
    def view_concession(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Concession History'),
            'res_model': 'sicon.concession',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env['ir.model.data'].xmlid_to_res_id(
                'sicon.sicon_concession_history_form_view'),
            'res_id': self.concession_history_id.id,
            'target': 'new',
        }

    @api.one
    def unlink(self):
        domain = [
            ('concession_id', '=', self.concession_id.id),
            ('modify_concession', '=', True),
            ('id', '!=', self.id)
        ]

        related_events = self.env['sicon.event'].search(domain)
        newests = related_events.sorted(
            key=lambda r: r.date,
            reverse=True)

        if newests:
            newest = newests[0]
            self.concession_id.fantasy_name = newest.concession_history_id.fantasy_name
            self.concession_id.location = newest.concession_history_id.location
            self.concession_id.business_category_ids = newest.concession_history_id.business_category_ids
            self.concession_id.concessionaire_id = newest.concession_history_id.concessionaire_id.id
            self.concession_id.canon = newest.concession_history_id.canon
            self.concession_id.expiration_date = newest.concession_history_id.expiration_date
            self.concession_id.state = newest.concession_history_id.state

        return super(Event, self).unlink()

    name = fields.Char(
        string='Description',
        required=True
    )

    concession_id = fields.Many2one(
        comodel_name='sicon.concession',
        required=True,
        ondelete='cascade',
        domain=[('concession_id', '=', False)]
    )

    concession_history_id = fields.Many2one(
        comodel_name='sicon.concession'
    )

    concessionaire_id = fields.Many2one(
        comodel_name='res.partner',
        related='concession_history_id.concessionaire_id',
        store=True
    )

    date = fields.Date(
        required=True
    )

    event_type_id = fields.Many2one(
        comodel_name='sicon.event_type',
        required=True
    )

    document_id = fields.Many2one(
        comodel_name='tmc.document'
    )

    other_related_document = fields.Char()

    observations = fields.Html()

    modify_concession = fields.Boolean()

    _order = 'date desc'
