#-*- coding:utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    chatter_threshold_minutes = fields.Integer(string='Chatter Threshold (minutes)',
                                               config_parameter="crm_archive.chatter_threshold_minutes")
