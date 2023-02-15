{
    'name': 'RESIDENTIAL MANAGEMENT',
    'version': '1.0.0',
    'category': 'Resident',
    'summary': 'RESIDENTIAL MANAGEMENT',
    'description': """RESIDENTIAL MANAGEMENT""",
    'depends': ['base', 'mail'],
    'sequence': -100,
    'data': [
        'views/icons.xml',
        'views/layout.xml',
        'security/resident_security.xml',
        'security/ir.model.access.csv',
        'views/dialog_box_confirm.xml',
        'views/menu.xml',
        'views/admin_account_view.xml',
        'views/resident_account_view.xml',
        'views/user_blockhouse_res_groups_rel_view.xml',
        'views/groups_inherit_view.xml',
        # 'views/templates.xml',
    ],
    'application': True,
    'license': 'AGPL-3',
    'assets': {
        'web.assets_frontend': [
            'resident_management/static/src/scss/login.scss',
        ],
        'web.assets_backend': [
            'resident_management/static/src/scss/variable.scss',
            'resident_management/static/src/scss/global.scss',
            'resident_management/static/src/scss/menu.scss',
            'resident_management/static/src/scss/control_panel.scss',
            'resident_management/static/src/scss/searchpanel.scss',
            'resident_management/static/src/scss/list.scss',
            'resident_management/static/src/scss/form.scss',
            'resident_management/static/src/scss/pivot.scss',
            'resident_management/static/src/scss/activity.scss',
            'resident_management/static/src/js/sidebar.js',
        ],
        'web.assets_qweb': [
            # 'resident_management/static/src/xml/styles.xml',
            # 'resident_management/static/src/xml/top_bar.xml',
            'resident_management/static/src/xml/sidebar.xml',
        ],
    },
    'images': [
        'static/description/banner.png',
        'static/description/theme_screenshot.png',
    ],
    'installable': True,
    'auto_install': False,
}
