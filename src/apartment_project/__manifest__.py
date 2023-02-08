# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Apartment Project Management',
    'version': '1.0.0',
    'category': 'Resident',
    'summary': 'Apartment Project Management features',
    'description': """""",
    'depends': ['resident_management'],
    'data': [
        'views/menu.xml',
        'views/blockhouse_view.xml',
        'views/building_view.xml',
        'views/building_floors_view.xml',
        'views/building_house_view.xml',
    ],
    'installable': True,
    'auto_install': True,
}
