#-*- coding: utf-8 -*-
{
    'name': 'CRM Commission',
    'version': '18.0.1.1.0',
    'summary': 'Commission Management application',
    'sequence': 1,
    'description': "An application for managing your crm commission",
    'category': 'Business',
    'depends': ['base', 'mail', 'crm', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/crm_commission_views.xml',
        'views/sales_person_views.xml'
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}