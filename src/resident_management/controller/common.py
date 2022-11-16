import ast
import json
import datetime
import logging
from werkzeug.wrappers import Request, Response

_logger = logging.getLogger(__name__)


def common_response(status='404', message='', data=[]):
    # headers_json = {'Content-Type': 'application/json'}
    response_data = {
        'status': status,
        'message': message,
        'data': data
    }
    # return Response(json.dumps(response_data), headers=headers_json)
    return response_data


def extract_arguments(limit="80", offset=0, order="id", domain="", fields=[]):
    """Parse additional data  sent along request."""
    limit = int(limit)
    expresions = []
    if domain:
        expresions = [tuple(preg.replace(":", ",").split(",")) for preg in domain.split(",")]
        expresions = json.dumps(expresions)
        expresions = json.loads(expresions, parse_int=True)
    if fields:
        fields = fields.split(",")

    if offset:
        offset = int(offset)
    return [expresions, fields, offset, limit, order]
