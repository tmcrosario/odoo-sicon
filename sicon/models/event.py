# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class Event(models.Model):

    _name = 'sicon.event'
    _order = 'date desc'

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

    related_document_ids = fields.Many2many(
        comodel_name='tmc.document'
    )

    modify_concession = fields.Boolean()

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
            con_obj = self.concession_id
            con_hist_obj = newest.concession_history_id

            con_obj.location = con_hist_obj.location
            con_obj.business_category_ids = con_hist_obj.business_category_ids
            con_obj.concessionaire_id = con_hist_obj.concessionaire_id.id
            con_obj.canon = con_hist_obj.canon
            con_obj.expiration_date = con_hist_obj.expiration_date
            con_obj.state = con_hist_obj.state

        return super(Event, self).unlink()
