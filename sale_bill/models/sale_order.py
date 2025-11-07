#-*- coding: utf-8 -*-

from odoo import models
from odoo.fields import Command


class AccountMove(models.Model):
    _inherit = "sale.order"

    def new_invoice(self):
        """Creating a Sale order"""
        sale_adv = self.env['sale.advance.payment.inv'].create({
            'advance_payment_method':'delivered',
            'sale_order_ids':[Command.link(self.id)]
        })
        sale_adv.create_invoice()