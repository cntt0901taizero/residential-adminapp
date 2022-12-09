{
    'name': 'RESIDENTIAL MANAGEMENT',
    'version': '1.0.0',
    'category': 'Resident',
    'summary': 'RESIDENTIAL MANAGEMENT',
    'description': """RESIDENTIAL MANAGEMENT""",
    'depends': ['base', 'mail', 'website_profile'],
    'sequence': -100,
    'data': [
        'security/resident_security.xml',
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/blockhouse_view/blockhouse_view.xml',
        'views/blockhouse_view/building_view.xml',
        'views/blockhouse_view/building_house_view.xml',
        'views/blockhouse_view/building_floors_view.xml',
        'views/news_view/news_view.xml',
        'views/notification_view/notification_view.xml',
        'views/banner/banner_view.xml',
        'views/account_view/taikhoan_view.xml',
        'views/fee_view/paybillconfigrender_view.xml',
        'views/fee_view/feekind_view.xml',

        # 'views/system_parameter_view.xml',
        # 'views/notification_view.xml',
        # 'views/resident_report_view.xml',
    ],
    'application': True,
    'license': 'AGPL-3',
    'assets': {
        'web.assets_backend': [
            'resident_management/static/css/style.css',
            'resident_management/static/js/website.js'
        ]
    }
}
