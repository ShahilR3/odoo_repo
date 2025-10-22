# -*- coding: utf-8 -*-

from odoo import api, fields, models

class SalesPerson(models.Model):
    """Creating a new field"""
    _inherit = 'res.users'

    commission_id = fields.Many2one('crm.commission')
