# -*- coding: utf-8 -*-

from odoo import fields,models


class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    hidden_menu_ids = fields.Many2many('ir.ui.menu', string='Hidden Menus')

    def load_menus(self, debug=False):
        user = self.env.user
        self.env['sale.order'].search()
        hidden_ids = set(user.hidden_menu_ids.ids)
        flat_menus = super().load_menus(debug)
        filtered_flat = {mid: m for mid, m in flat_menus.items() if mid not in hidden_ids}
        for menu in filtered_flat.values():
            if 'children' in menu:
                menu['children'] = [cid for cid in menu['children'] if cid in filtered_flat]
        return filtered_flat
