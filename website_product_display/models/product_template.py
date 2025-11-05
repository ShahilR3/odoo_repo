# -*- coding: utf-8 -*-

from odoo import api,fields,models

class ProductTemplate(models.Model):
    """Inheriting the Model"""
    _inherit = "product.template"

    product_wh_qty = fields.Integer("Product Available", compute="_compute_product_wh_qty")

    @api.depends('product_variant_id')
    def _compute_product_wh_qty(self):
        """To compute the no.of products available"""
        website = self.env['website'].get_current_website()
        for template in self:
            if website.stock_loc_id:
                location = website.stock_loc_id
                product = template.product_variant_id
                template.product_wh_qty = template.env['stock.quant']._get_available_quantity(product, location)
            else:
                template.product_wh_qty = 0.0