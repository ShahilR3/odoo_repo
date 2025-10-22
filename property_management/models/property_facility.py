# -*- coding: utf-8 -*-

from odoo import fields, models


class PropertyFacility(models.Model):
    """Creating a facility model and its fields"""
    _name = "property.facility"
    _description = "To create the facilities of the product"

    name = fields.Char(string="Facility")
    colors = fields.Integer('Color')
