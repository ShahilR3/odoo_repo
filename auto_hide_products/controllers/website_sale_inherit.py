# -*- coding: utf-8 -*-

from odoo.http import request
from odoo.tools import lazy
from odoo.addons.website_sale.controllers.main import WebsiteSale, TableCompute


class WebsiteSaleInherit(WebsiteSale):

    def shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):
        """To add the condition where 0 quantity products are invisible for the user"""
        response = super().shop(page=page, category=category, search=search,
                                min_price=min_price, max_price=max_price, ppg=ppg, **post)
        qcontext = response.qcontext
        products = qcontext.get('products')
        products = products.sudo()
        if request.env.user.is_public:
            filtered_products = products.filtered(
                lambda p: p.product_visible and any(v.qty_available > 0 for v in p.product_variant_ids)
            )
            qcontext['products'] = filtered_products
            qcontext['search_product'] = filtered_products
            qcontext['search_count'] = len(filtered_products)
            qcontext['products_prices'] = {
                p.id: request.website.pricelist_id._get_product_price(p, 1.0, request.website.user_id)
                for p in filtered_products}
            qcontext['bins'] = lazy(lambda: TableCompute().process(filtered_products, ppg))
        return response
