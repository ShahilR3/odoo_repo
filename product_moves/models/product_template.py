#-*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta

from odoo import api, models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_move = fields.Integer("Product Moves", compute="_compute_product_moves")
    stock_value = fields.Float("Stock Value", compute="_compute_stock_move", store=True)

    def _compute_product_moves(self):
        incoming_moves = self.env['stock.move.line'].search([
            ('product_id', '=', self.product_variant_id.id),
            ('state', '=', 'done'),
            ('picking_code', 'in', ['incoming','outgoing']),
            ('date', '>=', fields.Datetime.now() - relativedelta(days=7))
        ])
        for product in self:
            product.product_move = len(incoming_moves)

    # @api.depends('standard_price')
    def _compute_stock_move(self):
        print("ABC")
        for rec in self:
            rec.stock_value = rec.standard_price * rec.qty_available
