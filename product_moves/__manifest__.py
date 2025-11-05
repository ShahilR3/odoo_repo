# -*- coding: utf-8 -*-

{
    'name': 'Product Move',
    'sequence': 1,
    'depends': ['base','product','account'],
    'data':[
        'views/product_template_views.xml',
        'views/product_product_views.xml',
        'views/account_debit.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}