from odoo import _, fields, models
from odoo.exceptions import UserError


class ConcessionListReportWizard(models.TransientModel):

    _name = "sicon.concession.report.list"
    _description = "Wizard to generate concession list report"
    _inherit = ["tmc.report"]

    _listing_options = [("expired", "Expired Concessions"), ("all", "All")]

    listing = fields.Selection(
        selection=_listing_options, default="all", required=True
    )

    def get_concessions(self):
        concession_list = None
        concessions_model = self.env["sicon.concession"]
        if self.listing == "all":
            concession_list = concessions_model.search(
                [("concession_id", "=", False)]
            )
        if self.listing == "expired":
            concession_list = concessions_model.search(
                [("concession_id", "=", False), ("expired", "=", True)]
            )
        return concession_list

    def check_and_generate_report(self):
        if not self.get_concessions():
            raise UserError(
                _("No concessions matched to specified search criteria.")
            )
        return self.generate_report()
