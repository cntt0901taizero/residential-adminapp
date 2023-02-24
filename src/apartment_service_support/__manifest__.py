# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Apartment Service And Support',
    'version': '1.0.0',
    'category': 'Resident',
    'summary': 'Apartment Service And Support',
    'description': """""",
    'depends': ['resident_management'],
    'data': [
        'views/menu.xml',
        'views/news_view.xml',
        'views/news_approve_view.xml',
        'views/notification_view.xml',
        'views/banner_view.xml',
        'views/banner_approve_view.xml',
        'views/feekind_view.xml',
        'views/paybillconfig_view.xml',
        'views/apartment_utilities_view.xml',
        'views/vehicle_view.xml',
        'views/access_card_view.xml',
        'views/complain_view.xml',
        'views/register_delivery_view.xml',
        'views/resident_handbook_view.xml',
    ],
    'installable': True,
    'auto_install': True,
}
