# -*- coding: utf-8 -*-
from odoo import models, fields
from odoo.fields import Command

class ExistingInvoiceLine(models.Model):
    _name = 'existing.invoice.line'
    _description = 'Existing Invoice Line Reference'

    existing_move_id = fields.Many2one('account.move', string='Parent Invoice', ondelete='cascade')
    original_line_id = fields.Many2one('account.move.line', string='Original Invoice Line', readonly=True)
    product_id = fields.Many2one(related='original_line_id.product_id', store=False, readonly=True)
    quantity = fields.Float(related='original_line_id.quantity', store=False, readonly=True)
    product_uom_id = fields.Many2one(related='original_line_id.product_uom_id', store=False, readonly=True)
    price_unit = fields.Float(related='original_line_id.price_unit', store=False, readonly=True)
    tax_ids = fields.Many2many(related='original_line_id.tax_ids', store=False, readonly=True)
    price_subtotal = fields.Monetary(related='original_line_id.price_subtotal', store=False, readonly=True)
    currency_id = fields.Many2one(related='original_line_id.currency_id', store=False, readonly=True)

    def action_add_to_line(self):
        """Add the selected existing invoice line to the current invoice and remove it from existing_invoice_line"""
        invoice = self.existing_move_id
        new_line = self.env['account.move.line'].create({
            'move_id': invoice.id,
            'product_id': self.product_id.id,
            'quantity': self.quantity,
            'product_uom_id': self.product_uom_id.id,
            'price_unit': self.price_unit,
            'tax_ids': [Command.set(self.tax_ids.ids)],
            'price_subtotal': self.price_subtotal,
        })
        invoice.invoice_line_ids = new_line
        self.unlink()
