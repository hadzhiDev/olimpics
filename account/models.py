from uuid import uuid4

from django.db import models
from django.utils import timezone

from utils.models import TimeStampAbstractModel

from phonenumber_field.modelfields import PhoneNumberField


class Application(TimeStampAbstractModel):

    class Meta:
        verbose_name = 'заявка'
        verbose_name_plural = 'заявки'
        ordering = ('-created_at',)

    full_name = models.CharField(max_length=250, verbose_name='фамилия и имя')
    phone = PhoneNumberField(max_length=100, unique=True, verbose_name='номер телефона', blank=True, null=True)
    email = models.EmailField(verbose_name='электронная почта', unique=True, blank=False, null=False)
    language = models.ForeignKey('account.ProgramingLanguage', models.PROTECT, verbose_name='язык программирования',
                                 help_text='Выберите язык программирования')
    image = models.ImageField(upload_to='books_images/', verbose_name='фото чека')

    def __str__(self):
        return f'{self.full_name}'


class ProgramingLanguage(TimeStampAbstractModel):

    class Meta:
        verbose_name = 'язык программирования'
        verbose_name_plural = 'языки программирования'
        ordering = ('-created_at',)

    name = models.CharField('название', max_length=200, unique=True)

    def __str__(self):
        return f'{self.name}'


def get_expire_date():
    return timezone.now() + timezone.timedelta(minutes=15)


class SendRequestToEmail(TimeStampAbstractModel):

    class Meta:
        verbose_name = 'запрос для заявка'
        verbose_name_plural = 'запросы для заявки'
        ordering = ('-created_at', '-updated_at')

    application = models.OneToOneField('account.Application', on_delete=models.CASCADE, verbose_name='заявка',
                                       null=True, blank=True)
    key = models.UUIDField(default=uuid4, editable=False)
    expire_date = models.DateTimeField('срок действия', default=get_expire_date)
    is_confirmed = models.BooleanField('подтверждение', default=False)

    def __str__(self):
        return f'{self.application}'

    def is_expired(self):
        return timezone.now() > self.expire_date