# -*- coding: utf-8 -*-

{
    'name': 'Hide products website',
    'sequence': 1,
    'depends': ['product', 'website_sale', 'sale_management'],
    'data':[
        'views/product_template.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}