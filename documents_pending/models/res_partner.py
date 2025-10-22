# -*- coding: utf

from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = "res.partner"

    document_ids = fields.One2many("account.payment","partner_id",
                                       compute="compute_documents")
    pending_sale_order_ids = fields.One2many('sale.order','partner_id',
                                             compute="compute_pending_sale_order")

    def compute_documents(self):
        """Outstanding Invoice"""
        for partner in self:
           payment = self.env['account.payment'].search([('partner_id', '=', partner.id), ('state', '!=', 'paid')],)
           partner.document_ids = payment or self.env['account.payment']

    def compute_pending_sale_order(self):
        """Incomplete Sale order"""
        for partner in self:
            sale_order = self.env['sale.order'].search([('partner_id', '=', partner.id),('state', '!=', 'sale')])
            partner.pending_sale_order_ids = sale_order or self.env['sale.order']