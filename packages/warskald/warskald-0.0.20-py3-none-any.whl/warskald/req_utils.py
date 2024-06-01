from flask import request, g, has_request_context
from warskald.utils import parse_str_type
from warskald.attr_dict import AttrDict

def parse_request_data():
    if(has_request_context() and request):
        params = {}
        
        if(request.method == 'GET'):
            for key, value in request.args.items():
                params[key] = parse_str_type(value)
        else:    
            params = request.get_json()
        g.params = AttrDict(params)            
        return g.params