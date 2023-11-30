from django.contrib.auth.hashers import make_password
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import User
from users.serializers import UserSerializer


class UserViewSet(viewsets.GenericViewSet,
                  mixins.CreateModelMixin):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        password = make_password(serializer.validated_data.pop('password'))
        serializer.save(password=password)

    @action(detail=False, methods=('get',),
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(data=serializer.data, status=200)
