# -*- coding: utf-8 -*-

{
    'name': 'product owner',
    'sequence': 2,
    'depends': ['point_of_sale'],
    'data': [
        'views/product_template_views.xml',
        'views/res_partner_views.xml',
    ],
    'assets':{
        'point_of_sale._assets_pos':[
            'product_owner/static/src/js/product_owner.js',
            'product_owner/static/src/js/payment_limit.js',
            'product_owner/static/src/views/pos_orderline_views.xml',
            'product_owner/static/src/views/partner_list_views.xml',
            'product_owner/static/src/views/partner_line_views.xml',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}