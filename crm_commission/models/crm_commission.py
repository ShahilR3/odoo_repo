# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class CrmCommission(models.Model):
    """Creating a new model and its functions"""
    _name = "crm.commission"
    _description = "Commissions in crm"

    name = fields.Char("Commission Name")
    active = fields.Boolean(default=False)
    start_date = fields.Date("From Date")
    end_date = fields.Date("To Date")
    type = fields.Selection(selection=[('product', 'Product Wise'),
                                       ('revenue', 'Revenue Wise')])
    rev_type = fields.Selection(selection=([('straight', 'Straight Commission'),
                                            ('graduate', 'Graduated Commission')]), default='straight')
    rate = fields.Float(sting="Rate")
    user_id = fields.Many2one('res.users', string="Salesperson")
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id', string="Currency")
    achievement_ids = fields.One2many('crm.commission.achievements', 'commission_id')
    revenue_ids = fields.One2many('crm.commission.revenue', 'commission_id')
    commission_amount = fields.Float(compute="_compute_commission_amount", store=True)
    sale_order_ids = fields.Many2many('sale.order', string="Sale orders")

    @api.depends('user_id')
    def _compute_sale_order_id(self):
        self.sale_order_id = self.env['sale.order'].search([('user_id', '=', self.user_id.id)])

    @api.onchange('active', 'user_id')
    def _on_change_user_id(self):
        other_active = self.env['crm.commission'].search([('user_id', '=', self.user_id.id),
                                                          ('active', '=', 'True')])
        if other_active and self.active == True:
            raise ValidationError("Only one plan per Salesperson")

    @api.onchange('revenue_ids')
    def _onchange_revenue_ids(self):
        """Assign sequential numbers to each revenue line dynamically."""
        for index, line in enumerate(self.revenue_ids, start=1):
            line.sequence_number = index

    @api.depends('type', 'rev_type')
    def _compute_commission_amount(self):
        """Calculations for the commission for every sale order of the user"""
        for rec in self:
            sale_orders = rec.env['sale.order'].search([
                ('user_id', '=', rec.user_id.id),
                ('state', 'not in', ['cancel', 'draft'])
            ])
            rec.commission_amount = 0.0
            relevant_orders = rec.env['sale.order']
            for so in sale_orders:
                total_amount = so.amount_total
                order_used = False
                if rec.type == 'product':
                    for sol in so.order_line:
                        matching_product = rec.achievement_ids.filtered(
                            lambda a: a.product_id == sol.product_id)
                        if matching_product:
                            for mp in matching_product:
                                rec.commission_amount += sol.price_subtotal * mp.rate
                                order_used = True
                elif rec.rev_type == 'straight':
                    rec.commission_amount += total_amount * rec.rate
                    order_used = True
                else:
                    for range_line in rec.revenue_ids:
                        rate = range_line.rate
                        to_amount = range_line.to_amount
                        from_amount = range_line.from_amount
                        range_diff = to_amount - from_amount
                        if total_amount > range_diff:
                            rec.commission_amount += range_diff * rate
                            total_amount -= range_diff
                            order_used = True
                        else:
                            rec.commission_amount += total_amount * rate
                            order_used = True
                            break
                    if total_amount > 0 and rec.revenue_ids:
                        rec.commission_amount += total_amount * rec.revenue_ids[-1].rate
                        order_used = True
                if order_used:
                    relevant_orders |= so
            rec.sale_order_ids = relevant_orders