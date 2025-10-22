# -*- coding: utf-8 -*-

from odoo import api, fields, models

class SalesTeam(models.Model):
    """Creating a new fields"""
    _inherit = 'crm.team'

    commission_id = fields.Many2one('crm.commission')
