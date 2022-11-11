from werkzeug.wrappers import json, Request, Response

import odoo
from odoo.addons.web.controllers.main import ensure_db
from odoo import http
from odoo.http import request
from odoo.tools import GettextAlias

_ = GettextAlias()


class AuthenticateController(http.Controller):

    @http.route('/api/authenticate/mobile', method=['POST'], auth='none', type='json')
    def mobile_login(self, **kwargs):
        uid = None
        session_info = None
        ensure_db()
        request.params['login_success'] = False
        headers = {"Content-Type": "application/json"}

        try:
            user = request.env['res.users'].search([('login', '=', request.params['login'])])
            if not user.active:
                response_data = {
                    'status': 403,
                    'message': 'User is deactived',
                    'data': None
                }
                return Response(json.dumps(response_data), headers=headers)

            uid = request.session.authenticate(request.session.db, request.params['login'], request.params['password'])
            request.params['login_success'] = True
            session_info = request.env['ir.http'].session_info()
            response_data = {
                'status': 200,
                'message': 'Success',
                'data': session_info
            }
            return Response(json.dumps(response_data), headers=headers)

        except odoo.exceptions.AccessDenied as e:
            request.session.logout(keep_db=True)
            request.params['login_success'] = False
            request.uid = uid
            if e.args == odoo.exceptions.AccessDenied().args:
                response_data = {
                    'status': 401,
                    'message': 'Wrong login/password',
                    'data': None
                }
                return Response(json.dumps(response_data), headers=headers)
            else:
                response_data = {
                    'status': 401,
                    'message': e.args[0],
                    'data': None
                }
                return Response(json.dumps(response_data), headers=headers)

        except Exception as e:
            request.session.logout(keep_db=True)
            response_data = {
                'status': 500,
                'message': e.name,
                'data': None
            }
            return Response(json.dumps(response_data), headers=headers)

    @http.route('/api/mobile/session/logout', auth="none")
    def moible_logout(self, **kwargs):
        headers = {"Content-Type": "application/json"}
        request.session.logout(keep_db=True)
        response_data = {
            'status': 200,
            'message': 'Success',
            'data': None
        }
        return Response(json.dumps(response_data), headers=headers)
