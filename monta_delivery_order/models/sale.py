# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import datetime

class Sale(models.Model):
    _inherit = 'sale.order'

    monta_delivery_block_id = fields.Many2one('monta.delivery.block', 'Monta Delivery Block')

    # @api.onchange('commitment_date')
    # def _check_commitment_date(self):
    #     if self.commitment_date and self.commitment_date.date() <= fields.Datetime.now().date():
    #         raise ValidationError(
    #             _("Delivery date must be future date!")
    #         )

    @api.onchange('expected_date')
    def _onchange_expected_date(self):
        self.commitment_date = self.expected_date
        if not self.commitment_date or (self.commitment_date and self.commitment_date.date() <= fields.Datetime.now().date()):
            self.commitment_date = (fields.Datetime.now() + datetime.timedelta(days=1)).date()

    def action_confirm(self):
        if (self.commitment_date and self.commitment_date.date() <= fields.Datetime.now().date())\
                or not self.commitment_date:
            self.commitment_date = (fields.Datetime.now() + datetime.timedelta(days=1)).date()
            # raise ValidationError(
            #     _("Delivery date must be future date OR cannot be empty!")
            # )
        for self_obj in self:
            if self_obj.website_id:
                continue
            delivery_lines = self_obj.order_line.filtered(lambda l: l.is_delivery)
            if self_obj.carrier_id \
                    and not delivery_lines:
                delivery_lines.unlink()
                carrier_vals = self_obj.carrier_id.rate_shipment(self_obj)
                if carrier_vals.get('success'):
                    delivery_message = carrier_vals.get('warning_message', False)
                    delivery_price = carrier_vals['price']
                    self_obj.set_delivery_line(self_obj.carrier_id, delivery_price)
                    self_obj.write({
                        'recompute_delivery_price': False,
                        'delivery_message': delivery_message,
                    })
        return super().action_confirm()

    @api.onchange('partner_id')
    def _partner_onchange(self):
        carrier = (
                self.with_company(self.company_id).partner_id.property_delivery_carrier_id
                or self.with_company(self.company_id).partner_id.commercial_partner_id.property_delivery_carrier_id
        )
        self.carrier_id = carrier and carrier.id or False
