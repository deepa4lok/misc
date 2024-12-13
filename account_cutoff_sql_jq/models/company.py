# -*- coding: utf-8 -*-

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    # perform_posting_by_line = fields.Boolean(string="Experimental - Perform Posting by Line", default=False)
    use_description_as_reference = fields.Boolean(string="Use description as reference", check_company=True)
    perform_posting_by_line_jq = fields.Boolean(string="Perform Posting By Line Job Queue", check_company=True)
