from .models import Notification


def get_notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(target=request.user)
        new_notifications_count = notifications.filter(is_read=False).count()
        if new_notifications_count > 0:
            return {'notifications': notifications[:30], 'new_notifications_count': new_notifications_count}
        else:
            return {'notifications': notifications}
    else:
        return {}
