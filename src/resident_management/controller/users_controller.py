import json

import werkzeug

from odoo import http
from odoo.http import request
from odoo.addons.resident_management.controller.common import valid_response, invalid_response
from odoo.service import security

import xmlrpc.client


class Users_Controller(http.Controller):

    @http.route([
        '/auth/login/email',
    ], type='http', auth="public", website=True, methods=["POST"], csrf=False)
    def users_login_email(self, **kwargs):
        url = 'http://localhost:8069/'
        db_name = 'my_db_1'
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        common.version()
        print("ui id")
        return "123"

    @http.route('/api/users/user-info', methods=['GET'], auth='user', cors='*')
    def user_info(self, **kwargs):
        headers_json = {'Content-Type': 'application/json'}
        try:
            user = request.env.user
            sid = request.session.sid
            # reports = request.env['res.users'].search([('id', '=', self_id)])
            base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
            image_url = base_url + '/web/image?' + 'model=res.users&id=' + str(
                user.id) + '&field=avatar_1920' if user.avatar_1920 else None
            data = {
                'id': user.id,
                'sid': sid,
                'login': user.login,
                'email': user.email,
                'phone': user.phone,
                'display_name': user.display_name,
                'image_url': image_url,
                'signature': user.signature,
                'active': user.active
            }
            return valid_response(data, 200)
        except Exception as e:
            return invalid_response(e.name, 500)
