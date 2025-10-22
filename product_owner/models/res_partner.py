# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ResPartner(models.Model):
    """Inherits model res.partner and adds new fields to it"""
    _inherit = "res.partner"

    max_limit = fields.Boolean("Payment Limit", default=False)
    payment_limit = fields.Integer("Max Limit")

    @api.model
    def _load_pos_data_fields(self, config_id):
        fields = super()._load_pos_data_fields(config_id)
        fields.append('max_limit')
        fields.append('payment_limit')
        return fields
