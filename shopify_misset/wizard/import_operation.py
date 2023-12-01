# -*- coding: utf-8 -*-

from logging import getLogger
from odoo import api,fields,models


_logger = getLogger(__name__)


class ImportOperation(models.TransientModel):
	_inherit = 'import.operation'


	# def create_products(self,product_data_list):
	# 	success_ids,error_ids = [],[]
	# 	feeds = self.env['product.feed']
	# 	for product_data in product_data_list:
	# 		product_feed = self.create_product(product_data)
	# 		if product_feed:
	# 			feeds += product_feed
	# 			success_ids.append(product_data.get('store_id'))
	# 		else:
	# 			error_ids.append(product_data.get('store_id'))
	# 	return success_ids,error_ids,feeds

	def create_product(self,product_data):
		product_feed = False
		variant_data_list = product_data.pop('variants')
		try:
			product_data.update(type='service') #deep
			product_feed = self.env['product.feed'].create(product_data)
		except Exception as e:
			_logger.error(
				"Failed to create feed for Product: {} Due to: {}".format(
					product_data.get('store_id'),
					e.args[0],
				)
			)
		else:
			for variant_data in variant_data_list:
				variant_data.update(feed_templ_id=product_feed.id)
				variant_data.update(type='service') #deep
				try:
					self.env['product.variant.feed'].create(variant_data)
				except Exception as e:
					_logger.error(
						"Failed to create feed for Product Variant: {} Due to: {}".format(
							variant_data.get('store_id'),
							e.args[0],
						)
					)
		return product_feed

	# def create_partners(self,partner_data_list):
	# 	success_ids,error_ids = [],[]
	# 	feeds = self.env['partner.feed']
	# 	for partner_data in partner_data_list:
	# 		partner_feed = self.create_partner(partner_data)
	# 		if partner_feed:
	# 			feeds += partner_feed
	# 			success_ids.append(partner_data.get('store_id'))
	# 		else:
	# 			error_ids.append(partner_data.get('store_id'))
	# 	return success_ids,error_ids,feeds

# 	def create_partner(self,partner_data):
# 		partner_feed = False
# 		contact_data_list = partner_data.pop('contacts',[])
# # Todo: Change feed field from state_id,country_id to state_code,country_code
# 		partner_data['state_id']   = partner_data.pop('state_code',False)
# 		partner_data['country_id'] = partner_data.pop('country_code',False)
# # & remove this code
# 		try:
# 			partner_feed = self.env['partner.feed'].create(partner_data)
# 		except Exception as e:
# 			_logger.error(
# 				"Failed to create feed for Customer: {} Due to: {}".format(
# 					partner_data.get('store_id'),
# 					e.args[0],
# 				)
# 			)
# 		else:
# 			for contact_data in contact_data_list:
# 				partner_feed+=self.create_partner(contact_data)
# 		return partner_feed

# 	def create_orders(self,order_data_list):
# 		success_ids,error_ids = [],[]
# 		feeds = self.env['order.feed']
# 		for order_data in order_data_list:
# 			order_feed = self.create_order(order_data)
# 			if order_feed:
# 				feeds += order_feed
# 				success_ids.append(order_data.get('store_id'))
# 			else:
# 				error_ids.append(order_data.get('store_id'))
# 		return success_ids,error_ids,feeds
#
# 	def create_order(self,order_data):
# 		order_feed = False
# # Todo: Change feed field from state_id,country_id to state_code,country_code
# 		order_data['invoice_state_id']    = order_data.pop('invoice_state_code',False)
# 		order_data['invoice_country_id']  = order_data.pop('invoice_country_code',False)
#
# 		if not order_data.get('same_shipping_billing'):
# 			order_data['shipping_state_id']   = order_data.pop('shipping_state_code',False)
# 			order_data['shipping_country_id'] = order_data.pop('shipping_country_code',False)
# # & remove this code
# 		try:
# 			order_feed = self.env['order.feed'].create(order_data)
# 		except Exception as e:
# 			_logger.error(
# 				"Failed to create feed for Order: {} Due to: {}".format(
# 					order_data.get('store_id'),
# 					e.args[0],
# 				)
# 			)
# 		return order_feed

