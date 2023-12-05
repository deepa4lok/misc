# -*- coding: utf-8 -*-


from odoo import api, fields, models, exceptions

from logging import getLogger
_logger = getLogger(__name__)



class SaleOrder(models.Model):
    _inherit = "sale.order"

    journal_id = fields.Many2one(
        comodel_name="account.journal",
        string="Billing Journal",
        domain="[('type', '=', 'sale'), '|', ('company_id', '=', False), "
        "('company_id', '=', company_id)]",
        check_company=True,
    )

    @api.multi
    def _prepare_invoice(self):
        "update Journal"
        self.ensure_one()
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals['journal_id'] = self.journal_id.id
        return invoice_vals


