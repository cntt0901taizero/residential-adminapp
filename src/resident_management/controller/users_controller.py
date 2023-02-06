import json
import werkzeug
from odoo.addons.portal.controllers.portal import get_error
from odoo import http
from odoo.http import request
from odoo.addons.resident_management.common import common_response
from odoo.service import security, model
import xmlrpc.client
from odoo.exceptions import ValidationError, AccessError, MissingError, UserError, AccessDenied
from odoo.tools import GettextAlias

_ = GettextAlias()

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

    @http.route('/api/users/update', methods=['POST'], auth='none', type='json', cors='*', csrf=False)
    def update(self, *args, **kwargs):
        try:
            user = request.env.user
            request.env['res.users'].sudo().browse(request.params['id'])\
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

    # @http.route('/api/users/fn_change_password', type='http', auth='none', website=True, methods=['GET', 'POST'])
    # def security(self, **post):
    #     values = self._prepare_portal_layout_values()
    #     values['get_error'] = get_error
    #     values['allow_api_keys'] = bool(request.env['ir.config_parameter'].sudo().get_param('portal.allow_api_keys'))
    #
    #     if request.httprequest.method == 'POST':
    #         values.update(self._update_password(
    #             post['old'].strip(),
    #             post['new1'].strip(),
    #             post['new2'].strip()
    #         ))
    #
    #     return request.render('portal.portal_my_security', values, headers={
    #         'X-Frame-Options': 'DENY'
    #     })
    #
    # def _prepare_portal_layout_values(self):
    #     """Values for /my/* templates rendering.
    #
    #     Does not include the record counts.
    #     """
    #     # get customer sales rep
    #     sales_user = False
    #     partner = request.env.user.partner_id
    #     if partner.user_id and not partner.user_id._is_public():
    #         sales_user = partner.user_id
    #
    #     return {
    #         'sales_user': sales_user,
    #         'page_name': 'home',
    #     }
    #
    # def _update_password(self, old, new1, new2):
    #     for k, v in [('old', old), ('new1', new1), ('new2', new2)]:
    #         if not v:
    #             return {'errors': {'password': {k: _("You cannot leave any password empty.")}}}
    #
    #     if new1 != new2:
    #         return {'errors': {'password': {'new2': _("The new password and its confirmation must be identical.")}}}
    #
    #     try:
    #         request.env['res.users'].change_password(old, new1)
    #     except UserError as e:
    #         return {'errors': {'password': e.name}}
    #     except AccessDenied as e:
    #         msg = e.args[0]
    #         if msg == AccessDenied().args[0]:
    #             msg = _('The old password you provided is incorrect, your password was not changed.')
    #         return {'errors': {'password': {'old': msg}}}
    #
    #     # update session token so the user does not get logged out (cache cleared by passwd change)
    #     new_token = request.env.user._compute_session_token(request.session.sid)
    #     request.session.session_token = new_token
    #
    #     return {'success': {'password': True}}

    @http.route('/api/users/update_password', method=['POST'], auth="user", type='json', cors='*', csrf=False)
    def update_password(self, **kwargs):
        old = request.params['old']
        new1 = request.params['new1']
        new2 = request.params['new2']

        for k, v in [('old', old), ('new1', new1), ('new2', new2)]:
            if not v:
                return common_response(500, _("You cannot leave any password empty."), 0)
        if new1 != new2:
            return common_response(500, _("The new password and its confirmation must be identical."), 0)

        try:
            request.env['res.users'].change_password(old, new1)
        except UserError as e:
            return common_response(500, e, 0)
        except AccessDenied as e:
            msg = e.args[0]
            if msg == AccessDenied().args[0]:
                msg = _('The old password you provided is incorrect, your password was not changed.')
            return common_response(500, msg, 0)

        # # update session token so the user does not get logged out (cache cleared by passwd change)
        # new_token = request.env.user._compute_session_token(request.session.sid)
        # request.session.session_token = new_token
        return common_response(200, 'Success', 1)
