#-*- coding: utf-8 -*-

from odoo import models, fields

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    sale_order_relate_id = fields.Many2one('sale.order', string='Sale order',
                                           domain=[('state', '!=', 'cancel')])

    def button_confirm(self):
        sale_connect = self.env['purchase.order'].search([('sale_order_relate_id','=',self.sale_order_relate_id.id),
                                                          ('id','!=',self.id),('state','!=','purchase')])
        if sale_connect:
            for sale in sale_connect:
                sale.button_cancel()
        res = super().button_confirm()
        return res
