# -*- coding: utf-8 -*-

from odoo import fields, models


class ResPartner(models.Model):
    """Adding new field to the inherited model"""
    _inherit = "project.project"

    project_percent = fields.Integer(compute="_compute_project_perc", string='Project Percent')

    def _compute_project_perc(self):
        """Calculating the percentage of project"""
        for rec in self:
            rec.project_percent = (rec.closed_task_count / rec.task_count) * 100
