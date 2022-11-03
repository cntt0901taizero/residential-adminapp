import odoo
from odoo.addons.web.controllers.main import ensure_db
from odoo import http
from odoo.http import request
from odoo.http import Response
from odoo.tools import GettextAlias
from odoo.addons.resident_management.controller.common import valid_response, invalid_response

_ = GettextAlias()


class AuthenticateController(http.Controller):

    @http.route('/api/authenticate/mobile', method=['POST'], auth='none', type='json')
    def mobile_login(self, **kwargs):
        ensure_db()
        request.params['login_success'] = False

        try:
            uid = None
            session_info = None
            uid = request.session.authenticate(request.session.db, request.params['login'], request.params['password'])
            request.params['login_success'] = True
            session_info = request.env['ir.http'].session_info()
            return session_info

        except odoo.exceptions.AccessDenied as e:
            Response.status = "401"
            request.session.logout(keep_db=True)
            request.params['login_success'] = False
            request.uid = uid
            if e.args == odoo.exceptions.AccessDenied().args:
                error = {"message": "Wrong login/password"}
                return error
            else:
                error = {"message": e.args[0]}
                return error

        except Exception as e:
            Response.status = "401"
            request.session.logout(keep_db=True)
            return invalid_response("Failed", message=e.name)

    @http.route('/api/mobile/session/logout', auth="none")
    def moible_logout(self, **kwargs):
        request.session.logout(keep_db=True)
        return valid_response({
            "message": "Success"
        })