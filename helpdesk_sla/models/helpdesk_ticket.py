from odoo import models, fields, api
from datetime import datetime, timedelta

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ], string='Ticket Priority')

    response_time_overdue = fields.Boolean(string='Response Time Overdue', compute='_compute_overdue_times', store=True)
    resolution_time_overdue = fields.Boolean(string='Resolution Time Overdue', compute='_compute_overdue_times', store=True)
    remaining_response_time_hours = fields.Integer(string='Remaining Response Time (hours)', compute='_compute_remaining_times', store=True)
    remaining_resolution_time_hours = fields.Integer(string='Remaining Resolution Time (hours)', compute='_compute_remaining_times', store=True)

    @api.depends('priority', 'team_id')
    def _compute_remaining_times(self):
        for ticket in self:
            sla_line = self._get_sla_line(ticket)
            if sla_line:
                ticket.remaining_response_time_hours = self._calculate_remaining_time(ticket.create_date, sla_line.response_time_hours)
                ticket.remaining_resolution_time_hours = self._calculate_remaining_time(ticket.create_date, sla_line.resolution_time_hours)
            else:
                ticket.remaining_response_time_hours = 0
                ticket.remaining_resolution_time_hours = 0

    @api.depends('remaining_response_time_hours', 'remaining_resolution_time_hours')
    def _compute_overdue_times(self):
        for ticket in self:
            ticket.response_time_overdue = ticket.remaining_response_time_hours < 0
            ticket.resolution_time_overdue = ticket.remaining_resolution_time_hours < 0

    def _get_sla_line(self, ticket):
        if ticket.priority and ticket.team_id:
            return self.env['sla.line'].search([
                ('priority', '=', ticket.priority),
                ('sla_id.team_ids', 'in', ticket.team_id.id)
            ], limit=1)
        return None

    def _calculate_remaining_time(self, create_date, sla_hours):
        deadline = create_date + timedelta(hours=sla_hours)
        remaining_time = deadline - datetime.now()
        return int(remaining_time.total_seconds() // 3600)

    @api.model
    def check_sla_deadlines(self):
        tickets = self.search([('response_time_overdue', '=', False), ('resolution_time_overdue', '=', False)])
        for ticket in tickets:
            ticket._compute_overdue_times()
            ticket._compute_remaining_times()
