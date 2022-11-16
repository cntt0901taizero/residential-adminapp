import json
import werkzeug
from odoo import http
from odoo.http import request
from odoo.addons.resident_management.controller.common import common_response
from odoo.service import security
import xmlrpc.client


class Notification_Controller(http.Controller):

    @http.route('/api/notifications/get-page', methods=['GET'], auth='none', type='json', cors='*', csrf=False)
    def get_page(self, **kwargs):
        current_page = int(kwargs.get('current_page', 0))
        page_size = int(kwargs.get('page_size', 10))
        offset = 0 if current_page == 0 else current_page * page_size
        try:
            news = http.request.env['tb_notification'].sudo() \
                .search([('type', '=', 'ACTIVE_BY_ADMIN'), ('state', '=', 'ACTIVE')], order="id asc", offset=offset, limit=page_size)
            list_data = []
            for item in news:
                list_data.append({'id': item.id, 'name': item.name, 'content': item.content,
                                  'state': item.state, 'write_date': item.write_date})

            data_page = {
                "page_list_data": list_data,
                "size": page_size,
                "total_pages": "",
                "total_items": "",
                "current_page": current_page if current_page > 0 else 0,
            }

            return common_response('200', '', data_page)
        except Exception as e:
            return common_response('500', e.name, [])