from odoo import api, models
from odoo.osv.expression import AND


class AccountReconciliationWidget(models.AbstractModel):
    _inherit = "account.reconciliation.widget"

    @api.model
    def _domain_move_lines_for_reconciliation(
        self,
        st_line,
        aml_accounts,
        partner_id,
        excluded_ids=None,
        search_str=False,
        mode="rp",
    ):
        """Inject OU"""
        result = super()._domain_move_lines_for_reconciliation(
            st_line,
            aml_accounts,
            partner_id,
            excluded_ids=excluded_ids,
            search_str=search_str,
            mode=mode,
        )
        return AND(
            [
                result,
                [
                    "|",
                    ("operating_unit_id", "=", False),
                    (
                        "operating_unit_id",
                        "=",
                        st_line.statement_id.journal_id.operating_unit_id.id,
                    ),
                ],
            ]
        )
