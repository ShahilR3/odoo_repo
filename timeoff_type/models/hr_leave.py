# -*- coding: utf-8 -*-

from datetime import timedelta

from odoo import models
from odoo.exceptions import ValidationError

class StockMove(models.Model):
    _inherit = "hr.leave"

    def action_approve(self):
        previous_date = self.env['hr.leave'].search([('employee_id','=',self.employee_id.id),
                                                     ('holiday_status_id','=', self.holiday_status_id.id),
                                                     ('state','=','validate')],
                                                    order="request_date_to desc")
        print((self.request_date_from - previous_date.request_date_to))
        if (self.request_date_from - previous_date.request_date_to) < timedelta(days=30):
            raise ValidationError("Can only apply after 30 days from previous leave")
        else:
            res =super().action_approve()
            return res