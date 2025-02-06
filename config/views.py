from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

def redirect_to_api_root(request):
    return redirect('api-root')

class APIRoot(APIView):
    def get(self, request, format=None):
        return Response({
            'users': reverse('user-list', request=request, format=format),
            'conversations': reverse('conversation-list', request=request, format=format),
            'messages': reverse('message-list', request=request, format=format),
            'auth': {
                'register': reverse('register', request=request, format=format),
                'login': reverse('token_obtain_pair', request=request, format=format),
                'refresh': reverse('token_refresh', request=request, format=format),
            }
        })

