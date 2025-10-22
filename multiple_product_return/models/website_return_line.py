# -*- coding: utf-8 -*-

from odoo import fields, models


class WebsiteReturnLine(models.Model):
    """Creating Website Return Line with its required fields"""
    _name = "website.return.line"

    website_return_id = fields.Many2one('website.return','Website Return')
    product_id = fields.Many2one('product.product', string='Product')
    delivered_qty = fields.Integer('Delivered Qty')
    return_qty = fields.Integer('Return Qty')
    reason = fields.Char(string="Reason")
