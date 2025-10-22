# -*- coding: utf-8 -*-

from odoo import models


class ProjectProject(models.Model):
    """Class for inheriting the model and then to perform certain actions"""
    _inherit = "project.project"

    def action_create_proj_template(self):
        """Button actions that can create a new project template"""
        create_temp = self.env['project.template'].create({
            'name': self.name,
            'label_tasks':self.label_tasks,
            'partner_id':self.partner_id.id,
            'company_id':self.company_id.id,
            'user_id': self.user_id.id,
            'tags_ids': self.tag_ids,
            'active':self.active,
            'date_start':self.date_start,
            'date_end':self.date,
            'description':self.description,
        })
        return{
            'type': 'ir.actions.act_window',
            'name': 'Project Template',
            'view_mode':'form',
            'res_model': 'project.template',
            'res_id': create_temp.id,
            'target': 'current',
        }

class ProjectProject(models.Model):
    """Class for inheriting the model and then to perform certain actions"""
    _inherit = "project.task"

    def action_create_task_template(self):
        """Button actions that can create a new task template"""
        create_task = self.env['project.template.task'].create({
            "name": self.name,
            "project_id": self.project_id.id,
            "milestone_id": self.milestone_id.id,
            "user_ids": self.user_ids.ids,
            "tag_ids": self.tag_ids.ids,
            "partner_id": self.partner_id.id,
            "date_deadline": self.date_deadline,
        })
        if self.child_ids:
            for rec in self.child_ids:
                subtask_vals = {
                    'name': rec.name,
                    'partner_id': rec.partner_id.id,
                    'milestone_id': rec.milestone_id.id,
                    'user_ids': rec.user_ids.ids,
                    'date_deadline': rec.date_deadline,
                    'tag_ids': rec.tag_ids,
                    'project_id': rec.project_id.id,
                    'parent_id': create_task.id,
                }
                rec.env['project.template.task'].create(subtask_vals)
        return {
            'type': 'ir.actions.act_window',
            "name": "Project Task",
            "res_model": "project.template.task",
            "res_id": create_task.id,
            "view_mode": "form",
            "target": 'current'
        }
