#-*- coding: utf-8 -*-
{
    'name':'Sales Dashboard',
    'version':'18.0.0.0.0',
    'description':'A dasboard with informations about thhe sales',
    'depends':['base','sale'],
    'data':[
        'views/sales_dashboard_views.xml',
    ],
    'assets':{
        'web.assets_backend':[
            'sales_dashboard/static/src/js/sales_dashboard.js',
            'sales_dashboard/static/src/xml/sales_dashboard_template_views.xml',
            'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js',
        ],
    },
    'installable':True,
    'application':True,
    'license':'LGPL-3'
}