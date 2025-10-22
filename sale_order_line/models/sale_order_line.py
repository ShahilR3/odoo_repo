from odoo import models

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def action_make_sale_order_line_wizard(self):
        view = self.env.ref('sale_order_line.view_sale_order_line_wizard_form')
        return {
            'name': 'My Wizard',
            'type': 'ir.actions.act_window',
            'res_model': 'make.sale.order.line',
            'view_mode': 'form',
            'view_id': view.id,
            'target': 'new',
        }
