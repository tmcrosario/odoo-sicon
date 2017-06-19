# -*- coding: utf-8 -*-

from datetime import date, datetime

from concession import Concession
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class Add_Event_Wizard(models.TransientModel):

    _name = 'sicon.add_event_wizard'

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

    concessionaire_id = fields.Many2one(
        comodel_name='res.partner',
        domain=[('concessionaire', '=', 'True')]
    )

    business_category_ids = fields.Many2many(
        comodel_name='municipal.business_category'
    )

    location = fields.Char()

    canon = fields.Char()

    start_date = fields.Date()

    expiration_date = fields.Date()

    state = fields.Selection(
        selection=Concession.states
    )

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

                con_obj = self.concession_id
                con_obj.location = self.location
                con_obj.business_category_ids = self.business_category_ids
                con_obj.concessionaire_id = self.concessionaire_id.id
                con_obj.canon = self.canon
                con_obj.expiration_date = self.expiration_date
                con_obj.state = self.state

        concession_model = self.env['sicon.concession']
        concession_id = concession_model.create(concession_vals)

        event.concession_history_id = concession_id


class Concessions_Listing_Report_Wizard(models.TransientModel):
    _name = 'sicon.concessions_listing.report.wizard'

    _listing_options = [
        ('expired', 'Expired Concessions'),
        ('all', 'All'),
    ]

    listing = fields.Selection(
        selection=_listing_options,
        default='all',
        required=True
    )

    @api.multi
    def format_date(self, date_string):
        formatted_date = None
        if date_string:
            formatted_date = datetime.strptime(
                date_string, '%Y-%m-%d').strftime('%d/%m/%Y')
        return formatted_date

    @api.multi
    def get_concessions(self):
        concession_list = None
        concessions_model = self.env['sicon.concession']
        if self.listing == 'all':
            concession_list = concessions_model.search(
                [('concession_id', '=', False)])
        if self.listing == 'expired':
            concession_list = concessions_model.search(
                [('concession_id', '=', False),
                 ('expired', '=', True)])
        return concession_list

    @api.multi
    def _prepare_report(self):
        context = self._context.copy()
        context['date'] = date.today().strftime('%d/%m/%Y')
        return self.with_context(context)

    @api.multi
    def generate_report(self):
        if not self.get_concessions():
            raise UserError(
                _('No concessions matched to specified search criteria.'))
        self.ensure_one()
        self = self._prepare_report()
        return self.env['report'].get_action(
            self, 'concessions_listing')
