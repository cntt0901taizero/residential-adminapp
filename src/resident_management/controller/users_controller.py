import json
import werkzeug
from odoo import http
from odoo.http import request
from odoo.addons.resident_management.common import common_response
from odoo.service import security, model
import xmlrpc.client


class Users_Controller(http.Controller):

    @http.route('/api/users/user-info', methods=['GET'], auth='user', type='json', cors='*', csrf=False)
    def user_info(self, *args, **kwargs):
        try:
            user = request.env.user
            sid = request.session.sid
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
            return common_response(200, '', data)
        except Exception as e:
            return common_response(500, e.name, [])

    @http.route('/api/users/put', methods=['PORT'], auth='user', type='json', cors='*', csrf=False)
    def image_upload(self, *args, **kwargs):
        try:
            user = request.env.user
            request.env['res.users'].sudo().browse(request.params['id']) \
                .write({
                    'name': request.params['name'],
                    'display_name': request.params['display_name'],
                    'login': request.params['login'],
                    'phone': request.params['phone'],
                    'email': request.params['email'],
                    'image_1920': request.params['image_data'],
                })
            # model.execute('res.partner', 'write', )

            return common_response(200, '', user.id)
        except Exception as e:
            return common_response(500, e.name, [])
