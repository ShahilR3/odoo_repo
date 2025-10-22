# -*- coding: utf-8 -*-

from odoo import api, fields, models

class CrmCommission(models.Model):
    """Creating a new model and its functions"""
    _name = "crm.commission"
    _description = "Commissions in crm"

    name = fields.Char("Commission Name")
    active = fields.Boolean(default=True)
    start_date = fields.Date("From Date")
    end_date = fields.Date("To Date")
    type = fields.Selection(selection=[('product', 'Product Wise'),
                                       ('revenue', 'Revenue Wise')])
    rev_type = fields.Selection(selection=([('straight', 'Straight Commission'),
                                            ('graduate', 'Graduated Commission')]), default='straight')
    rate = fields.Float(sting="Rate")
    user_id = fields.Many2one('res.users',string="Salesperson")
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id', string="Currency")
    achievement_ids = fields.One2many('crm.commission.achievements','commission_id')
    revenue_ids = fields.One2many('crm.commission.revenue','commission_id')
    commission_amount = fields.Float(readonly=True, compute="_compute_commission_amount")

    @api.onchange('revenue_ids')
    def _onchange_revenue_ids(self):
        """Assign sequential numbers to each revenue line dynamically."""
        for index, line in enumerate(self.revenue_ids, start=1):
            line.sequence_number = index

    @api.depends('rev_type')
    def _compute_commission_amount(self):
        """Calculations for the commission"""
        for rec in self:
            so = rec.env['sale.order'].search([('user_id', '=', rec.user_id.id)], limit=1)
            total_amount = so.amount_total
            if rec.rev_type == 'straight':
                rec.commission_amount = total_amount * rec.rate
            else:
                rec.commission_amount = 0
                for range in rec.revenue_ids:
                    rate = range.rate
                    to_amount = range.to_amount
                    from_amount = range.from_amount
                    range = to_amount-from_amount
                    if total_amount > range:
                        rate_val = range * rate
                        total_amount = total_amount - range
                        rec.commission_amount += rate_val
                    else:
                        rec.commission_amount += total_amount * rate
                        break
                if total_amount > 0:
                    rec.commission_amount += total_amount * rec.revenue_ids[-1].rate
