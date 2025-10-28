# -*- coding: utf-8 -*-

from odoo import fields, models


class ResPartner(models.Model):
    """Adding new field to the inherited model"""
    _inherit = "res.partner"

    is_vip = fields.Boolean(default=False, string="Is VIP")
    vip_discount = fields.Float(string="Vip Discount")
