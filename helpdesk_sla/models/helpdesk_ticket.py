from odoo import models, fields, api
from datetime import datetime, timedelta

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Medium'),
        ('2', 'High'),
        ('3', 'Critical')
    ], string='Priority', default='0')

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

    @api.model
    def message_new(self, msg_dict, custom_values=None):
        custom_values = custom_values or {}
        if custom_values.get('model') == 'helpdesk.ticket':
            ticket = self.search([('id', '=', custom_values.get('res_id'))])
            done_stage = self.env.ref('helpdesk_mgmt.helpdesk_ticket_stage_done')
            in_progress_stage = self.env.ref('helpdesk_mgmt.helpdesk_ticket_stage_in_progress')

            if ticket and ticket.stage_id.id == done_stage.id:
                # Update the ticket's stage to 'In Progress'
                ticket.write({'stage_id': in_progress_stage.id})

                # Add the 're-opened' tag
                tag_reopened = self.env.ref('helpdesk_sla.tag_reopened')
                if tag_reopened:
                    ticket.write({'tag_ids': [(4, tag_reopened.id)]})

        return super(HelpdeskTicket, self).message_new(msg_dict, custom_values)

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
