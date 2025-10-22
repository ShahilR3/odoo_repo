# -*-coding: utf-8 -*-

from odoo import api,fields, models


class ProjectTemplateTask(models.Model):
    """Creating a new model and its fields"""
    _name = "project.template.task"

    name = fields.Char()
    project_id = fields.Many2one('project.project', string="Project name")
    milestone_id = fields.Many2one('project.milestone', string="milestone")
    parent_id = fields.Many2one('project.template.task', string='Parent Task', index=True, tracking=True)
    child_ids = fields.One2many('project.template.task', 'parent_id', string="Sub-tasks")
    user_ids = fields.Many2many('res.users', string="Assignees")
    tag_ids = fields.Many2many('project.tags', string="Tags")
    partner_id = fields.Many2one('res.partner', string="Customer")
    date_deadline = fields.Datetime(string="Deadline")
    description = fields.Html(string='Description', sanitize_attributes=False)

    def action_create_task(self):
        create_task = self.env['project.task'].create({
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
                rec.env['project.task'].create({
                    'name': rec.name,
                    'project_id': rec.project_id.id,
                    'parent_id': create_task.id,
                })
        return {
            'type': 'ir.actions.act_window',
            "name": "Project Task",
            "res_model": "project.task",
            "res_id": create_task.id,
            "view_mode": "form",
            "target": 'current'
        }
