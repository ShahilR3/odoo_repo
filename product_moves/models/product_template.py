#-*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta

from odoo import models, fields

class PurchaseOrder(models.Model):
    _inherit = "product.template"

    product_move = fields.Integer("Product Moves", compute="_compute_product_moves")

    def _compute_product_moves(self):
        incoming_moves = self.env['stock.move.line'].search([
            ('product_id', '=', self.product_variant_id.id),
            ('state', '=', 'done'),
            ('picking_code', 'in', ['incoming','outgoing']),
            ('date', '>=', fields.Datetime.now() - relativedelta(days=7))
        ])
        for product in self:
            product.product_move = len(incoming_moves)
