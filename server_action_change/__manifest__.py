# -*- coding: utf-8 -*-

{
    'name': 'server action',
    'sequence': 1,
    'depends': ['base','sale','sale_stock'],
    'data': [
             'views/ir_server_action.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
