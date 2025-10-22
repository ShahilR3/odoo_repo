# -*- coding: utf-8 -*-

{
    'name': 'Project Template',
    'sequence': 10,
    'description':'An application for adding project/task templates',
    'category': 'Projects',
    'depends': ['base','project'],
    'data': [
        'security/project_template_group.xml',
        'security/project_template_security.xml',
        'data/project_template_manager_data.xml',
        'security/ir.model.access.csv',
        'views/project_template_views.xml',
        'views/task_template_views.xml',
        'views/project_project.xml',
        'views/project_task.xml',
        'views/project_template_menus.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
