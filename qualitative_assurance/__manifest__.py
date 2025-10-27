# -*- coding: utf-8 -*-

{
    'name': 'Quality Assurance',
    'version': '18.0.1.1.0',
    'summary': 'Quality Assurance application',
    'sequence': 1,
    'description': "An application for managing the quality",
    'category': 'Business',
    'depends': ['base','sale','purchase', 'mail', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/quality_assurance_views.xml',
        'views/quality_alert_views.xml',
        'views/quality_test_views.xml',
        'views/stock_picking_views.xml',
        'views/quality_assurance_menus.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
