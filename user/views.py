from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from user.models import User
from user.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['GET'], detail=False)
    def me(self, request):
        return Response(self.get_serializer(self.request.user).data)
