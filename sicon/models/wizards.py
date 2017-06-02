# -*- coding: utf-8 -*-

from odoo import models, fields, api
from ..models.concession import Concession


class Add_Event_Wizard(models.TransientModel):

    _name = 'sicon.add_event_wizard'

    @api.multi
    def save_event(self):

        events_vals = {
           'date': self.date,
           'event_type_id': self.event_type_id.id,
           'name': self.name,
           'concession_id': self.concession_id.id,
           'document_id': self.document_id.id,
           'other_related_document': self.other_related_document,
           'observations': self.observations
        }

        event_model = self.env['sicon.event']
        event = event_model.create(events_vals)

        concession_vals = {
            'fantasy_name': self.fantasy_name,
            'concessionaire_id': self.concessionaire_id.id,
            'business_category_ids': [(6, 0, self.business_category_ids.ids)],
            'location': self.location,
            'canon': self.canon,
            'start_date': self.start_date,
            'expiration_date': self.expiration_date,
            'state': self.state,
            'concession_id': self.concession_id.id,
            'event_id': event.id,
            'name': self.concession_id.name
        }

        if self.modify_concession:

            event.modify_concession = True

            domain = [
                ('concession_id', '=', self.concession_id.id),
                ('modify_concession', '=', True)
            ]

            related_events = self.env['sicon.event'].search(domain)

            newests = related_events.sorted(
                key=lambda r: r.date,
                reverse=True)

            newest = False
            if newests:
                newest = newests[0]

            if newest == event or not newests:

                self.concession_id.fantasy_name = self.fantasy_name
                self.concession_id.location = self.location
                self.concession_id.business_category_ids = self.business_category_ids
                self.concession_id.concessionaire_id = self.concessionaire_id.id
                self.concession_id.canon = self.canon
                self.concession_id.expiration_date = self.expiration_date
                self.concession_id.state = self.state

                concession_vals['changed'] = True

        concession_model = self.env['sicon.concession']
        concession_id = concession_model.create(concession_vals)
        
        event.concession_history_id = concession_id


    concession_id = fields.Many2one(
        comodel_name='sicon.concession',
    )

    date = fields.Date(
        required=True
    )

    event_type_id = fields.Many2one(
        comodel_name='sicon.event_type',
        required=True
    )

    name = fields.Char(
        string='Description',
        required=True
    )

    document_id = fields.Many2one(
        comodel_name='tmc.document',
        string='Administrative Act'
    )

    other_related_document = fields.Char()

    add_observations = fields.Boolean()

    observations = fields.Html()

    modify_concession = fields.Boolean()

    fantasy_name = fields.Char(
        required=True
    )

    concessionaire_id = fields.Many2one(
        comodel_name='res.partner',
        domain=[('concessionaire', '=', 'True')]
    )

    business_category_ids = fields.Many2many(
        comodel_name='sicon.business_category'
    )

    location = fields.Char(
        required=True
    )

    canon = fields.Char()

    start_date = fields.Date()

    expiration_date = fields.Date()

    state = fields.Selection(
        selection=Concession.states,
        required=True
    )
