#-*- coding: utf-8 -*-

from odoo import models, fields
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    uom = fields.Boolean(string='UOM Convert')

    def action_confirm(self):
        res = super().action_confirm()
        if self.uom and not self.order_line.product_id.product_uom_id:
            raise ValidationError("Select Delivery UOM in product")
        return res
