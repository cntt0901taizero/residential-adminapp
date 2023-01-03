{
    'name': 'RESIDENTIAL MANAGEMENT',
    'version': '1.0.0',
    'category': 'Resident',
    'summary': 'RESIDENTIAL MANAGEMENT',
    'description': """RESIDENTIAL MANAGEMENT""",
    'depends': ['base', 'mail', 'website_profile'],
    'sequence': -100,
    'data': [
        'views/icons.xml',
        'views/layout.xml',
        'security/resident_security.xml',
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/account_view/taikhoan_view.xml',
        'views/user_blockhouse_res_groups_rel_view.xml',
        'views/groups_inherit_view.xml',
        # 'views/notification_view.xml',
        # 'views/resident_report_view.xml',
    ],
    'application': True,
    'license': 'AGPL-3',
    'assets': {
        'web.assets_frontend': [
            'resident_management/static/src/scss/login.scss',
        ],
        'web.assets_backend': [
            'resident_management/static/src/css/style.css',
            'resident_management/static/src/scss/theme_accent.scss',
            'resident_management/static/src/scss/navigation_bar.scss',
            'resident_management/static/src/scss/datetimepicker.scss',
            'resident_management/static/src/scss/theme.scss',
            'resident_management/static/src/scss/sidebar.scss',

            'resident_management/static/src/js/fields/colors.js',
            'resident_management/static/src/js/chrome/sidebar_menu.js',
        ],
        'web.assets_qweb': [
            'resident_management/static/src/xml/styles.xml',
            'resident_management/static/src/xml/top_bar.xml',
        ],
    },
    'images': [
        'static/description/banner.png',
        'static/description/theme_screenshot.png',
    ],
    'installable': True,
    'auto_install': False,
}
