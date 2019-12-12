from datetime import datetime
from re import search

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from ..models.concession import Concession


class AddEventWizard(models.TransientModel):

    _name = 'sicon.add_event_wizard'
    _description = 'Wizard for adding a new event'

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
                if self.date.year != self.document_id.period:
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

        self.env['sicon.event'].create(events_vals)

    @api.onchange('state')
    def _onchange_state(self):
        if self.state == 'rescinded':
            self.concessionaire_id = False
