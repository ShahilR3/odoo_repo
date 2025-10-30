#-*- coding: utf-8 -*-

from odoo import models
from odoo.fields import Command

class AccountMove(models.Model):
    _inherit = "account.move.line"

    def action_add_to_line(self):
        """To add the selected existing invoice line to the current invoice line"""
        active_invoice = self.env.context.get('active_id')
        invoice = self.env['account.move'].search([('id','=',active_invoice)])
        order=[]
        order.append(Command.create({
            'move_id': invoice.id,
            'product_id': self.product_id.id,
            'quantity': self.quantity,
            'product_uom_id': self.product_uom_id.id,
            'price_unit': self.price_unit,
            'tax_ids': self.tax_ids.ids,
            'price_subtotal': self.price_subtotal,}))
        invoice.invoice_line_ids = order
