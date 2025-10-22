# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountMoveLine(models.Model):
    """Adding a new field to the inherited model"""
    _inherit = 'account.move.line'

    property_line_id = fields.Many2one('property.intermediate', string="Property Lines")
