from odoo import models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    department_id = fields.Many2one(
        'hr.department',
        string='Department',
        help='Department associated with this move'
    )
