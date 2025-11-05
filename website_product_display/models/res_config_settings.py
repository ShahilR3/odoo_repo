#-*- coding:utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    stock_loc_id = fields.Many2one('stock.location', string='Stock Location',
                                               config_parameter="website_product_display.stock_loc_id")
