import odoo
from odoo.addons.web.controllers.main import ensure_db
from odoo import http
from odoo.http import request
from odoo.tools import GettextAlias
from werkzeug.wrappers import Request, Response
import json
from odoo.addons.resident_management.controller.common import common_response


_ = GettextAlias()


class AuthenticateController(http.Controller):

    @http.route('/api/authenticate/mobile', method=['POST'], auth='public', type='json', cors='*', csrf=False)
    def mobile_login(self, *args, **kwargs):
        uid = None
        session_info = None
        ensure_db()
        request.params['login_success'] = False

        try:
            user = request.env['res.users'].sudo().search([('login', '=', request.params['login'])])
            if not user.active:
                return common_response('403', 'User is deactived', [])

            uid = request.session.authenticate(request.session.db, request.params['login'], request.params['password'])
            request.params['login_success'] = True
            session_info = request.env['ir.http'].session_info()
            return common_response('200', 'Success', session_info)

        except odoo.exceptions.AccessDenied as e:
            request.session.logout(keep_db=True)
            request.params['login_success'] = False
            request.uid = uid
            if e.args == odoo.exceptions.AccessDenied().args:
                return common_response('401', 'Wrong login/password', [])
            else:
                return common_response('401', e.args[0], [])

        except Exception as e:
            request.session.logout(keep_db=True)
            return common_response('500', e.name, [])

    @http.route('/api/mobile/session/logout', method=['POST'], auth="none", cors='*')
    def moible_logout(self, **kwargs):
        request.session.logout(keep_db=True)
        return common_response('200', 'Success', [])
