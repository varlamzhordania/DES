from rest_framework.generics import RetrieveAPIView
from rest_framework import permissions
from .models import User
from .serializers import UserSerializer


class UserDetail(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
