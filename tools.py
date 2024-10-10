import json
from datetime import date, datetime, time

from django.db.models.fields import Field
from django.forms.models import model_to_dict

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        elif isinstance(obj, time):
            return obj.strftime('%H:%M:%S')
        return super().default(obj)
    
def is_ajax(request):
     return request.headers.get('x-requested-with') == 'XMLHttpRequest'

def decodeRequest(request):
    try:
        requestBody = json.loads(request.body)
        return requestBody
    except json.JSONDecodeError:
        print(json.JSONDecodeError)

def model_to_dict_verbose(instance):
    data = model_to_dict(instance)

    verbose_data = {}
    for field in instance._meta.fields:
        if isinstance(field, Field):
            verbose_name = field.verbose_name.title()
            original_name = field.name
            if original_name in data:
                verbose_data[verbose_name] = data[original_name]
    return verbose_data
