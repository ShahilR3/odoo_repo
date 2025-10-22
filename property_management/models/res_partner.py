# -*- coding: utf-8 -*-

from odoo import fields, models


class ResPartner(models.Model):
    """Adding new field to the inherited model"""
    _inherit = "res.partner"

    partner_property_ids = fields.One2many('property.properties', 'owner_id',
                                           string="Property Name", ondelete="cascade")
