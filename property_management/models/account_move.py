# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountMove(models.Model):
    """Adding new field for the model"""
    _inherit = 'account.move'

    property_rental_id = fields.Many2one('property.rent.lease', string='Property Rent/Lease')
