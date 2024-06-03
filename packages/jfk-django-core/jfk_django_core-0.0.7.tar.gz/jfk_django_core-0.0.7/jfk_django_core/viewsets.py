import logging

from django.db.models import Q
from django.contrib.auth.models import User

from rest_framework import permissions, viewsets
from . import serializers

log = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        return super().get_queryset().filter(id=self.request.user.id)