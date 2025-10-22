# -*- coding: utf-8 -*-

{
    'name': 'sale order state',
    'sequence': 1,
    'depends': ['base','sale','sale_stock'],
    'data': [
             'views/sale_state_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
