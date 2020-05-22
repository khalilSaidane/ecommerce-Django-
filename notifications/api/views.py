from rest_framework import generics
from rest_framework import authentication, permissions
from .serialzers import NotificationListSerializer
from notifications.models import Notification
from rest_framework.views import APIView
from rest_framework.response import Response



class NotificationAPIListView(generics.ListAPIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationListSerializer
    queryset = Notification.objects.all()


class NotificationAPIView(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk=None, format=None):
        notification = Notification.objects.filter(pk=pk).first()
        notification.is_read = True
        notification.save()
        data = {'is_read': True}
        return Response(data)
