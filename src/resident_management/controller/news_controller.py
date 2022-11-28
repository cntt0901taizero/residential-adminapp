import json
from odoo import http
from odoo.http import request
from odoo.addons.resident_management.controller.common import common_response, alternative_json_response


class NewsController(http.Controller):

    @http.route('/api/news/search-page', methods=['POST'], auth='none', type='json', cors='*', csrf=False)
    def search_page(self, **kwargs):
        current_page = request.params['current_page']
        page_size = request.params['current_page']
        offset = 0 if current_page == 0 else current_page * page_size
        try:
            news = request.env['tb_news'].sudo()\
                .search([('state', '=', 'ACTIVE')], order="id asc", offset=offset, limit=page_size)
            list_data = []
            for item in news:
                # base_url = http.request.env['ir.config_parameter'].sudo().get_param('web.base.url')
                image_url = '/web/image?' + 'model=tb_news&id=' + str(
                    item.id) + '&field=image' if item.image else None
                file_url = '/web/content/tb_news/' + str(item.id) + '/file' if item.file else None
                list_data.append({'id': item.id, 'name': item.name, 'content': item.content,
                                  'image_url': image_url, 'file_url': file_url,
                                  'state': item.state, 'write_date': item.write_date})

            data_page = {
                "page_list_data": list_data,
                "size": page_size,
                "total_pages": "",
                "total_items": "",
                "current_page": current_page if current_page > 0 else 0,
            }

            return common_response(200, '', data_page)
        except Exception as e:
            return common_response(500, e.name, [])

