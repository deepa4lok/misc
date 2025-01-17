# -*- coding: utf-8 -*-
# Copyright 2014-17 Eficent Business and IT Consulting Services, S.L.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HrTimesheetSheet(models.Model):
    _inherit = "hr_timesheet.sheet"

    @api.model
    def _default_department(self):
        employees = self.env['hr.employee'].search([
            ('user_id', '=', self.env.uid)])
        for emp in employees:
            return emp.department_id and emp.department_id.id or False
        return False


    def _check_validator(self):
        validator = False
        grpOfficer = self.env.user.has_group('hr.group_hr_user')
        if self.user_id.id != self.env.uid and self.env.uid in self.validator_user_ids.ids and grpOfficer and self.state == 'confirm':
            validator = True
        self.is_validator = validator

    validator_user_ids = fields.Many2many(
        'res.users',
        string='Validators'
    )

    department_id = fields.Many2one(
        comodel_name='hr.department',
        string='Department',
        default=_default_department,
    )
    is_validator = fields.Boolean(string="Is validator", compute='_check_validator')


    def _get_validator_user_ids(self):
        """Return the list of user_ids that can validate a given timesheet."""
        self.ensure_one()
        for timesheet in self:
            users = []
            if (timesheet.employee_id and
                    timesheet.employee_id.parent_id and
                    timesheet.employee_id.parent_id.user_id):
                users.append(
                    timesheet.employee_id.parent_id.user_id.id)
            if (timesheet.department_id and
                    timesheet.department_id.manager_id and
                    timesheet.department_id.manager_id.user_id and
                    timesheet.department_id.manager_id.user_id.id !=
                    self.env.uid):
                users.append(
                    timesheet.department_id.manager_id.user_id.id)
            elif (timesheet.department_id and
                    timesheet.department_id.parent_id and
                    timesheet.department_id.parent_id.manager_id and
                    timesheet.department_id.parent_id.manager_id.user_id and
                    timesheet.department_id.parent_id.manager_id.
                    user_id.id != self.env.uid):
                users.append(
                    timesheet.department_id.manager_id.user_id.id)
            return list(set(users)) if users else []

    def action_timesheet_confirm(self):
        for sheet in self:
            validators = sheet._get_validator_user_ids()
            sheet.write({'validator_user_ids': [(6, 0, validators)]})
        return super(HrTimesheetSheet, self).action_timesheet_confirm()

    def _check_authorised_validator(self):
        group_hr_manager = self.env.ref('hr.group_hr_manager')
        group_hr_user = self.env.ref('hr.group_hr_user')
        for timesheet in self:
            if group_hr_manager and self.env.uid in group_hr_manager.users.ids:
                continue

            if group_hr_user and self.env.uid in group_hr_user.users.ids:
                continue

            # TODO: check this:
            # TODO: this is not raising, why?:
            if self.env.uid not in timesheet.validator_user_ids.ids:
                raise UserError(_('You are not authorised to approve  or '
                                  'refuse this Timesheet.'))

    def action_timesheet_draft(self):
        self._check_authorised_validator()
        return super(HrTimesheetSheet, self).action_timesheet_draft()

    def action_timesheet_done(self):
        self._check_authorised_validator()
        return super(HrTimesheetSheet, self).action_timesheet_done()
