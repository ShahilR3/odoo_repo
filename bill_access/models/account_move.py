#-*- coding: utf-8 -*-

from odoo import models,fields
from odoo.fields import Command

class AccountMove(models.Model):
    _inherit = "account.move"

    def action_create_purchase_order(self):
        """Create a Purchase Order from the current Vendor Bill"""
        for move in self:
            if move.move_type != 'in_invoice':
                continue
            order_lines = []
            for line in move.invoice_line_ids:
                line_name = line.name or line.product_id.display_name or 'No description'
                order_lines.append(Command.create({
                    'product_id': line.product_id.id,
                    'name': line_name,
                    'product_qty': line.quantity,
                    'price_unit': line.price_unit,
                    'date_planned': fields.Date.today(),
                }))
            purchase = self.env['purchase.order'].create({
                'partner_id': move.partner_id.id,
                'date_order': move.invoice_date or fields.Date.today(),
                'order_line': order_lines,
                'invoice_ids': [Command.link(move.id)]
            })
            move.purchase_id = purchase.id
            for line in move.invoice_line_ids:
                po_line = purchase.order_line.filtered(lambda l: l.product_id == line.product_id)
                if po_line:
                    line.purchase_line_id = po_line[0].id
            return {
                'name': "Purchase Order",
                'view_mode': 'form',
                'res_model': 'purchase.order',
                'res_id': purchase.id,
                'type': 'ir.actions.act_window',
                'target': 'current',
            }
