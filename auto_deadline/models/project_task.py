# -*-coding: utf-8 -*-

from datetime import timedelta

from odoo import api,fields,models
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):
    """Inheriting a model and its fields"""
    _inherit = "project.task"

    @api.onchange('allocated_hours')
    def deadline(self):
        """Calculating the deadline"""
        if len(self.user_ids) > 1:
            raise ValidationError("Only one Assignee")
        else:
            for task in self:
                working_days = task.allocated_hours / 8.0
                start_date = fields.Date.from_string(task.date_assign.date())
                current_date = start_date
                added_days = 0
                while added_days < working_days:
                    current_date += timedelta(days=1)
                    if current_date.weekday() < 5:
                        added_days += 1
                task.date_deadline = fields.Datetime.to_string(current_date)
