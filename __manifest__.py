# -*- coding: utf-8 -*-
{
    'name': 'Universidad ISEP test',
    'summary': '''
        Prueba técnica segun los requerimientos
    ''',
    'author': 'Daniel Chuc',
    'license': 'AGPL-3',
    'category': 'Installer',
    'version': '13.0.1.0.3',
    'depends': [
        'contacts',
    ],
    'data': [
        'data/skills.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',
        'report/experience.xml',
        'views/menu.xml',
        'views/experience.xml',
        'views/skill.xml',
        'views/res_partner.xml',
        'wizard/load_skill.xml',
        'wizard/generate_report.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
