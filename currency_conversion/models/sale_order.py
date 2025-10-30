# -*- coding: utf-8 -*-

from odoo import api,fields, models


class SaleOrder(models.Model):
    """Adding new actions inside Sale order model"""
    _inherit = "sale.order"

    currency_select_id = fields.Many2one('res.currency',"Choose Currency",
                                          domain=lambda self: [('id', '!=', self.pricelist_id.currency_id.id)])
    currency_convert_amount = fields.Float(string="Currency conversion", compute="_compute_currency_convert_amount")

    @api.depends('currency_select_id')
    def _compute_currency_convert_amount(self):
        """To convert the values into selected currency field"""
        for rec in self:
            date = fields.Date.today()
            rec.currency_convert_amount = rec.currency_id._convert(rec.amount_total, rec.currency_select_id, rec.company_id, date)
            # amount = rec.currency_display_id.rate /rec.currency_id.rate
            # rec.currency_convert_amount = rec.amount_total * amount
