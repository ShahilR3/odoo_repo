# -*- coding: utf-8 -*-
{
    'name': 'Warehouse Product Count',
    'sequence': 1,
    'depends': ['base','stock','website_sale'],
    'data':[
        'views/product_template.xml',
        'views/website_sale.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}