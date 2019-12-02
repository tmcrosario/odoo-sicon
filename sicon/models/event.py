from odoo import fields, models


class Event(models.Model):

    _name = 'sicon.event'
    _order = 'date desc'

    name = fields.Char(string='Description', required=True)

    concession_id = fields.Many2one(comodel_name='sicon.concession',
                                    required=True,
                                    ondelete='cascade',
                                    domain=[('concession_id', '=', False)])

    date = fields.Date(required=True)

    event_type_id = fields.Many2one(comodel_name='sicon.event_type',
                                    required=True)

    event_type_name = fields.Char(related='event_type_id.name')

    document_id = fields.Many2one(comodel_name='tmc.document')

    document_pdf_url = fields.Char(related='document_id.pdf_url')

    related_document_ids = fields.Many2many(comodel_name='tmc.document')

    modify_concession = fields.Boolean()

    folder_file = fields.Binary()

    folder_filename = fields.Char()

    def open_document_pdf(self):
        return self.document_id.open_pdf()
