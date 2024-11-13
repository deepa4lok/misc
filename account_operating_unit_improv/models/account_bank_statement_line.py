from odoo import api, models


class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"

    @api.model_create_multi
    def create(self, vals_list):
        """Add statement's operating unit to move"""
        result = super().create(vals_list)
        for this in result:
            this.operating_unit_id = this.statement_id.journal_id.operating_unit_id
        return result

    def _prepare_move_line_default_vals(self, counterpart_account_id=None):
        """Set journal's OU on generated MLs"""
        result = super()._prepare_move_line_default_vals(
            counterpart_account_id=counterpart_account_id
        )
        result[0][
            "operating_unit_id"
        ] = self.statement_id.journal_id.operating_unit_id.id
        result[1][
            "operating_unit_id"
        ] = self.statement_id.journal_id.operating_unit_id.id
        return result

    def _prepare_liquidity_move_line_vals(self):
        """Set OU on liquitidy line"""
        result = super()._prepare_liquidity_move_line_vals()
        result["operating_unit_id"] = self.statement_id.journal_id.operating_unit_id.id
        return result

    def _create_counterpart_and_new_aml(
        self, counterpart_moves, counterpart_aml_dicts, new_aml_dicts
    ):
        """Inject OU"""
        operating_unit = self.statement_id.journal_id.operating_unit_id
        return super()._create_counterpart_and_new_aml(
            counterpart_moves,
            [
                dict(
                    _dict,
                    operating_unit_id=operating_unit.id,
                )
                for _dict in counterpart_aml_dicts
            ],
            [
                dict(
                    _dict,
                    operating_unit_id=operating_unit.id,
                )
                for _dict in new_aml_dicts
            ],
        )
