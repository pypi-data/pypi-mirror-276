from flask import request, g, has_request_context
from warskald.utils import parse_str_type
from warskald.attr_dict import AttrDict

def parse_request_data():
    if(has_request_context() and request):
        request_data = {}
        
        if(request.method == 'GET'):
            for key, value in request.args.items():
                request_data[key] = parse_str_type(value)
        else:    
            request_data = request.get_json()
        g.request_data = AttrDict(request_data)            
        return g.request_data