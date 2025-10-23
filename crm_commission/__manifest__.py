#-*- coding: utf-8 -*-
{
    'name': 'CRM Commission',
    'version': '18.0.1.1.0',
    'summary': 'Commission Management application',
    'sequence': 1,
    'description': "An application for managing your crm commission",
    'category': 'Business',
    'depends': ['base','sale', 'mail', 'crm', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_commission_views.xml',
        'views/commission_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}