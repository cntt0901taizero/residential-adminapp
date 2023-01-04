# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Apartment Banners',
    'version': '1.0',
    'category': 'Resident',
    'summary': 'Apartment Banners features',
    'description': """""",
    # 'depends': ['base', 'mail', 'website_profile'],
    'sequence': -100,
    'data': [
        'views/menu.xml',
        'views/banner_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
