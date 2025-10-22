# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PropertyIntermediate(models.Model):
    """Creating an intermediatory model along with its fields"""
    _name = "property.intermediate"
    _description = "Intermediate model"

    name = fields.Char(related="intermediate_rent_id.name")
    days = fields.Integer(related="intermediate_rent_id.total_days")
    property_name = fields.Char(related='intermediate_management_id.name', store=True)
    date = fields.Date(related="intermediate_rent_id.start_date")
    intermediate_rent_id = fields.Many2one('property.rent.lease', string="Property Rent/Lease",
                                           ondelete="cascade")
    invoice_line_ids = fields.Many2many('account.move.line', string="Invoice Line")
    intermediate_management_id = fields.Many2one('property.properties', string="Property Name",
                                                 ondelete='cascade')
    partner_id = fields.Many2one(related='intermediate_rent_id.tenant_id', string="Partner")
    owner_id = fields.Many2one(related='intermediate_management_id.owner_id', string="Owner Name", store=True)
    company_id = fields.Many2one('res.company',  # pylin disable:line-too-long
                                 string='Company name',
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one(related='company_id.currency_id', string="Currency")
    amount = fields.Monetary(string="Rent/lease", compute="_compute_amount", inverse="_inverse_amount", readonly=False,
                             store=True)
    total_amount = fields.Monetary(compute="_compute_total_amount", store=True)
    type = fields.Selection(string="Type", selection=[('rent', 'Rent'), ('lease', 'Lease')],
                            readonly=True, related="intermediate_rent_id.property_type")
    quantity = fields.Integer(string="Quantity")
    state = fields.Selection(related="intermediate_rent_id.state")
    invoiced_qty = fields.Float(string="Invoiced Qty", compute="_compute_invoiced_qty")

    @api.depends('intermediate_rent_id')
    def _compute_invoiced_qty(self):
        for rec in self:
            invoices = rec.intermediate_rent_id.invoice_ids.filtered(
                lambda inv: inv.state == 'posted' and inv.move_type == 'out_invoice'
            )
            lines = invoices.mapped('invoice_line_ids')
            matched_lines = [line for line in lines if line.property_line_id.id == rec.id]
            rec.invoiced_qty = sum(line.quantity for line in matched_lines)

    @api.depends('quantity', 'days', 'amount')
    def _compute_total_amount(self):
        """Calculating the total amount"""
        for record in self:
            record.total_amount = record.amount * record.days * record.quantity

    @api.depends('intermediate_management_id', 'type')
    def _compute_amount(self):
        """assigning the values for amount field"""
        for record in self:
            if record.type == 'rent':
                record.amount = record.intermediate_management_id.rent
            else:
                record.amount = record.intermediate_management_id.legal_amount

    def _inverse_amount(self):
        """Amount changes in Property model"""
        for record in self:
            if record.intermediate_management_id:
                if record.type == 'rent':
                    record.intermediate_management_id.rent = record.amount
                else:
                    record.intermediate_management_id.legal_amount = record.amount
