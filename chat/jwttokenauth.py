from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from channels.auth import AuthMiddlewareStack
from django.db import close_old_connections
from django.contrib.auth.models import AnonymousUser


class JwtTokenAuthMiddleware:
    """
    JWT token authorization middleware for Django Channels 2
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        headers = dict(scope['headers'])
        print(headers)
        try:
            token_header = dict(scope['headers'])[b'authorization'].decode().split()
            data = {'token': token_header[1]}
            print(data)
            valid_data = VerifyJSONWebTokenSerializer().validate(data)
            print(valid_data)
            user = valid_data['user']
            scope['user'] = user
        except:
            pass
        return self.inner(scope)


TokenAuthMiddleWareStack = lambda inner: JwtTokenAuthMiddleware(AuthMiddlewareStack(inner))