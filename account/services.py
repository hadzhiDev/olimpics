from django.conf import settings
from django.core.mail import send_mail
from django.utils.html import strip_tags

from account.models import SendRequestToEmail
from urllib.parse import urlencode


class SendRequestToEmailManager:

    def __init__(self, application):
        self.application = application
        self.payload = SendRequestToEmail.objects.get_or_create(application=self.application)[0]
        if self.payload.is_expired():
            self.payload.delete()
            self.payload = SendRequestToEmail.objects.get_or_create(application=self.application)[0]

    def _make_link(self):
        key = self.payload.key
        queries = urlencode({'key': key})
        front_host = settings.FRONT_HOST
        email_confirm_link = settings.CONFIRM_REQUEST_EMAIL
        return f'https://olimpics.pythonanywhere.com/api/v1/auth/confirm-request-to-application/?{queries}'

    def send_key(self):
        link = self._make_link()
        subject, to, from_email = 'Reset Password | Hadzhi.kg', self.application.email, settings.EMAIL_HOST_USER
        html_message = f'this is a  <a href="{link}">link</a> to reset password'
        plain_message = strip_tags(html_message)

        send_mail(
            subject,
            plain_message,
            from_email,
            [to],
            html_message=plain_message
        )

    def confirm(self, key: str, is_confirmed: bool) -> bool:
        real_key = self.payload.key
        application = self.application
        if real_key == key and is_confirmed:
            application.is_confirmed = True
            application.save()
            self.payload.delete()
            return True
        return False