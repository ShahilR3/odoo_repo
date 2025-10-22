# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        if self.partner_id.sales_date:
            previous = (fields.Datetime.now() - self.partner_id.sales_date).days
            print("previous", previous)
            if previous > 90:
                raise ValidationError("Cannot Confirm")
        res =super().action_confirm()
        self.date_order = self.date_order
        self.partner_id.sales_date = self.date_order
        return res
