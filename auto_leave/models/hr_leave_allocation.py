# -*- coding: utf-8 -*-

from datetime import date

from odoo import models


class HrLeaveAllocation(models.Model):
    _inherit = 'hr.leave.allocation'

    def _send_leave_notice(self):
        leaves = self.search([('date_to','=',date.today()),('state','=','validate')])
        for record in leaves:
            if record.remaining_leaves > 1:
                self.env.ref('auto_leave.leave_mail_template').send_mail(record.id, force_send=True)
