# -*- coding: utf-8 -*-

{
    'name': 'Existing Invoice Lines',
    'sequence': 1,
    'depends': ['base','sale','account'],
    'data':[
        'security/ir.model.access.csv',
        'views/account_move_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}