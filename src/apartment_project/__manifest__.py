# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Apartment Project Management',
    'version': '1.0',
    'category': 'Resident',
    'summary': 'Apartment Project Management features',
    'description': """""",
    # 'depends': ['base', 'mail', 'website_profile'],
    'sequence': -100,
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/blockhouse_view.xml',
        'views/building_view.xml',
        'views/building_house_view.xml',
        'views/building_floors_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}