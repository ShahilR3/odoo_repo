# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.fields import Command


class ResPartner(models.Model):
    _inherit = "res.partner"

    # product_id = fields.Many2one('product.product','Products')
    # sale_order_line_ids = fields.One2many('sale.order.line', 'partner_order_id',
    #                                       compute='compute_sale_order_line_ids', store=True)
    # purchase_order_line_ids = fields.One2many('purchase.order.line','partner_order_id',
    #                                           compute='compute_purchase_order_line_ids', store=True)
    # sale_quantity = fields.Float("Total Sale quantity", compute="compute_sale_quantity")
    # purchase_quantity = fields.Float("Total Purchase Quantity", compute="_compute_purchase_quantity")
    # tax_ids = fields.Many2many('account.tax', string='Taxes')
    # price = fields.Float("Price")
    # tax_price = fields.Float("Tax Price",compute='compute_tax')
    qty = fields.Float("Quantity")
    uom_id = fields.Many2one('uom.uom', string='Source UoM', required=True)
    uom_category_id = fields.Many2one('uom.category', string='UoM Category', related='uom_id.category_id',
                                      store=True)
    target_uom_id = fields.Many2one('uom.uom', string='Target UoM', domain="[('category_id', '=', uom_category_id)]")
    computed = fields.Float(string='Converted Quantity', compute='_compute_converted_qty')

    @api.depends('qty', 'uom_id', 'target_uom_id')
    def _compute_converted_qty(self):
        for rec in self:
            if rec.qty and rec.uom_id and rec.target_uom_id:
                rec.computed = rec.uom_id._compute_quantity(rec.qty, rec.target_uom_id)
            else:
                rec.computed = 0.0

    # @api.depends('product_id')
    # def compute_sale_order_line_ids(self):
    #     for rec in self:
    #         if rec.sale_order_ids and rec.product_id:
    #             rec.sale_order_line_ids = [Command.set(rec.sale_order_ids.mapped('order_line').filtered(lambda l: l.product_id == rec.product_id).ids)]
    #         else:
    #             rec.product_id = None
    #
    # @api.depends('product_id')
    # def compute_purchase_order_line_ids(self):
    #     for rec in self:
    #         if rec.purchase_line_ids and rec.product_id:
    #             rec.purchase_order_line_ids = [Command.set(rec.purchase_line_ids.filtered(lambda l: l.product_id == rec.product_id).ids)]
    #         else:
    #             rec.product_id = None
    #
    # def compute_sale_quantity(self):
    #     """Sale order line Quantity"""
    #     for partner in self:
    #         sale_order_line = partner.sale_order_ids.mapped('order_line')
    #         partner.write({'sale_quantity':sum(sale_order_line.mapped('product_uom_qty'))})
    #
    # def _compute_purchase_quantity(self):
    #     """Purchase order line quantity"""
    #     for rec in self:
    #         rec.write({'purchase_quantity': sum(rec.purchase_line_ids.mapped('product_qty'))})
    #
    # @api.depends('tax_ids','price')
    # def compute_tax(self):
    #     for rec in self:
    #         rec.write({'tax_price': rec.tax_ids.compute_all(rec.price)['total_included']})
