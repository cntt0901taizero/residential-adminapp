import json

from odoo import http
from odoo.http import Response
from odoo.addons.resident_management.controller.common import common_response


class FeeKind_Controller(http.Controller):

    @http.route('/api/fee/fee-kind/get-all', methods=['GET'], auth='none', cors='*')
    def get_all(self, **kwargs):
        try:
            reports = http.request.env['tb_feekind'].sudo().search([])
            list = []
            for item in reports:
                list.append({
                    'id': item.id,
                    'code': item.code,
                    'name': item.name,
                    'note': item.note,
                    'is_active': item.is_active
                })
            return common_response(200, '', list)
        except Exception as e:
            return common_response(500, e.name, [])

    @http.route('/api/fee/fee-kind/find-by-code/<self_code>', methods=['GET'], auth='none', cors='*')
    def find_by_id(self, self_code, **kwargs):
        try:
            reports = http.request.env['tb_feekind'].sudo().search([('code', '=', self_code)])
            data = {
                'id': reports.id,
                'code': reports.code,
                'name': reports.name,
                'note': reports.note,
                'is_active': reports.is_active
            }
            return common_response(200, '', data)
        except Exception as e:
            return common_response(500, 'Data not found', [])
