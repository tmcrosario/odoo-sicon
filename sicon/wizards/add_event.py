from odoo import _, api, fields, models
from odoo.exceptions import UserError

from ..models.concession import Concession


class AddEventWizard(models.TransientModel):
    _name = "sicon.event.add"
    _description = "Wizard for adding a new event"

    concession_id = fields.Many2one(comodel_name="sicon.concession")

    date = fields.Date(required=True)

    event_type_id = fields.Many2one(comodel_name="sicon.event_type", required=True)

    name = fields.Char(string="Description", required=True)

    document_id = fields.Many2one(
        comodel_name="tmc.document", string="Administrative Act"
    )

    related_document_ids = fields.Many2many(comodel_name="tmc.document")

    modify_concession = fields.Boolean()

    concessionaire_id = fields.Many2one(
        comodel_name="res.partner", domain=[("concessionaire", "=", "True")]
    )

    fantasy_name = fields.Char()

    canon = fields.Char()

    start_date = fields.Date()

    expiration_date = fields.Date()

    state = fields.Selection(selection=Concession.states)

    def save_event(self):
        if self.document_id:
            if self.date:
                if self.date.year != self.document_id.period:
                    raise UserError(_("Event year must be equal to document period."))

        # Create the event
        events_vals = {
            "date": self.date,
            "event_type_id": self.event_type_id.id,
            "name": self.name,
            "concession_id": self.concession_id.id,
            "document_id": self.document_id.id,
            "related_document_ids": [(6, 0, self.related_document_ids.ids)],
            "concessionaire_id": self.concessionaire_id.id,
            "state": self.state,
        }

        event_model = self.env["sicon.event"]
        event = event_model.create(events_vals)

        # If the event modify the concession then get the newest event
        # If this one is the last event then modify the concession
        if self.modify_concession:
            event.modify_concession = True
            domain = [
                ("concession_id", "=", self.concession_id.id),
                ("modify_concession", "=", True),
            ]
            related_events = self.env["sicon.event"].search(domain)

            newests = related_events.sorted(key=lambda r: r.date, reverse=True)
            newest = False
            if newests:
                newest = newests[0]
            if newest == event or not newests:
                self.concession_id.concessionaire_id = self.concessionaire_id
                self.concession_id.canon = self.canon
                self.concession_id.start_date = self.start_date
                self.concession_id.expiration_date = self.expiration_date
                self.concession_id.state = self.state

    @api.onchange("state")
    def _onchange_state(self):
        if self.state == "rescinded":
            self.concessionaire_id = False
