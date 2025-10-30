#-*- coding: utf-8 -*-

from odoo import api,models,fields
from odoo.fields import Command

class AccountMove(models.Model):
    _inherit = "account.move"

    existing_invoice_line_ids = fields.One2many('account.move.line','move_id',
                                                "Previous Invoice Lines", compute="_compute_line_ids")

    @api.depends('partner_id')
    def _compute_line_ids(self):
        """To fetch the existing invoice lines"""
        for rec in self:
            invoices = self.env['account.move'].search([
                ('partner_id', '=', rec.partner_id.id),
                ('move_type', '=', 'out_invoice'),
                ('state', '=', 'posted')
            ])
            invoice_lines = self.env['account.move.line'].search([
                ('product_id','!=',None),
                ('move_id', 'in', invoices.ids),
            ])
            rec.existing_invoice_line_ids = [Command.set(invoice_lines.ids)]

    def action_open_existing_invoices(self):
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

