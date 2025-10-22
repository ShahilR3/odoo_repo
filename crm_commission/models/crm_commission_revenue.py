#-*- coding: utf-8 -*-

from odoo import api,fields,models

class CrmCommissionRevenue(models.Model):
    _name = "crm.commission.revenue"

    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id', string="Currency")
    sequence_number = fields.Integer(string="Sequence", default=0)
    rate = fields.Float(string='Rate', store=True)
    commission_id = fields.Many2one('crm.commission')
    from_amount = fields.Float("From Amount")
    to_amount = fields.Float("To Amount")
