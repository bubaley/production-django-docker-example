from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import viewsets, mixins

from user.serializers import UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ReadOnlyModelViewSet, mixins.UpdateModelMixin, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]

    # def get_permissions(self):
    #     if self.action in ('update', 'destroy', 'list', 'retrieve'):
    #         permission_classes = [IsAdminUser]
    #     elif self.action in 'create':
    #         permission_classes = []
    #     else:
    #         permission_classes = [IsAuthenticated]
    #     return [permission() for permission in permission_classes]

    @action(methods=['GET'], detail=False)
    def me(self, request):
        return Response(self.get_serializer(self.request.user).data)
