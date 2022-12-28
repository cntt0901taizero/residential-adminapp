# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Apartment Pay bill',
    'version': '1.0',
    'category': 'Resident',
    'summary': 'Apartment Pay bill features',
    'description': """""",
    # 'depends': ['base', 'mail', 'website_profile'],
    'sequence': -100,
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/feekind_view.xml',
        'views/paybillconfigrender_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
