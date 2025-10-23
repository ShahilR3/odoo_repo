# -*- coding: utf-8 -*-

import math
from odoo.http import request, route
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleInherit(WebsiteSale):

    def shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):
        response = super().shop(page=page, category=category, search=search, min_price=min_price, max_price=max_price,
                                ppg=ppg, **post)
        if 'products' in response.qcontext:
            original_products = response.qcontext['products']
            filtered_products = original_products.filtered(lambda p: p.product_visible and p.sudo().qty_available > 0)
            response.qcontext['products'] = filtered_products
            if 'search_product' in response.qcontext:
                search_products = response.qcontext['search_product']
                filtered_search_products = search_products.filtered(lambda p: p.product_visible and p.sudo().qty_available > 0)
                response.qcontext['search_product'] = filtered_search_products
            total_products = len(filtered_products)
            response.qcontext['search_count'] = total_products
            if 'products_prices' in response.qcontext:
                prices = response.qcontext['products_prices']
                if isinstance(prices, dict):
                    filtered_prices = {p.id: prices[p.id] for p in filtered_products if p.id in prices}
                    response.qcontext['products_prices'] = filtered_prices
            ppg_value = response.qcontext.get('ppg')
            page_count = max(1, math.ceil(total_products / ppg_value))
            base_url = '/shop' + ('/page/%d' % (page + 1) if page > 0 else '')
            pager = {
                'page_count': page_count,
                'offset': page * ppg_value,
                'page': {'url': f'{base_url}?', 'num': page + 1},
                'page_first': {'url': '/shop?', 'num': 1},
                'page_start': {'url': '/shop?', 'num': 1},
                'page_previous': {'url': f'/shop/page/{max(1, page)}?', 'num': max(1, page)},
                'page_next': {'url': f'/shop/page/{min(page_count, page + 2)}?', 'num': min(page_count, page + 2)},
                'page_end': {'url': f'/shop/page/{page_count}?', 'num': page_count},
                'page_last': {'url': f'/shop/page/{page_count}?', 'num': page_count},
                'pages': [{'url': '/shop?' if i == 0 else f'/shop/page/{i + 1}?', 'num': i + 1} for i in
                          range(page_count)],
            }
            response.qcontext['pager'] = pager
            print(f"Filtered products count: {total_products}, pages: {page_count}")
            print(response.qcontext)
        return response
