from datetime import datetime

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.utils.logger import Logg
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
        Logg.info(e='user.test', msg='test method', success=True, now=_now)
        return Response({'success': True, 'now': _now})
