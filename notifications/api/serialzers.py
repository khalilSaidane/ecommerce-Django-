from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField
)
from notifications.models import Notification
from accounts.api.serializers import UserRetrieveSerializer


class NotificationListSerializer(ModelSerializer):
    class Meta:
        model = Notification
        actor = UserRetrieveSerializer()
        target = UserRetrieveSerializer()
        fields = [
            'actor',
            'target',
            'verb',
            'timestamp',
            'is_read',
        ]
