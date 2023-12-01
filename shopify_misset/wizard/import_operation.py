# -*- coding: utf-8 -*-

from logging import getLogger
from odoo import api, fields, models


_logger = getLogger(__name__)


class ImportOperation(models.TransientModel):
	_inherit = 'import.operation'

	# Overridden:
	def create_product(self,product_data):
		" Force update product type as 'service'"
		product_feed = False
		variant_data_list = product_data.pop('variants')
		try:
			product_data.update(type='service')
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
				variant_data.update(type='service')
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
