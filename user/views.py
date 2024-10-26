from datetime import datetime

from loguru import logger
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from user.models import User
from user.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ('me',):
            return [IsAuthenticated()]
        return []

    @action(methods=['GET'], detail=False)
    def me(self, request):
        return Response(self.get_serializer(self.request.user).data)

    @action(methods=['GET'], detail=False)
    def test(self, request):
        _now = str(datetime.now())
        logger.info({'event': 'USER.TEST', 'now': _now})
        return Response({'success': True, 'now': _now})
