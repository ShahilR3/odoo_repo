# -*- coding: utf-8 -*-

from odoo import api,fields,models
from odoo.exceptions import ValidationError
from odoo.fields import Command


class ProjectTemplate(models.Model):
    """Defining anew module and its fields"""
    _name = "project.template"

    name = fields.Char("Name", required=True, tracking=True)
    label_tasks = fields.Char(string="Name of the task")
    partner_id = fields.Many2one("res.partner",string="Customer")
    company_id = fields.Many2one('res.company', string="Company",
                                 default= lambda self: self.env.user.company_id.id)
    user_id = fields.Many2one('res.users', string='Project Manager',
                              default=lambda self: self.env.user, tracking=True)
    tags_ids = fields.Many2many('project.tags', string='Tags')
    active = fields.Boolean(default=True, copy=False, export_string_translation=False)
    date_start = fields.Date(required=True)
    date_end = fields.Date(required=True)
    description = fields.Html(string='Description', sanitize_attributes=False)
    task_count = fields.Integer(compute="_compute_task_count")

    @api.depends('name')
    def _compute_task_count(self):
        for rec in self:
            rec.task_count = rec.env['project.task'].search_count([('project_id.name', '=', self.name),
                                                                   ('parent_id', '=', False)])

    def action_get_property(self):
        return{
            'type': 'ir.actions.act_window',
            'name': 'Task',
            'res_model': 'project.task',
            'domain': [('project_id.name', '=', self.name),('parent_id', '=', False)],
            'view_mode': 'list,form',
            'target': 'current',
        }

    def action_project_create(self):
        """Providing an action for the button"""
        create_project = self.env['project.project'].create({
            'name': self.name,
            'label_tasks':self.label_tasks,
            'partner_id':self.partner_id.id,
            'company_id':self.company_id.id,
            'user_id': self.user_id.id,
            'tag_ids': self.tags_ids,
            'active':self.active,
            'date_start':self.date_start,
            'date':self.date_end,
            'description':self.description,
        })
        self.env['project.task.type'].create({
            'name': 'New',
            'project_ids': [Command.link(create_project.id)]
        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Project',
            'res_id': create_project.id,
            'res_model': 'project.project',
            'view_mode': 'form',
            'target': 'current',
        }
