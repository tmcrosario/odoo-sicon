from odoo import fields, models
from odoo.exceptions import UserError


class ConcessionListReportWizard(models.TransientModel):
    _name = "sicon.concession.report.list"
    _description = "Wizard to generate concession list report"

    _listing_options = [("expired", "Expired Concessions"), ("all", "All")]

    listing = fields.Selection(selection=_listing_options, default="all", required=True)

    def get_concessions(self):
        # Root concessions only; event_id set marks event-derived snapshots
        domain = [("event_id", "=", False)]
        if self.listing == "expired":
            domain.append(("expiration_date", "<=", fields.Date.today()))
        return self.env["sicon.concession"].search(domain)

    def check_and_generate_report(self):
        if not self.get_concessions():
            raise UserError(
                self.env._("No concessions matched to specified search criteria.")
            )
        return self.env.ref("sicon.concessions_report_list").report_action(self)
