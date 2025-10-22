# -*- coding: utf-8 -*-

{
    'name': 'Bill Sale',
    'sequence': 1,
    'depends': ['base','sale','account'],
    'data':[
        'views/account_move_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}