# -*- coding: utf-8 -*-

{
    'name': 'Website Form',
    'sequence': 1,
    'depends': ['base','product','website_sale','website'],
    'data':[
        'views/product_details.xml',
        'views/website_menu_views.xml',
    ],
    # 'assets': {
    #         'web.assets_frontend': [
    #             'website_add_to_cart/static/src/js/popup.js',
    #         ],
    #     },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
