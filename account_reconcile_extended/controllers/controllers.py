# -*- coding: utf-8 -*-
# from odoo import http


# class AccountReconcileExtended(http.Controller):
#     @http.route('/account_reconcile_extended/account_reconcile_extended', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_reconcile_extended/account_reconcile_extended/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_reconcile_extended.listing', {
#             'root': '/account_reconcile_extended/account_reconcile_extended',
#             'objects': http.request.env['account_reconcile_extended.account_reconcile_extended'].search([]),
#         })

#     @http.route('/account_reconcile_extended/account_reconcile_extended/objects/<model("account_reconcile_extended.account_reconcile_extended"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_reconcile_extended.object', {
#             'object': obj
#         })
