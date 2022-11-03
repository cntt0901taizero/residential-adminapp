import json

from odoo import http
from odoo.http import Response


class PaybillConfigRender_Controller(http.Controller):

    @http.route('/api/fee/paybill-configrender/get-all', methods=['GET'], auth='none', cors='*')
    def get_all(self, **kwargs):
        headers_json = {'Content-Type': 'application/json'}
        try:
            reports = http.request.env['tb_paybill_configrender'].sudo().search([])
            list_data = []
            for item in reports:
                list_data.append({
                    'id': item.id,
                    'fee_kind_id': item.fee_kind_id, 'fee_kind_code': item.fee_kind_code, 'fee_kind_name': item.fee_kind_name,
                    'block_house_id': item.block_house_id, 'block_house_ma': item.block_house_ma, 'block_house_name': item.block_house_name,
                    'building_id': item.building_id, 'building_code': item.building_code, 'building_name': item.building_name,
                    'house_id': item.house_id, 'house_code': item.house_code, 'house_number': item.house_number,
                    'price': item.price,
                })
            response = {
                "status": "200",
                "message": "",
                "data": list_data
            }
        except Exception as e:
            response = {
                "status": "error",
                "message": "",
                "data": []
            }

        return Response(json.dumps(response), headers=headers_json)

