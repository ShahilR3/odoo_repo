# -*- coding: utf-8 -*-
{
    'name': 'Auto Leave Mail',
    'sequence': 1,
    'depends': ['base','hr','hr_holidays'],
    'data':[
        'data/ir_cron_data.xml',
        'data/mail_data.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}