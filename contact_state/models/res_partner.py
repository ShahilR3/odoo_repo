# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResPartner(models.Model):
    """Adding new field to the inherited model"""
    _inherit = "res.partner"

    state = fields.Selection(selection=[('customer','Customer'),
                                        ('vendor','Vendor'),
                                        ('both','Both')],compute='_compute_state',store=True)

    @api.depends('vat')
    def _compute_state(self):
        print("ABC")
        for rec in self:
            if rec.sale_order_ids and rec.supplier_rank:
                rec.write({'state': 'both'})
            elif rec.supllier_rank:
                rec.write({'state': 'vendor'})
            elif rec.sale_order_ids:
                rec.write({'state': 'customer'})
            else:
                rec.write({'state':None})
