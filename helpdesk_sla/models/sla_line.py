from odoo import models, fields

class SLALine(models.Model):
    _name = 'sla.line'
    _description = 'SLA Line'

    name = fields.Char(string='Name', required=True)
    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ], string='Priority', required=True)
    response_time_hours = fields.Float(string='Response Time (hours)')
    resolution_time_hours = fields.Float(string='Resolution Time (hours)')
    next_working_day = fields.Boolean(string='SLA Starts at Next Working Day')
    sla_id = fields.Many2one('helpdesk.sla', string='SLA', ondelete='cascade')
