#-*- coding: utf-8 -*-

from odoo import fields,models

class CrmCommissionAchievements(models.Model):
    _name = "crm.commission.achievements"

    product_id = fields.Many2one('product.product', string="Product")
    product_categ_id = fields.Many2one(related='product_id.categ_id', string="Product Category")
    rate = fields.Float(string='Rate', store=True)
    max_commission_amount = fields.Integer("Max Commission")
    commission_id = fields.Many2one('crm.commission')
