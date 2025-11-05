# -*- coding: utf-8 -*-

from odoo import api, models


class StockRule(models.Model):
    _inherit = "stock.rule"

    @api.model
    def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, company_id, values):
        move_values = super()._get_stock_move_values(product_id, product_qty, product_uom, location_id, name, origin, company_id, values)
        uom = self.env['sale.order.line'].browse(move_values['sale_line_id']).order_id.uom
        if uom == True:
            default_uom = product_id.product_uom_id
            if product_uom and product_uom != default_uom:
                converted_qty = product_uom._compute_quantity(product_qty, default_uom)
                move_values['product_uom_qty'] = converted_qty
                move_values['product_uom'] = default_uom.id
        return move_values
