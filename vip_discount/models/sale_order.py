# -*- coding: utf-8 -*-

from odoo import api, models


class SaleOrder(models.Model):
    """Adding new field to the inherited model"""
    _inherit = "sale.order.line"

    @api.depends('order_id.order_line', 'order_id.partner_id', 'order_id.partner_id.is_vip', 'order_id.partner_id.vip_discount')
    def _compute_discount(self):
        print("ABC")
        for order in self:
            if order.order_id.partner_id.is_vip:
                for line in order.order_id.order_line:
                    line.discount = order.order_id.partner_id.vip_discount
