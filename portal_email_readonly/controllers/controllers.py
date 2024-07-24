# -*- coding: utf-8 -*-
# from odoo import http


# class PortalEmailReadonly(http.Controller):
#     @http.route('/portal_email_readonly/portal_email_readonly/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/portal_email_readonly/portal_email_readonly/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('portal_email_readonly.listing', {
#             'root': '/portal_email_readonly/portal_email_readonly',
#             'objects': http.request.env['portal_email_readonly.portal_email_readonly'].search([]),
#         })

#     @http.route('/portal_email_readonly/portal_email_readonly/objects/<model("portal_email_readonly.portal_email_readonly"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('portal_email_readonly.object', {
#             'object': obj
#         })
