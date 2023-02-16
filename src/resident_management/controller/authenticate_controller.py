import odoo
from odoo.addons.web.controllers.main import ensure_db
from odoo import http
from odoo.http import request
from odoo.tools import GettextAlias
from odoo.addons.resident_management.common import common_response

_ = GettextAlias()


class AuthenticateController(http.Controller):

    @http.route('/api/authenticate/login', method=['POST'], auth='public', type='json', cors='*', csrf=False)
    def login(self, **kwargs):
        uid = None
        ensure_db()
        request.params['login_success'] = False
        login = request.params['login']
        password = request.params['password']

        try:
            user_check = request.env['res.users'].sudo()\
                .search([('partner_id.phone', '=', login), ('password', '=', password)])
            if user_check and user_check.login:
                login = user_check.login

            uid = request.session.authenticate(request.session.db, login, password)
            request.params['login_success'] = True
            # aaa = uid.cookies.get('session_id')
            # session_info = request.env['ir.http'].session_info()
            user = request.env.user
            base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
            image_url = base_url + '/web/image?' + 'model=res.users&id=' + str(
                user.id) + '&field=avatar_1920' if user.avatar_1920 else None
            data = {
                'id': user.id or None,
                'sid': None,
                'expires_time': None,
                'login': user.login or None,
                'email': user.email or None,
                'phone': user.phone or None,
                'display_name': user.display_name or None,
                'image_url': image_url or None,
                'signature': user.signature or None,
                'active': user.active or None
            }
            return common_response(200, 'Success', data)

        except odoo.exceptions.AccessDenied as e:
            request.session.logout(keep_db=True)
            request.params['login_success'] = False
            request.uid = uid
            if e.args == odoo.exceptions.AccessDenied().args:
                return common_response(401, 'Wrong login/password', [])
            else:
                return common_response(401, e.args[0], [])

        except Exception as e:
            request.session.logout(keep_db=True)
            return common_response(500, e.args[0], [])

    @http.route('/api/authenticate/logout', method=['POST'], auth="user", type='json', cors='*', csrf=False)
    def logout(self, **kwargs):
        try:
            user = request.env.user
            request.session.logout(keep_db=True)
            return common_response(200, 'Success', user.id)
        except Exception as e:
            return common_response(500, 'Error', 0)

    @http.route('/api/authenticate/check-auth', method=['POST'], auth="user", type='json', cors='*', csrf=False)
    def check_auth(self, **kwargs):
        try:
            user = request.env.user
            if user.id > 0:
                return common_response(200, 'Success', user.id)
            else:
                return common_response(401, 'Error', 0)
        except Exception as e:
            return common_response(500, 'Error', 0)
