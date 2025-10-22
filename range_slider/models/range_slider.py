#-*- coding: utf-8 -*-

from odoo import fields, models

class RangeSlider(models.Model):
    _name = "range.slider"

    range_value = fields.Integer("Range")