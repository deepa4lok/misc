from odoo import models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    team_id = fields.Many2one(
        'crm.team',
        string='Team',
        help='Sales Team associated with this move'
    )
