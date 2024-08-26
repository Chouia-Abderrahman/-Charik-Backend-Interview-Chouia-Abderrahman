import json
from datetime import datetime


def hubspot_association_serializer(data):
    def serialize(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return str(obj)

    return json.dumps(data, default=serialize, indent=2)