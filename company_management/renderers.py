from rest_framework import renderers
import json
from rest_framework import status


class UserRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''
        message = renderer_context.get('message', '')
        status_code = renderer_context.get('status', status.HTTP_200_OK)
        success = renderer_context.get('success', True)
        
        if 'ErrorDetail' in str(data):
            response = json.dumps({ 'status': status.HTTP_400_BAD_REQUEST, 'success': False , 'errors': data})
        else:
            response = json.dumps(data)
        
        return response
    

