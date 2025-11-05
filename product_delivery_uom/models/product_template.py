#-*- coding: utf-8 -*-

from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_uom_id = fields.Many2one("uom.uom", "Deliver UOM", domain="[('category_id','=',uom_category_id)]")
