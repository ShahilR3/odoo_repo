# -*- coding: utf-8 -*-

{
    'name': "Razor",
    'version': '1.0',
    'category': 'Accounting/Payment Providers',
    'sequence': 355,
    'summary': "A payment provider in India.",
    'description': " ",
    'depends': ['payment'],
    'data': [
        'data/payment_provider_data.xml',
        'views/payment_providers_views.xml',
    ],
'assets': {
        'web.assets_frontend': [
            'payment_razor/static/src/js/payment_form.js',
        ],
    },
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'license': 'LGPL-3',
}
