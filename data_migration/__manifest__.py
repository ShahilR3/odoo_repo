# -*- coding: utf-8 -*-

{
    'name': 'Data Migrate',
    'sequence': 1,
    'depends': ['base','sale','account'],
    'data':[
        'security/ir.model.access.csv',
        'wizard/make_data_migrate_views.xml',
        'views/data_migrate_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}