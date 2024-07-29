from odoo import models, fields

class HelpdeskSLA(models.Model):
    _name = 'helpdesk.sla'
    _description = 'Helpdesk SLA'

    name = fields.Char(string='Name', required=True)
    team_ids = fields.Many2many('helpdesk.team', string='Helpdesk Teams')
    sla_line_ids = fields.One2many('helpdesk.sla.line', 'helpdesk_sla_id', string='SLA Lines')
