# -*-coding: utf-8 -*-

from odoo import api,models
from odoo.exceptions import ValidationError, UserError


class ProjectTask(models.Model):
    """Creating a new model and its fields"""
    _inherit = "project.task"

    @api.constrains('user_ids')
    def _user_ids(self):
        if len(self.user_ids.ids) > 1:
            raise UserError("Only 1 Assignee can be selected")

    @api.onchange('timesheet_ids')
    def onchange_timesheet_ids(self):
        total_time_spent = 0
        hours_per_day = {}
        for line in self.timesheet_ids:
            if line.unit_amount > 0:
                key = (line.employee_id.id, str(line.date))
                per_day_hours = line.employee_id.resource_calendar_id.hours_per_day
                hours_per_day[key] = hours_per_day.get(key, 0) + line.unit_amount
                if hours_per_day[key] > per_day_hours:
                    raise ValidationError("Employee cannot work these many hours per day")
            total_time_spent += line.unit_amount
        if self.allocated_hours and total_time_spent > self.allocated_hours:
            raise ValidationError("Total time spent is more")
