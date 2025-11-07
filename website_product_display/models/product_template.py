# -*- coding: utf-8 -*-

from odoo import fields,models

class ProductTemplate(models.Model):
    """Inheriting the Model"""
    _inherit = "product.template"

    product_wh_qty = fields.Integer("Product Available", compute="_compute_product_wh_qty")

    def _compute_product_wh_qty(self):
        """To compute the no.of products available"""
        stock_loc_id_param = self.env['ir.config_parameter'].sudo().get_param('website_product_display.stock_loc_id')
        stock_loc_id = self.env['stock.location'].browse(int(stock_loc_id_param)) if stock_loc_id_param else False
        for template in self:
            template.product_wh_qty = template.env['stock.quant']._get_available_quantity(
                    template.product_variant_id, stock_loc_id) if stock_loc_id else 0
