# -*- coding: utf-8 -*-

{
    'name': 'sale order line',
    'sequence': 1,
    'depends': ['base','sale'],
    'data': [
             'security/ir.model.access.csv',
             'views/sale_order_line_views.xml',
             'wizard/make_sale_order_line_views.xml',
             'views/sale_order_line_action_views.xml',
             'views/sale_order_line_menu.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}