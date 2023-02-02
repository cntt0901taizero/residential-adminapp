# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Apartment Service And Support',
    'version': '1.0.0',
    'category': 'Resident',
    'summary': 'Apartment Service And Support',
    'description': """""",
    'depends': ['base', 'apartment_project'],
    'sequence': -100,
    'data': [
        'views/menu.xml',
        'views/news_view.xml',
        'views/notification_view.xml',
        'views/banner_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
