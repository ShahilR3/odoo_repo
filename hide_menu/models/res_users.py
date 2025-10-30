# -*- coding: utf-8 -*-

from odoo import api, models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    hidden_menu_ids = fields.Many2many('ir.ui.menu', string='Hidden Menus')

    @api.onchange('hidden_menu_ids')
    def on_change_hidden_menu_ids(self):
        """On changing the fields calling the menu load function"""
        self.env['ir.ui.menu'].load_menus(False)
