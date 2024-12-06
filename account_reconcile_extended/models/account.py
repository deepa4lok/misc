# -*- coding: utf-8 -*-

from odoo import models, fields, _
from odoo.exceptions import ValidationError

class accountMoveLine(models.Model):
    _inherit = 'account.move.line'

    migration_remarks = fields.Char('Migration Remarks')

    def action_reconcile_manually(self):
        action = super(accountMoveLine, self).action_reconcile_manually()
        if not self:
            return action
        self.env.cr.execute('SELECT account_id, migration_remarks FROM account_move_line WHERE id IN %s GROUP BY account_id, migration_remarks',
                            [tuple(self.ids)])

        data = self.env.cr.dictfetchall()

        if len(data) > 1:
            raise ValidationError(
                _("You can only reconcile journal items belonging to the same account & migration remark.")
            )
        return action
