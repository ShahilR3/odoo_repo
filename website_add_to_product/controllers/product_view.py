# -*- coding: utf-8 -*-

import base64

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class ProductDetaail(WebsiteSale):

    @http.route(['/shop/product'], type='http', auth="public", website=True, csrf=True)
    def web_product_form(self, **data):
        if request.httprequest.method == 'POST':
            product_image = request.httprequest.files.get('prod_img')
            product_name = data.get('prod_name') or 'Unnamed Product'
            price = float(data.get('add_price') or 0)
            product_quantity = int(data.get('add_qty'))
            image_data = None
            if product_image:
                image_data = base64.b64encode(product_image.read())
            request.env['product.template'].sudo().create({
                'name': product_name,
                'list_price': price,
                'qty_available': product_quantity,
                'image_1920': image_data,
                'website_published': True,
            })
            redirect_url = request.params.get('redirect', '/shop')
            return request.redirect(redirect_url)
        return request.render('website_add_to_product.template_product_detail')
