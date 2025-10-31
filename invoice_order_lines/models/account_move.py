#-*- coding: utf-8 -*-

from odoo import api,models,fields
from odoo.fields import Command

class AccountMove(models.Model):
    _inherit = "account.move"

    existing_invoice_line_ids = fields.One2many('existing.invoice.line', 'existing_move_id',
                                                "Previous Invoice Lines", compute="_compute_line_ids", store="True")

    @api.depends('partner_id')
    def _compute_line_ids(self):
        """To fetch the existing invoice lines"""
        for rec in self:
            invoice_lines = self.env['account.move.line'].search([
                ('product_id', '!=', False),
                ('move_id.partner_id', '=', rec.partner_id.id),
                ('move_id.move_type', '=', 'out_invoice'),
                ('move_id.state', '=', 'posted'),
            ], limit=20)
            new_lines = []
            for line in invoice_lines:
                new_lines.append(Command.create({
                    'product_id': line.product_id.id,
                    'quantity': line.quantity,
                    'price_unit': line.price_unit,
                    'product_uom_id': line.product_uom_id.id,
                    'tax_ids': line.tax_ids.ids,
                    'price_subtotal': line.price_subtotal,
                    'existing_move_id': line.move_id.id,
                    'original_line_id': line.id,
                }))
            if rec.existing_invoice_line_ids:
                rec.existing_invoice_line_ids.unlink()
            rec.existing_invoice_line_ids = new_lines

    def action_add_existing_invoices(self):
        """To add all the existing invoice lines to current invoice line"""
        order=[]
        for line in self.existing_invoice_line_ids:
            order.append(Command.create({
                'move_id': self.id,
                'product_id': line.product_id.id,
                'quantity': line.quantity,
                'product_uom_id': line.product_uom_id.id,
                'price_unit': line.price_unit,
                'tax_ids': line.tax_ids.ids,
                'price_subtotal': line.price_subtotal,
            })
            )
        self.invoice_line_ids = order
        self.existing_invoice_line_ids.unlink()
