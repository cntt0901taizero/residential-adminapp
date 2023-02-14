import json
import logging
from odoo.http import request, JsonRequest, Response
from odoo.tools import date_utils

_logger = logging.getLogger(__name__)


def alternative_json_response(self, result=None, error=None):
    if error is not None:
        response = error
    if result is not None:
        response = result

    mime = 'application/json'
    body = json.dumps(response, default=date_utils.json_default)
    return Response(
        body, status=error and error.pop('http_status', 200) or 200,
        headers=[('Content-Type', mime), ('Content-Length', len(body))]
    )


def common_response(status: int = 500, message: str = '', data=None):
    response_data = {
        'status': status,
        'message': message,
        'data': data
    }
    request._json_response = alternative_json_response.__get__(request, JsonRequest)
    return response_data




