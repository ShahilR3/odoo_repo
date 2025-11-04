# -*- coding: utf-8 -*-

from datetime import date

from odoo import models


class HrLeaveAllocation(models.Model):
    _inherit = 'hr.leave.allocation'

    def action_send_mail_for_leave(self):
        leaves = self.search([('date_to','=',date.today()),('state','=','validate')])
        employees = self.env['hr.employee'].search([])
        for record in leaves:
            for employee in employees:
                if employee.work_email and (record.max_leaves - record.leaves_taken) > 1:
                    self.env.ref('auto_leave.leave_mail_template').send_mail(record.id, force_send=True)
