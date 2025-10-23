#-*- coding: utf-8 -*-

from odoo import fields,models

class CrmCommissionAchievements(models.Model):
    _name = "crm.commission.achievements"

    product_id = fields.Many2one('product.product', string="Product")
    product_categ_id = fields.Many2one(related='product_id.categ_id', string="Product Category")
    rate = fields.Float(string='Rate', store=True)
    max_commission_amount = fields.Integer("Max Commission")
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id', string="Currency")
    commission_id = fields.Many2one('crm.commission')
