from odoo import _, fields, models
from odoo.exceptions import UserError


class ConcessionListReportWizard(models.TransientModel):
    _name = "sicon.concession.report.list"
    _description = "Wizard to generate concession list report"
    # TODO(19.0 migration): removed `_inherit = ["tmc.report"]` (model provided by
    # the deleted tmc_data_py3o module). NOTE: check_and_generate_report() below
    # calls self.generate_report(), which came from that mixin and is now undefined
    # — the button will fail until report generation is reimplemented (the py3o
    # report it produced is stubbed in report/concessions_list.xml).

    _listing_options = [("expired", "Expired Concessions"), ("all", "All")]

    listing = fields.Selection(selection=_listing_options, default="all", required=True)

    def get_concessions(self):
        concession_list = None
        concessions_model = self.env["sicon.concession"]
        if self.listing == "all":
            concession_list = concessions_model.search([("concession_id", "=", False)])
        if self.listing == "expired":
            concession_list = concessions_model.search(
                [("concession_id", "=", False), ("expired", "=", True)]
            )
        return concession_list

    def check_and_generate_report(self):
        if not self.get_concessions():
            raise UserError(_("No concessions matched to specified search criteria."))
        # TODO(19.0 migration): report generation is being reimplemented as native
        # QWeb (the py3o `tmc.report` mixin was removed). The wizard button is hidden
        # (invisible="1") until then; this guard replaces the old, now-undefined
        # self.generate_report() call so it fails clearly instead of AttributeError.
        raise UserError(
            _(
                "Concession report generation is temporarily unavailable "
                "(being migrated to QWeb)."
            )
        )
