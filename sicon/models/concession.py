from odoo import api, fields, models


class Concession(models.Model):
    _name = "sicon.concession"
    _description = "Concession"
    _order = "name"

    _expiration_types_ = [("certain", "Certain"), ("uncertain", "Uncertain")]

    _certain_expiration_options_ = [("date", "Date"), ("duration", "Duration")]

    _date_units_ = [
        ("days", " Day(s)"),
        ("months", " Month(s)"),
        ("years", " Year(s)"),
    ]

    states = [
        ("tendered", "Tendered"),
        ("awarded", "Awarded"),
        ("on_term", "On Term"),
        ("extended", "Extended"),
        ("rescinded", "Rescinded"),
    ]

    name = fields.Char(required=True)

    fantasy_name = fields.Char()

    state = fields.Selection(selection=states)

    location = fields.Char(required=True)

    geographical_location = fields.Char()

    additional_information = fields.Char()

    concessionaire_id = fields.Many2one(
        comodel_name="res.partner", domain=[("concessionaire", "=", True)]
    )

    event_ids = fields.One2many(
        comodel_name="sicon.event",
        inverse_name="concession_id",
        string="Events",
    )

    canon = fields.Char()

    start_date = fields.Date()

    expiration_date = fields.Date()

    term_expiration = fields.Selection(selection=_expiration_types_)

    term_certain_expiration = fields.Selection(selection=_certain_expiration_options_)

    term_duration = fields.Integer()

    term_unit = fields.Selection(selection=_date_units_, default="years")

    term_due_date = fields.Date()

    term_description = fields.Text()

    planned_extension = fields.Boolean()

    extension_expiration = fields.Selection(selection=_expiration_types_)

    extension_certain_expiration = fields.Selection(
        selection=_certain_expiration_options_
    )

    extension_duration = fields.Integer()

    extension_unit = fields.Selection(selection=_date_units_, default="years")

    extension_due_date = fields.Date()

    extension_description = fields.Text()

    highest_highlight = fields.Selection(
        selection=[("high", "High"), ("medium", "Medium")],
        compute="_compute_highest_highlight",
    )

    highlight_ids = fields.One2many(
        comodel_name="tmc.highlight", inverse_name="concession_id"
    )

    highlights_count = fields.Integer(compute="_compute_highlights_count")

    event_id = fields.Many2one(comodel_name="sicon.event", ondelete="cascade")

    event_date = fields.Date(related="event_id.date", store=True)

    url_mr = fields.Char()

    related_document_ids = fields.Many2many(
        comodel_name="tmc.document",
        compute="_compute_related_documents",
        readonly=True,
    )

    administrator_id = fields.Many2one(
        comodel_name="sicon.administrator", required=True
    )

    grantor_id = fields.Many2one(comodel_name="sicon.grantor", required=True)

    zone_id = fields.Many2one(comodel_name="sicon.zone", required=True)

    active = fields.Boolean(default=True)

    @api.onchange(
        "planned_extension",
        "term_expiration",
        "term_certain_expiration",
        "extension_due_date",
        "extension_duration",
        "extension_expiration",
        "extension_certain_expiration",
    )
    def _onchange_planned_extension(self):
        if not self.planned_extension:
            self.extension_expiration = False
            self.extension_certain_expiration = False
            self.extension_duration = False
            self.extension_due_date = False
        if self.extension_expiration == "certain":
            self.extension_description = False
        if self.extension_expiration == "uncertain":
            self.extension_certain_expiration = False
        if not self.extension_expiration:
            self.extension_certain_expiration = False
        if not self.extension_certain_expiration:
            self.extension_due_date = False
            self.extension_duration = False

    @api.depends("highlight_ids", "highlight_ids.applicable")
    def _compute_highlights_count(self):
        for concession in self:
            applicable_highlight_ids = concession.highlight_ids.filtered(
                lambda record: record.applicable is True
            )
            concession.highlights_count = len(applicable_highlight_ids)

    @api.depends("event_ids.document_id", "event_ids.related_document_ids")
    def _compute_related_documents(self):
        for concession in self:
            documents = self.env["tmc.document"]
            for event in concession.event_ids:
                documents |= event.document_id
                documents |= event.related_document_ids
            concession.related_document_ids = documents

    def add_event(self):
        return {
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "sicon.event.add",
            "target": "new",
        }

    def open_location(self):
        return {
            "type": "ir.actions.act_url",
            "url": self.geographical_location,
            "target": "new",
        }

    def open_additional_information(self):
        return {
            "type": "ir.actions.act_url",
            "url": self.additional_information,
            "target": "new",
        }

    @api.depends("highlight_ids.applicable", "highlight_ids.level")
    def _compute_highest_highlight(self):
        for concession in self:
            applicable = concession.highlight_ids.filtered("applicable")
            if any(h.level == "high" for h in applicable):
                concession.highest_highlight = "high"
            elif any(h.level == "medium" for h in applicable):
                concession.highest_highlight = "medium"
            else:
                concession.highest_highlight = False
