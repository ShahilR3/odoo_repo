#-*- coding: utf-8 -*-

from odoo import models
from odoo.fields import Command


class AccountMove(models.Model):
    _inherit = "account.move"

    def action_create_sale_order_bill(self):
        """Creating a Sale order"""
        for move in self:
            order_lines = []
            for line in move.invoice_line_ids:
                sale_order = Command.create({
                    'product_id': line.product_id.id,
                    'name': line.name,
                    'product_uom_qty': line.quantity,
                    'price_unit': line.price_unit,
                    'price_subtotal': line.price_subtotal,
                })
                order_lines.append(sale_order)
        sale = self.env['sale.order'].create({
            'partner_id':self.partner_id.id,
            'date_order':self.invoice_date,
            'order_line': order_lines,
            'invoice_ids': [Command.link(move.ids)]
        })
        sale.invoice_origin = self.name
        for line in self.invoice_line_ids:
            so_line = sale.order_line.filtered(lambda l: l.product_id == line.product_id)
            if so_line:
                line.sale_line_ids = [Command.set(so_line.ids)]
        return{
            'name': "Sale Order",
            'view_mode': 'form',
            'res_model': 'sale.order',
            'res_id': sale.id,
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
