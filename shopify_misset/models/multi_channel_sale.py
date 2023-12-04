# -*- coding: utf-8 -*-


from odoo import api, fields, models, exceptions

from logging import getLogger
_logger = getLogger(__name__)



class MultiChannelSale(models.Model):
	_inherit = 'multi.channel.sale'

	@api.model
	def _default_company(self):
		user = self.env['res.users'].browse(self._uid)
		if user.company_id:
			return user.company_id.id
		comps = self.env['res.company'].search([('parent_id', '=', False)]).ids
		return comps and comps[0] or False

	company_id = fields.Many2one('res.company', string='Company', required=False, default=_default_company)

	customer_payment_mode_id = fields.Many2one(
			comodel_name="account.payment.mode",
			company_dependent=True,
			check_company=True,
			domain="[('payment_type', '=', 'inbound'),"
				   "('company_id', '=', company_id)]",
			help="Select the default payment mode for the customer.",
			)

	property_payment_term_id = fields.Many2one('account.payment.term', company_dependent=True,
			   string='Customer Payment Terms',
			   domain="[('company_id', 'in', [company_id, False])]",
			   help="This payment term will be used instead of the default one for sales orders and customer invoices")

	journal_id = fields.Many2one(
		comodel_name="account.journal",
		string="Billing Journal",
		domain="[('type', '=', 'sale'), '|', ('company_id', '=', False), "
			   "('company_id', '=', company_id)]",
		check_company=True,
	)

	operating_unit_id = fields.Many2one(
		comodel_name='operating.unit',
		string='Operating Unit',
		domain="[('company_id', '=', company_id)]",
	)




