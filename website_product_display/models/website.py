#-*- coding:utf-8 -*-

from odoo import fields, models


class Website(models.Model):
    _inherit = 'website'

    stock_loc_id = fields.Many2one('stock.location',compute="_compute_stock_loc_id")

    def _compute_stock_loc_id(self):
        self.stock_loc_id = self.env['ir.config_parameter'].sudo().get_param('website_product_display.stock_loc_id')