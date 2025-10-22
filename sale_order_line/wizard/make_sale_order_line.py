#-*- coding: utf-8 -*-

from odoo import api,fields, models
from odoo.fields import Command


class MakePropertyRentLease(models.TransientModel):
    """Creating a Wizard Model for Report"""
    _name = "make.sale.order.line"
    _description = "Sale order line wizard"

    partner_id = fields.Many2one('res.partner', string='partner', required=True)
    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist')
    sale_order_lines = fields.Many2many('sale.order.line', string='Selected Sale Order Lines')

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        """For setting values with respect to partner"""
        if self.partner_id:
            self.pricelist_id = self.partner_id.property_product_pricelist
        else:
            self.pricelist_id = "False"

    @api.model
    def default_get(self, fields_list):
        """To set the sale order lines as same as the selected ones"""
        res = super().default_get(fields_list)
        active_ids = self.env.context.get('active_ids', [])
        if 'sale_order_lines' in fields_list and active_ids:
            res['sale_order_lines'] = [Command.set(active_ids)]
        return res

    def action_create_sale_order(self):
        """Creating a sale order"""
        sale_order = self.env['sale.order'].create({
            'partner_id': self.partner_id.id,
            'pricelist_id': self.pricelist_id.id,
            'invoice_status': 'no',
        })
        for line in self.sale_order_lines:
            self.env['sale.order.line'].create({
                'order_id': sale_order.id,
                'product_id': line.product_id.id,
                'product_uom_qty': line.product_uom_qty,
                'price_unit': line.price_unit,
            })
        return sale_order
