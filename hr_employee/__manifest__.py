#-*- coding: utf-8 -*-
{
    'name': 'Employee state',
    'version': '18.0.1.1.0',
    'summary': 'Commission Management application',
    'sequence': 1,
    'description': "An application for managing your crm commission",
    'category': 'Business',
    'depends': ['base','sale', 'hr'],
    'data': [
        'views/hr_employee_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}