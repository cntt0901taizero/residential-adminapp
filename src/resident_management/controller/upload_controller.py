# -*- coding: utf-8 -*-
from odoo import api, Command, fields, models, _
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


class Upload_Controller(http.Controller):

    @http.route('/api/upload', methods=['POST'], auth='none', type='json', cors='*', csrf=False)
    def upload(self, *args, **kwargs):
        try:
            name = request.params['name']  # -> Tên file = Tên field
            res_id = request.params['res_id']  # -> Id của bản ghi file đính kèm
            res_model = request.params['res_model']  # -> Id của bản ghi file đính kèm
            datas = request.params['datas']  # -> data file Base64
            mimetype = request.params['mimetype']  # -> image/x-icon | image/png | text/css | application/pdf | ...
            res_field = request.params['res_field']  # -> Tên field
            attachment = self._upload(name, datas, mimetype, res_id, res_model, res_field)
            return common_response(200, '', attachment)

        except Exception as e:
            return common_response(500, e.name, [])

    def _upload(self, name, datas, mimetype, res_id, res_model, res_field):
        attachment = request.env['ir.attachment'].sudo().create({
            'name': name,
            'datas': datas,
            'mimetype': mimetype,
            'type': 'binary',
            'res_id': res_id,
            'res_model': res_model,
            'res_field': res_field
        })
        return attachment

