from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now


class User(AbstractUser):  # наследуемся от существующего класса и через upload_to добавляем новое необязательное поле
    image = models.ImageField(upload_to="users_images/", blank=True, null=True)
    is_verified_email = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True,)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    class Meta:
        verbose_name_plural = 'Верификация почты'

    def __str__(self):
        return 'EmailVerification for {self.user.email}'

    def send_verification_email(self):
        link = reverse("users:email_verification", kwargs={"code": self.code, "email": self.user.email})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Подтверждение учетной записи для {self.user.username}'
        message = 'Для подтверждения учетной записи для {} перейдите по ссылке: {}'.format(
            self.user.email,
            verification_link
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        return now() >=self.expiration
