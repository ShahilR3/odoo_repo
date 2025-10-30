# -*- coding: utf-8 -*-

{
    'name': 'Purchase RFQ',
    'sequence': 1,
    'depends': ['base','purchase','sale'],
    'data':[
        'views/purchase_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}