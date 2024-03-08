from rest_framework import renderers
import json
from rest_framework import status


class ErrorRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''
        message = renderer_context.get('message', '')
        status_code = renderer_context.get('status', status.HTTP_200_OK)
        success = renderer_context.get('success', True)
        print("---data---", renderer_context['request'].data)
        request_data = renderer_context['request'].data if renderer_context and renderer_context['request'] else {}
        if 'ErrorDetail' in str(data):
            if request_data.get('password') != request_data.get('confirm_password'):
                data['password_not_match'] = ["Password and Confirm Password don't match"]
            response = json.dumps({ 'status': status.HTTP_400_BAD_REQUEST, 'success': False , 'errors': data})
        else:
            response = json.dumps(data)
        
        return response
    

