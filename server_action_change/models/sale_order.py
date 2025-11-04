# -*- coding: utf-8 -*-

from odoo import models


class SaleOrder(models.Model):
    """New states for delivery status"""
    _inherit = "sale.order"

    def action_unit_to_dozen(self):
        """Changing the uom of draft sale"""
        active_ids = self.env.context.get('active_ids', [])
        dozen_uom = self.env['uom.uom'].search([('name', '=', 'Dozens')], limit=1)
        unit_uom = self.env['uom.uom'].search([('name', '=', 'Units')], limit=1)
        sale_order_unit = self.env['sale.order'].browse(active_ids).mapped('order_line').filtered(lambda l:l.product_uom.id == unit_uom.id)
        if sale_order_unit:
            sale_order_unit.write({'product_uom': dozen_uom.id})
