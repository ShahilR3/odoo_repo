# -*- coding: utf-8 -*-

from odoo import fields, models


class ResPartner(models.Model):
    """Adding new field to the inherited model"""
    _inherit = "res.partner"

    state = fields.Selection(selection=[('customer','Customer'),
                                        ('vendor','Vendor'),
                                        ('both','Both')],compute='_compute_state')

    def _compute_state(self):
        """Set the state of partners"""
        for rec in self:
            if rec.customer_rank and rec.supplier_rank:
                rec.write({'state': 'both'})
            elif rec.supllier_rank:
                rec.write({'state': 'vendor'})
            elif rec.customer_rank:
                rec.write({'state': 'customer'})
            else:
                rec.write({'state':None})
