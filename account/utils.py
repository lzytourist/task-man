from account.models import Notification


def send_notification(by, to, message):
    Notification.objects.create(
        generated_by=by,
        message=message,
        user=to
    )

    # TODO: send via websocket