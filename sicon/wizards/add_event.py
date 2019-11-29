from datetime import datetime
from re import search

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from ..models.concession import Concession


class AddEventWizard(models.TransientModel):

    _name = 'sicon.add_event_wizard'

    concession_id = fields.Many2one(comodel_name='sicon.concession')

    date = fields.Date(required=True)

    event_type_id = fields.Many2one(comodel_name='sicon.event_type',
                                    required=True)

    name = fields.Char(string='Description', required=True)

    document_id = fields.Many2one(comodel_name='tmc.document',
                                  string='Administrative Act')

    related_document_ids = fields.Many2many(comodel_name='tmc.document')

    modify_concession = fields.Boolean()

    concessionaire_id = fields.Many2one(comodel_name='res.partner',
                                        domain=[('concessionaire', '=', 'True')
                                                ])

    business_category_ids = fields.Many2many(
        comodel_name='municipal.business_category')

    fantasy_name = fields.Char()

    canon = fields.Char()

    start_date = fields.Date()

    expiration_date = fields.Date()

    state = fields.Selection(selection=Concession.states)

    folder_file = fields.Binary()

    folder_filename = fields.Char()

    @api.onchange('folder_file', 'document_id')
    def _onchange_folder_file(self):
        if self.folder_file and self.date:
            tmp = search(r'\.[A-Za-z0-9]+$', self.folder_filename)
            extension = tmp.group(0) if tmp else ""
            date = datetime.strptime(self.date,
                                     '%Y-%m-%d').strftime('%d-%m-%Y')
            self.folder_filename = 'pliego-' + date + extension

    def save_event(self):
        if self.document_id:
            if self.date:
                event_year = datetime.strptime(self.date,
                                               '%Y-%m-%d').strftime('%Y')
                if event_year != str(self.document_id.period):
                    raise UserError(
                        _('Event year must be equal to document period.'))

        events_vals = {
            'date': self.date,
            'event_type_id': self.event_type_id.id,
            'name': self.name,
            'concession_id': self.concession_id.id,
            'document_id': self.document_id.id,
            'related_document_ids': [(6, 0, self.related_document_ids.ids)],
            'folder_file': self.folder_file,
            'folder_filename': self.folder_filename
        }

        event_model = self.env['sicon.event']
        event = event_model.create(events_vals)

        concession_vals = {
            'concessionaire_id': self.concessionaire_id.id,
            'business_category_ids': [(6, 0, self.business_category_ids.ids)],
            'fantasy_name': self.concession_id.fantasy_name,
            'location': self.concession_id.location,
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
            domain = [('concession_id', '=', self.concession_id.id),
                      ('modify_concession', '=', True)]
            related_events = self.env['sicon.event'].search(domain)

            newests = related_events.sorted(key=lambda r: r.date, reverse=True)
            newest = False
            if newests:
                newest = newests[0]
            if newest == event or not newests:
                con_obj = self.concession_id
                con_obj.fantasy_name = self.concession_id.fantasy_name
                con_obj.location = self.concession_id.location
                con_obj.business_category_ids = self.business_category_ids
                con_obj.concessionaire_id = self.concessionaire_id.id
                con_obj.canon = self.canon
                con_obj.start_date = self.start_date
                con_obj.expiration_date = self.expiration_date
                con_obj.state = self.state

        concession_model = self.env['sicon.concession']
        concession_id = concession_model.create(concession_vals)

        event.concession_history_id = concession_id

    @api.onchange('state')
    def _onchange_state(self):
        if self.state in ['rescinded', 'caducous']:
            self.concessionaire_id = False
