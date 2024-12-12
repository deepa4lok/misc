# -*- coding: utf-8 -*-
# from odoo import http


# class PurchaseOrderExtended(http.Controller):
#     @http.route('/purchase_order_extended/purchase_order_extended', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/purchase_order_extended/purchase_order_extended/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('purchase_order_extended.listing', {
#             'root': '/purchase_order_extended/purchase_order_extended',
#             'objects': http.request.env['purchase_order_extended.purchase_order_extended'].search([]),
#         })

#     @http.route('/purchase_order_extended/purchase_order_extended/objects/<model("purchase_order_extended.purchase_order_extended"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('purchase_order_extended.object', {
#             'object': obj
#         })
