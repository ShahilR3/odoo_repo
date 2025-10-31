#-*- coding: utf-8 -*-
{
    'name': 'CRM Archive',
    'version': '18.0.1.1.0',
    'summary': 'Commission Management application',
    'sequence': 1,
    'description': "An application for managing your crm commission",
    'category': 'Business',
    'depends': ['base','crm',],
    'data': [
        'data/ir_cron_data.xml',
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}