# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResPartner(models.Model):
    """Adding new field to the inherited model"""
    _inherit = "res.partner"

    sales_date = fields.Datetime(string='Sales Date', readonly=True)
