# -*- coding: utf-8 -*-

from odoo import api, fields, models

class QualityAssurance(models.Model):
    _name = "quality.assurance"

    name = fields.Char()
    product_id = fields.Many2one("product.product", string="Products")
    type = fields.Selection(selection=([('quality', 'Quality'),
                                        ('quantity','Quantity')]),string="Test Type")
    quality_line_ids = fields.One2many('quality.assurance.line','quality_assurance_id',
                                    string="Trigger On")

