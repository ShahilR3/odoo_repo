#-*- coding:utf-8 -*-

from odoo import models


class SaleOrder(models.Model):
    """Inheriting the Sale Order for performing the calculation"""
    _inherit = 'sale.order'

    def action_confirm(self):
        """Calculation for commission"""
        res = super(SaleOrder, self).action_confirm()
        commission_rule = self.env['crm.commission'].search([('user_id', '=', self.user_id.id)])
        if commission_rule:
            commission_rule._compute_commission_amount()
        return res

    def action_cancel(self):
        """Re-calculate commission and update crm.commission"""
        res = super(SaleOrder, self).action_cancel()
        for order in self:
            commission_rule = self.env['crm.commission'].search([('user_id', '=', order.user_id.id),('sale_order_ids','in',self.id)])
            if commission_rule:
                commission_rule._compute_commission_amount()
        return res
