from datetime import datetime, date

from flask import json

from core.service.types import DATETIME_FORMAT_NICE


class JsonEncoder(json.JSONEncoder):
    """Encode JSONs with nice datetimes."""
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.strftime(DATETIME_FORMAT_NICE)
        return json.JSONEncoder.default(self, obj)
