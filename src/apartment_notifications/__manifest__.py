# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Apartment Notifications',
    'version': '1.0.0',
    'category': 'Resident',
    'summary': 'Apartment Notifications features',
    'description': """""",
    'depends': ['base', 'apartment_project'],
    'sequence': -100,
    'data': [
        'views/notification_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
