import json

from odoo import http
from odoo.addons.resident_management.controller.common import valid_response, invalid_response


class NewsController(http.Controller):

    @http.route('/api/news/get-page', methods=['GET'], cors='*', auth='none')
    def get_page(self, **kwargs):
        current_page = int(kwargs.get('current_page', 0))
        page_size = int(kwargs.get('page_size', 10))
        offset = 0 if current_page == 0 else current_page * page_size
        try:
            news = http.request.env['tb_news'].sudo().search([('state', '=', 'ACTIVE')], order="id asc", offset=offset,
                                                      limit=page_size)
            list = []
            for item in news:
                base_url = http.request.env['ir.config_parameter'].sudo().get_param('web.base.url')
                image_url = base_url + '/web/image?' + 'model=tb_news&id=' + str(
                    item.id) + '&field=image' if item.image else None
                file_url = base_url + '/web/content/tb_news/' + str(item.id) + '/file' if item.file else None
                list.append({'id': item.id, 'name': item.name, 'content': item.content, "image_url": image_url,
                             "file_url": file_url, "state": item.state, "write_date": item.write_date})

            data_page = {
                "page_list_data": list,
                "size": page_size,
                "total_pages": "",
                "total_items": "",
                "current_page": current_page if current_page > 0 else 0,
            }

            return valid_response(data_page, status=200)
        except Exception as e:
            return invalid_response("failed", message=e.name)
