# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.fields import Command

class WebsiteReturn(models.Model):
    """Creating Website Return with its required fields"""
    _name = "website.return"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    name = fields.Char(readonly=True, default='New', copy=False)
    sale_order_id = fields.Many2one('sale.order', string='Sale Order', readonly=True)
    partner_id = fields.Many2one('res.partner','Customer', readonly=True)
    picking_type_id = fields.Many2one('stock.picking.type','Deliver To', required=True,
                                      default=lambda self: self._default_picking_type(),
                                      domain="['|', ('warehouse_id', '=', False), ('warehouse_id.company_id', '=', company_id)]")
    create_date = fields.Datetime(string="Create Date", readonly=True)
    user_id = fields.Many2one('res.users','Responsible', readonly=True)
    state = fields.Selection(selection=[('draft','Draft'),
                                        ('return','Return')], default='draft')
    order_line_ids = fields.One2many('website.return.line', 'website_return_id',
                                     string='Products', readonly=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)

    @api.model
    def _default_picking_type(self):
        return self._get_picking_type(self.env.context.get('company_id') or self.env.company.id)

    @api.model
    def _get_picking_type(self, company_id):
        picking_type = self.env['stock.picking.type'].search(
            [('code', '=', 'incoming'), ('warehouse_id.company_id', '=', company_id)])
        if not picking_type:
            picking_type = self.env['stock.picking.type'].search(
                [('code', '=', 'incoming'), ('warehouse_id', '=', False)])
        if not picking_type:
            picking_type = self.env['stock.picking.type'].with_context(active_test=False).search(
                [('code', '=', 'incoming'), ('warehouse_id', '=', False)])
        return picking_type[:1]

    @api.model_create_multi
    def create(self, vals_list):
        """ Create a sequence for the model """
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('website.return')
        return super().create(vals_list)

    def action_confirm(self):
        """ To Confirm Recieving the Stock"""
        self.write({'state': 'return'})

    def action_view_picking(self):
        """Always return the form view for pickings (open existing or new one)."""
        pickings = self.env['stock.picking'].search([('origin', '=', self.name)], limit=1)
        if pickings:
            return {
                'name': "Stock Return",
                'view_mode': 'form',
                'res_model': 'stock.picking',
                'res_id': pickings.id,
                'type': 'ir.actions.act_window',
                'target': 'current',
            }
        orderline = []
        for line in self.order_line_ids:
            orderline.append(Command.create({
                'product_id': line.product_id.id,
                'product_uom_qty': line.return_qty,
                'name': line.product_id.display_name,
                'product_uom': line.product_id.uom_id.id,
            }))
        picking = self.env['stock.picking'].create({
            'partner_id': self.partner_id.id,
            'picking_type_id': self.picking_type_id.id,
            'location_id': self.partner_id.property_stock_customer.id,
            'location_dest_id': self.picking_type_id.default_location_dest_id.id,
            'origin': self.name,
            'move_ids': orderline,
        })
        return {
            'name': "Stock Return",
            'view_mode': 'form',
            'res_model': 'stock.picking',
            'res_id': picking.id,
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
