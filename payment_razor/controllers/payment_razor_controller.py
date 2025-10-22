# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request

from odoo.addons.payment_razor.const import HANDLED_WEBHOOK_EVENTS


class RazorpayController(http.Controller):

    @http.route('/payment/razorpay/webhook', type='json', auth='public', csrf=False)
    def razor_webhook(self):
        data = request.get_json_data()
        if not data or 'payload' not in data or 'payment' not in data['payload']:
            return request.make_json_response({'error': 'Invalid payload'}, status=400)
        try:
            entity_data = data['payload']['payment']['entity']
            entity_data['entity_type'] = 'payment' # Explicitly set for Razorpay handler
            order_name = entity_data.get('description')
            if not order_name:
                return request.make_json_response({'error': 'No order_id provided'}, status=400)
            tx = request.env['payment.transaction'].sudo().search([
                ('reference', '=', order_name)
            ], limit=1)
            if not tx:
                return request.make_json_response({'status': 'ignored'}, status=200)
            tx._handle_notification_data('draco', entity_data)
        except Exception as e:
            return request.make_json_response({'error': 'Internal server error'}, status=500)
        return request.make_json_response({'status': 'ok'}, status=200)
