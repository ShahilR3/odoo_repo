# -*- coding: utf-8 -*-

{
    'name': 'Range Slider',
    'version': '18.0.1.1.0',
    'summary': 'Wigdet',
    'sequence': 1,
    'description': "A widget",
    'category': 'Business',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/range_slider_views.xml',
        'views/range_slider_menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'range_slider/static/src/component/range_field.xml',
            'range_slider/static/src/component/range_slider.js',
                                ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}