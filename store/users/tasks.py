import uuid
from datetime import timedelta

from celery import shared_task
from django.utils.timezone import now

from users.models import EmailVerification, User


@shared_task
def send_email_verification(user_id):
    user = User.objects.get(id=user_id)
    expiration = now() + timedelta(hours=24)
    code = uuid.uuid4()
    record = EmailVerification.objects.create(user=user, expiration=expiration, code=code)
    record.send_verification_email()


#celery -A store worker --loglevel=info
