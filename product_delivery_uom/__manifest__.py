# -*- coding: utf-8 -*-
{
    'name': 'Product Delivery UOM',
    'sequence': 2,
    'depends': ['base','sale','product','stock'],
    'data': [
        'views/product_product_views.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}