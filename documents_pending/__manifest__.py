# -*- coding: utf-8 -*-

{
    'name': 'sale due docs',
    'sequence': 1,
    'depends': ['base','sale','contacts'],
    'data': [
             'views/res_partner_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}