# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request, route
from odoo.fields import Command


class ReturnOrderController(http.Controller):

    @route('/webform/submit', type='http', auth='user', website=True, methods=['POST'])
    def submit_return_order(self, **data):
        """Passing the values from front end to the backend"""
        order_id = int(data.get('order_id'))
        order = request.env['sale.order'].browse(order_id)
        order_lines = []
        for line in order.order_line:
            qty = float(data.get(f'return_qty_{line.id}') or 0)
            reason = data.get(f'return_reason_{line.id}', '').strip()
            if qty > 0:
                order_lines.append(Command.create({
                    'product_id': line.product_id.id,
                    'delivered_qty': line.qty_delivered,
                    'return_qty': qty,
                    'reason': reason,
                }))
        request.env['website.return'].sudo().create({
            'sale_order_id': order_id,
            'partner_id': order.partner_id.id,
            'user_id': order.user_id.id,
            'order_line_ids': order_lines,
        })
        return request.redirect('/my/home')
