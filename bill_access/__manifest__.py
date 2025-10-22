# -*- coding: utf-8 -*-

{
    'name': 'Bill Purchase',
    'sequence': 1,
    'depends': ['base','purchase','account'],
    'data':[
        'views/account_move_view.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}