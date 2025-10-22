# -*- coding: utf-8 -*-
{
    'name': 'Multiple product Return',
    'version': '18.0.1.1.0',
    'summary': 'Website Management application',
    'sequence': 1,
    'description': "An application for managing your sale return",
    'category': 'Business',
    'depends': ['base','sale', 'mail', 'stock', 'contacts', 'account', 'web', 'website', 'portal'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/website_return_modal_view.xml',
        'views/website_sales_view.xml',
        'views/website_return_portal.xml',
        'views/website_return_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
