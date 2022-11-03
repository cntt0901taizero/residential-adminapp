import json

from odoo import http
from odoo.http import Response


class FeeKind_Controller(http.Controller):

    @http.route('/api/fee/fee-kind/get-all', methods=['GET'], auth='none', cors='*')
    def get_all(self, **kwargs):
        headers_json = {'Content-Type': 'application/json'}
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
            response = {
                "status": "200",
                "message": "",
                "data": list
            }
        except Exception as e:
            response = {
                "status": "error",
                "message": "not found",
                "data": []
            }
        return Response(json.dumps(response), headers=headers_json)

    @http.route('/api/fee/fee-kind/find-by-code/<self_code>', methods=['GET'], auth='none', cors='*')
    def find_by_id(self, self_code, **kwargs):
        headers_json = {'Content-Type': 'application/json'}
        try:
            reports = http.request.env['tb_feekind'].sudo().search([('code', '=', self_code)])
            data = {
                'id': reports.id,
                'code': reports.code,
                'name': reports.name,
                'note': reports.note,
                'is_active': reports.is_active
            }
            response = {
                "status": "200",
                "message": "",
                "data": data
            }
        except Exception as e:
            response = {
                "status": "error",
                "message": "not found",
                "data": []
            }
        return Response(json.dumps(response), headers=headers_json)


