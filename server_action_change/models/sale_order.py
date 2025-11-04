# -*- coding: utf-8 -*-

from odoo import models


class SaleState(models.Model):
    """New states for delivery status"""
    _inherit = "sale.order"

    def action_unit_to_dozen(self):
        dozen_uom = self.env['uom.uom'].search([('name', '=', 'Dozens')], limit=1)
        sale_order_lines = self.env['sale.order.line'].search([
            ('product_uom.name', '=', 'Units'),
            ('state', '=', 'draft')
        ])
        if sale_order_lines:
            sale_order_lines.write({'product_uom': dozen_uom.id})
