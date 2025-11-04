# -*- coding: utf-8 -*-

from odoo import api,fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    partner_order_id = fields.Many2one('res.partner', related='order_id.partner_id', store=True, string='Customer')

class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    partner_order_id = fields.Many2one('res.partner', related='order_id.partner_id', store=True, string='Customer')
