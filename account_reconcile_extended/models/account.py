# -*- coding: utf-8 -*-

from odoo import models, fields, _, api
from odoo.exceptions import ValidationError

class accountMoveLine(models.Model):
    _inherit = 'account.move.line'

    migration_remarks = fields.Char('Migration Remarks')


class MassReconcileSimpleMigrationRemarks(models.TransientModel):
    _name = "mass.reconcile.simple.migration_remarks"
    _inherit = "mass.reconcile.simple"
    _description = "Mass Reconcile Simple Reference"

    # has to be subclassed
    # field name used as key for matching the move lines
    _key_field = "migration_remarks"


class AccountMassReconcileMethod(models.Model):
    _inherit = "account.mass.reconcile.method"


    def _selection_name(self):
        res = super(AccountMassReconcileMethod, self)._selection_name()
        return res + [(("mass.reconcile.simple.migration_remarks", "Simple. Amount and Migartion Remarks"))]
