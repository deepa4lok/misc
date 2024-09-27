# -*- coding: utf-8 -*-
# from odoo import http


# class BypassTierValidation(http.Controller):
#     @http.route('/bypass_tier_validation/bypass_tier_validation/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bypass_tier_validation/bypass_tier_validation/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('bypass_tier_validation.listing', {
#             'root': '/bypass_tier_validation/bypass_tier_validation',
#             'objects': http.request.env['bypass_tier_validation.bypass_tier_validation'].search([]),
#         })

#     @http.route('/bypass_tier_validation/bypass_tier_validation/objects/<model("bypass_tier_validation.bypass_tier_validation"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bypass_tier_validation.object', {
#             'object': obj
#         })
