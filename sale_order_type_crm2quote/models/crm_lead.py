# -*- coding: utf-8 -*-
# Copyright (C) 2024 The Open Source Company (<https://www.tosc.nl>)

from odoo import models, fields, api, _

class Lead(models.Model):
    _inherit = ["crm.lead"]


    #Overridden:
    def action_new_quotation(self):
        original = super(Lead, self).action_new_quotation()
        ctx = original.get('context', {})

        action = self.env["ir.actions.actions"]._for_xml_id("sale_order_type_crm2quote.action_lead2quoteSOT")
        action['context'] = ctx
        return action
