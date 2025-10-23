#-*- coding: utf-8 -*-

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_visible = fields.Boolean(string="Hide Out of Stock Products From Website",
                                     default=True)
