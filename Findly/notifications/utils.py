from .models import Notification


def notify(user, verb: str, link: str = "") -> Notification:
    return Notification.objects.create(user=user, verb=verb, link=link)

