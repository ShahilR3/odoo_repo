# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo.fields import Command


class AccountMove(models.Model):
    _inherit = 'account.move'

    location_source_id = fields.Many2one('stock.location', string="Source Location",)
    location_dest_id = fields.Many2one('stock.location', string="Destination Location")

    def action_view_stock_moves(self):
        """Return action to view related stock pickings"""
        self.ensure_one()
        picking_type = self.env['stock.picking.type'].search([
            ('code', '=', 'outgoing'),
            ('warehouse_id.company_id', '=', self.company_id.id),
        ], limit=1)
        move_lines = []
        for line in self.invoice_line_ids:
            move_lines.append(Command.create({
                'product_id': line.product_id.id,
                'product_uom_qty': line.quantity,
                'name': line.product_id.display_name,
                'product_uom': line.product_uom_id.id,
                'picking_type_id': picking_type.id,
                'location_id': self.location_source_id.id,
                'location_dest_id': self.location_dest_id.id,
            }))
        picking = self.env['stock.picking'].create({
            'partner_id': self.partner_id.id,
            'picking_type_id': picking_type.id,
            'location_id': self.location_source_id.id,
            'location_dest_id': self.location_dest_id.id,
            'origin': self.name,
            'move_ids': move_lines,
            'move_type':'direct',
        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Delivery Orders',
            'view_mode': 'form',
            'res_model': 'stock.picking',
            'res_id': picking.id,
            'domain': [('origin', '=', self.name)],
        }
