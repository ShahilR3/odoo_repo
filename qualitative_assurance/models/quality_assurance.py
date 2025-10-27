# -*- coding: utf-8 -*-

from odoo import fields, models

class QualityAssurance(models.Model):
    _name = "quality.assurance"
    _description = "Quality Assurance"

    name = fields.Char()
    product_id = fields.Many2one("product.product", string="Products", required=True)
    type = fields.Selection(selection=([('quality', 'Quality'),
                                        ('quantity','Quantity')]),string="Test Type", required=True)
    quality_line_ids = fields.One2many('quality.assurance.line','quality_assurance_id',
                                    string="Trigger On")
