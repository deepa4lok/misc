from odoo import models, fields

class SLALine(models.Model):
    _name = 'helpdesk.sla.line'
    _description = 'SLA Line'

    name = fields.Char(string='Name', required=True)
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Medium'),
        ('2', 'High'),
        ('3', 'Critical')
    ], string='Priority', required=True)
    response_time_hours = fields.Float(string='Response Time (hours)')
    resolution_time_hours = fields.Float(string='Resolution Time (hours)')
    next_working_day = fields.Boolean(string='SLA Starts at Next Working Day')
    helpdesk_sla_id = fields.Many2one('helpdesk.sla', string='SLA', ondelete='cascade')