# -*- coding: utf-8 -*-

from odoo import http, fields
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

class ProductCart(WebsiteSale):

    @http.route(['/shop/product/select'], type='http', auth="public", website=True, csrf=True)
    def web_form(self, **kwargs):
        """The contents to be displayed in this url"""
        product_id = request.env['product.product'].sudo().search([])
        datas = {
            'product_id': product_id,
        }
        return request.render('website_add_to_cart.template_product_detail', datas)

    @http.route(['/cart/create'], type='http', auth="public", website=True, csrf=True)
    def add_to_cart(self, **data):
        product = data.get('product_id')
        quantity = data.get('add_qty')
        order = request.website.sale_get_order()
        order._cart_update(
            product_id=int(product),
            add_qty=quantity,
        )
        values = {}
        if order:
            order.order_line.filtered(lambda sol: sol.product_id and not sol.product_id.active).unlink()
            values['suggested_products'] = order._cart_accessories()
            values.update(self._get_express_shop_payment_values(order))
        values.update({
            'website_sale_order': order,
            'date': fields.Date.today(),
            'suggested_products': [],
        })
        return request.render("website_sale.cart", values)
