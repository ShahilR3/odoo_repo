# -*- coding: utf-8 -*-

from odoo import api, models, fields

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    state = fields.Selection(selection=[('onboard', 'Onboarding'),
                                        ('Offboard', 'Offboarding'),
                                        ], compute='_compute_state', store=True)

    @api.depends('resource_calendar_id')
    def _compute_state(self):
        """Set the state of employee"""
        for rec in self:
            if rec.resource_calendar_id:
                rec.write({'state': 'onboard'})
                if not rec.active:
                    rec.action_unarchive()
            else:
                rec.write({'state': 'Offboard'})
                rec.action_archive()
