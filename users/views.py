from django.contrib.auth.models import User
from users.serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from utils.permissions import IsOwnerOrAdmin
from users.services import UserService


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    service = UserService()

    def get_permissions(self):
        if self.action in ["retrieve", "list"]:
            permission_classes = [IsAuthenticated]
        elif self.action in ['create', 'destroy']:
            permission_classes = [IsAdminUser]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsOwnerOrAdmin]
        else:
            permission_classes = []

        return [permission() for permission in permission_classes]
        
    def perform_create(self, serializer):
        serializer.instance = self.service.create_user(**serializer.validated_data)

    def perform_update(self, serializer):
        self.service.update_user(serializer.instance, **serializer.validated_data)