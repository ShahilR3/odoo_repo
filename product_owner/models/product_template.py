# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ProductTemplate(models.Model):
    """Inherits model product.template and adds new field to it"""
    _inherit = "product.template"

    product_owner_id = fields.Many2one("res.partner", string="Owner", store=True)


class ProductProduct(models.Model):
    """Inherits model product.product and adds new field to it"""
    _inherit = 'product.product'

    product_owner_id = fields.Many2one(related="product_tmpl_id.product_owner_id", store=True)

    @api.model
    def _load_pos_data_fields(self, config_id):
        fields = super()._load_pos_data_fields(config_id)
        fields.append('product_owner_id')
        return fields
