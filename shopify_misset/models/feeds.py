# -*- coding: utf-8 -*-

from logging import getLogger
from odoo import api, fields, models

from odoo.addons.odoo_multi_channel_sale.tools import parse_float, extract_list as EL
from odoo.addons.odoo_multi_channel_sale.models.order_feed import PartnerFields

_logger = getLogger(__name__)


class PartnerFeed(models.Model):
    _inherit = ["partner.feed"]


    # Overridden:
    def import_partner(self,channel_id):
        """ Update Payment Mode & Payment Terms from Channel """

        message = ""
        state = 'done'
        update_id = None
        create_id = None
        self.ensure_one()
        vals = EL(self.read(PartnerFields))
        _type = vals.get('type')
        store_id = vals.pop('store_id')
        vals.pop('website_message_ids','')
        vals.pop('message_follower_ids','')
        match = channel_id.match_partner_mappings(store_id,_type)
        name = vals.pop('name')

        # Force update Company Name, if found.
        company = vals.pop('company')
        if company and self.type == 'contact':
            name = company
            vals['company_type'] = 'company'

        if not name:
            message+="<br/>Partner without name can't evaluated."
            state = 'error'
        if not store_id:
            message+="<br/>Partner without store id can't evaluated."
            state = 'error'
        parent_store_id = vals['parent_id']
        if parent_store_id:
            partner_res = self.get_partner_id(parent_store_id,channel_id=channel_id)
            message += partner_res.get('message')
            partner_id = partner_res.get('partner_id')
            if partner_id:
                vals['parent_id'] = partner_id.id
            else:
                state = 'error'

        # Payment Term & Mode:
        vals['customer_payment_mode_id'] = channel_id.customer_payment_mode_id and channel_id.customer_payment_mode_id.id or False
        vals['property_payment_term_id'] = channel_id.property_payment_term_id and channel_id.property_payment_term_id.id or False

        if state == 'done':
            country_id = vals.pop('country_id')
            if country_id:
                country_id = channel_id.get_country_id(country_id)
                if country_id:
                    vals['country_id'] = country_id.id
            state_id = vals.pop('state_id')
            state_name = vals.pop('state_name')

            if (state_id or state_name) and country_id:
                state_id = channel_id.get_state_id(state_id,country_id,state_name)
                if state_id:
                    vals['state_id'] = state_id.id
            last_name = vals.pop('last_name','')
            if last_name:
                vals['name'] = "%s %s" % (name, last_name)
            else:
                vals['name'] =name
        if match:
            if  state =='done' :
                try:
                    match.odoo_partner.write(vals)
                    message +='<br/> Partner %s successfully updated'%(name)
                except Exception as e:
                    message += '<br/>%s' % (e)
                    state = 'error'
                update_id = match

            elif state =='error':
                message+='Error while partner updated.'

        else:
            if state == 'done':
                try:
                    erp_id = self.env['res.partner'].create(vals)
                    create_id =  channel_id.create_partner_mapping(erp_id, store_id,_type)
                    message += '<br/>Partner %s successfully evaluated.'%(name)
                except Exception as e:
                    message += '<br/>%s' % (e)
                    state = 'error'
        self.set_feed_state(state=state)
        self.message = "%s <br/> %s" % (self.message, message)
        return dict(
            create_id=create_id,
            update_id=update_id,
            message=message
        )

class OrderFeed(models.Model):
    _inherit = ["order.feed"]

    # Overridden:
    @api.multi
    def import_order(self,channel_id):
        """ Update Journal & Operating Unit from Channel """

        message = ""
        update_id=None
        create_id=None
        self.ensure_one()
        vals = EL(self.read(self.get_order_fields()))
        store_id = vals.pop('store_id')

        store_source = vals.pop('store_source')
        match = channel_id.match_order_mappings(store_id)
        state = 'done'
        store_partner_id = vals.pop('partner_id')


        date_info = self.get_order_date_info(channel_id,vals)
        if date_info.get('date_order'):
            vals['date_order']=date_info.get('date_order')
        date_invoice =  date_info.get('date_invoice')
        confirmation_date = date_info.get('confirmation_date')

        if store_partner_id:
            res_partner = self.get_order_partner_id(store_partner_id,channel_id)
            message += res_partner.get('message', '')
            partner_id = res_partner.get('partner_id')
            partner_invoice_id = res_partner.get('partner_invoice_id')
            partner_shipping_id = res_partner.get('partner_shipping_id')
            if partner_id and partner_invoice_id and partner_shipping_id:
                vals['partner_id'] = partner_id.id
                vals['partner_invoice_id'] = partner_invoice_id.id
                vals['partner_shipping_id'] = partner_shipping_id.id
            else:
                message += '<br/>Partner, Invoice, Shipping Address must present.'
                state = 'error'
                _logger.error('#OrderError1 %r'%message)
        else:
            message += '<br/>No partner in sale order data.'
            state = 'error'
            _logger.error('#OrderError2 %r'%message)


        # Update Payment Term & Payment Mode
        vals['payment_term_id'] = partner_id.property_payment_term_id and partner_id.property_payment_term_id.id or False
        vals['payment_mode_id'] = partner_id.customer_payment_mode_id and partner_id.customer_payment_mode_id.id or False


        if state=='done':
            carrier_id = vals.pop('carrier_id','')

            if carrier_id:
                carrier_res = self.get_carrier_id(carrier_id,channel_id=channel_id)
                message += carrier_res.get('message')
                carrier_id = carrier_res.get('carrier_id')
                if carrier_id:
                    vals['carrier_id'] = carrier_id.id
            order_line_res = self._get_order_line_vals(vals,carrier_id,channel_id)
            message += order_line_res.get('message', '')
            if not order_line_res.get('status'):
                state = 'error'
                _logger.error('#OrderError3 %r'%order_line_res)
            else:
                order_line = order_line_res.get('order_line')
                if len(order_line):
                    vals['order_line'] = order_line
                    state = 'done'
        currency = self.currency

        if state=='done' and currency:
            currency_id = channel_id.get_currency_id(currency)
            if not currency_id:
                message += '<br/> Currency %s no active in Odoo'%(currency)
                state = 'error'
                _logger.error('#OrderError4 %r'%message)
            else:
                pricelist_id = channel_id.match_create_pricelist_id(currency_id)
                vals['pricelist_id']=pricelist_id.id

        vals.pop('name')
        vals.pop('id')
        vals.pop('website_message_ids','')
        vals.pop('message_follower_ids','')
        vals['team_id'] = channel_id.crm_team_id.id
        vals['warehouse_id'] = channel_id.warehouse_id.id

        # Journal & Operating Unit:
        vals['journal_id'] = channel_id.journal_id.id or False
        vals['operating_unit_id'] = channel_id.operating_unit_id.id or False

        if match and match.order_name:
            if  state =='done' :
                try:

                    order_state = vals.pop('order_state')
                    if match.order_name.state=='draft':
                        match.order_name.write(dict(order_line=[(5,0)]))
                        match.order_name.write(vals)
                        message +='<br/> Order %s successfully updated'%(vals.get('name',''))
                    else:
                        message+='Only order state can be update as order not in draft state.'
                    message += self.env['multi.channel.skeleton']._SetOdooOrderState(match.order_name, channel_id,
                            order_state, self.payment_method,date_invoice=date_invoice,confirmation_date=confirmation_date)
                except Exception as e:
                    message += '<br/>%s' % (e)
                    _logger.error('#OrderError5  %r'%message)
                    state = 'error'
                update_id = match
            elif state =='error':
                message+='<br/>Error while order update.'
        else:
            if state == 'done':
                try:
                    order_state = vals.pop('order_state')
                    erp_id = self.env['sale.order'].create(vals)
                    message += self.env['multi.channel.skeleton']._SetOdooOrderState(erp_id, channel_id,  order_state, self.payment_method,date_invoice=date_invoice,confirmation_date=confirmation_date)
                    message  += '<br/> Order %s successfully evaluated'%(self.store_id)
                    create_id =  channel_id.create_order_mapping(erp_id, store_id,store_source)

                except Exception as e:
                    message += '<br/>%s' % (e)
                    _logger.error('#OrderError6 %r'%message)
                    state = 'error'
        self.set_feed_state(state=state)
        self.message = "%s <br/> %s" % (self.message, message)
        return dict(
            create_id=create_id,
            update_id=update_id,
            message=message
        )