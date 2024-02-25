from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from account.utils import is_manager_user
from account.models import Seat
from account.serializers import SeatSerializer


class IsManager(permissions.BasePermission):
    """
    Allows access only to Manager.
    """

    def has_permission(self, request, view):
        return bool(is_manager_user(request.user))


class UserSeatsView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsManager]
    serializer_class = SeatSerializer
    queryset = Seat.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields  = ['id', 'user']
