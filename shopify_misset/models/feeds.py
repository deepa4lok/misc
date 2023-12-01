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
        create_id=None
        self.ensure_one()
        vals = EL(self.read(PartnerFields))
        _type =vals.get('type')
        store_id = vals.pop('store_id')
        vals.pop('website_message_ids','')
        vals.pop('message_follower_ids','')
        match = channel_id.match_partner_mappings(store_id,_type)
        name = vals.pop('name')
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
                vals['parent_id'] =partner_id.id
            else:
                state = 'error'

        # Payment Term & Mode:
        if channel_id.customer_payment_mode_id:
            vals['customer_payment_mode_id'] = channel_id.customer_payment_mode_id.id
        if channel_id.property_payment_term_id:
            vals['property_payment_term_id'] = channel_id.property_payment_term_id.id

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