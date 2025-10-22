"""Inheriting the Sale order and Sale order line model"""
# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo.exceptions import UserError
from odoo.fields import Command


class SaleOrder(models.Model):
    """Adding new actions inside Sale order model"""
    _inherit = "sale.order"

    vanish = fields.Boolean(compute="_compute_vanish")

    def _compute_vanish(self):
        """for switching the buttons"""
        self.vanish = bool(self.env['project.project'].search([('name', '=', self.name)], limit=1))

    def get_milestones(self):
        """To get the milestones"""
        milestone_groups = {}
        for line in self.order_line:
            if line.milestone <= 0:
                raise UserError("Please Enter the milestone value")
            if line.milestone and line.milestone not in milestone_groups:
                milestone_groups[line.milestone] = []
            milestone_groups[line.milestone].append(line)
        return milestone_groups

    def action_project(self):
        """To create a project for the sale order"""
        milestone_groups = self.get_milestones()
        project = self.env['project.project'].create({
            'name': self.name,
            'label_tasks': 'Milestone',
        })
        self.env['project.task.type'].create({
            'name': 'New',
            'project_ids': [Command.link(project.id)],
        })
        for milestone, lines in milestone_groups.items():
            parent_task = self.env['project.task'].create({
                'name': f"Milestone {milestone}",
                'project_id': project.id,
            })
            for line in lines:
                subtask_name = f"Milestone {milestone} - {line.product_id.name}"
                subtask_vals = {
                    'name': subtask_name,
                    'project_id': project.id,
                    'parent_id': parent_task.id,
                }
                self.env['project.task'].create(subtask_vals)
        return {
            'name': 'Project Form',
            'type': 'ir.actions.act_window',
            'res_id': project.id,
            'res_model': 'project.project',
            'view_mode': 'form',
            'target': 'current',
        }

    def action_update(self):
        """Updating the project"""
        milestone_groups = self.get_milestones()
        existing_projects = self.env['project.project'].search([('name', '=', self.name)])
        if existing_projects :
            milestone_value = []
            existing_milestone = self.env['project.task'].search([
                ('project_id','=', existing_projects.id),
                ('parent_id','=', False)])
            milestone_value = ((int(task.name.replace("Milestone ", "").strip())) for task in existing_milestone)
            for milestone, lines in milestone_groups.items():
                parent_task = self.env['project.task'].search([
                    ('project_id', '=', existing_projects.id),
                    ('name', '=', f"Milestone {milestone}"),
                    ('parent_id', '=', False)
                ], limit=1)
                if not parent_task:
                    parent_task = self.env['project.task'].create({
                        'name': f"Milestone {milestone}",
                        'project_id': existing_projects.id,
                    })
                for line in lines:
                    subtask_name = f"Milestone {milestone} - {line.product_id.name}"
                    existing_subtask = self.env['project.task'].search([
                        ('project_id', '=', existing_projects.id),
                        ('parent_id', '=', parent_task.id),
                        ('name', '=', subtask_name)
                    ])
                    if not existing_subtask:
                        self.env['project.task'].create({
                            'name': subtask_name,
                            'project_id': existing_projects.id,
                            'parent_id': parent_task.id,
                        })
            missing_milestone = set(milestone_value) - set(milestone_groups.keys())
            for value in missing_milestone:
                parent_task = self.env['project.task'].search([
                    ('project_id', '=', existing_projects.id),
                    ('name', '=', f"Milestone {value}"),
                ], limit=1)
                parent_task.write({'active': False})
        return {
            'name': 'Project Form',
            'type': 'ir.actions.act_window',
            'res_id': existing_projects.id,
            'res_model': 'project.project',
            'view_mode': 'form',
            'target': 'current',
        }

    def action_view_project(self):
        """Stat button view"""
        self.ensure_one()
        project = self.env['project.project'].search([('name', '=', self.name)], limit=1)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Project Form',
            'view_mode': 'form',
            'res_model': 'project.project',
            'res_id': project.id,
            'target': 'current',
            'context': {'create': False},
        }


class SaleOrderLine(models.Model):
    """Adding new field to the inherited model"""
    _inherit = 'sale.order.line'

    milestone = fields.Integer(string="Milestone")
