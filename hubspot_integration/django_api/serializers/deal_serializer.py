import json
from datetime import datetime


def hubspot_deal_serializer(data):
    def serialize(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return str(obj)

    serialized_data = {
        'id': data['id'],
        'archived': data['archived'],
        'archived_at': serialize(data['archived_at']),
        'created_at': serialize(data['created_at']),
        'updated_at': serialize(data['updated_at']),
        'properties': data['properties'],
        'properties_with_history': data['properties_with_history']
    }

    return json.dumps(serialized_data, default=serialize, indent=2)