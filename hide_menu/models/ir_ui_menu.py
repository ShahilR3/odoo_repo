# -*- coding: utf-8 -*-

from odoo import fields,models


class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    hide_users_ids = fields.Many2many('res.users', string='Hide Menu User',
                                      domain=lambda self: [('id', '!=', self.env.uid)])

    # def load_menus(self, debug=False):
    #     """Loading the menu and hiding the menus selected"""
    #     user = self.env.user
    #     hidden_ids = set(user.hidden_menu_ids.ids)
    #     menus = super().load_menus(debug)
    #     filtered_menu = {menu_id: menu_values for menu_id, menu_values in menus.items() if menu_id not in hidden_ids}
    #     for menu in filtered_menu.values():
    #         if 'children' in menu:
    #             menu['children'] = [children_id for children_id in menu['children'] if children_id in filtered_menu]
    #     return filtered_menu
