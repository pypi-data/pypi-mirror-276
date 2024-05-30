import re

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


def validate_phone_number(value):
    """Валидация номера телефона """
    # regex = r"^\+?[78]\d{10}$"
    regex = r"^\+\d\(\d{3}\)-\d{3}-\d{2}-\d{2}$"
    if not re.match(regex, value):
        raise ValidationError('Неверный формат номера телефона.')


class User(AbstractUser):
    number = models.CharField('Номер телефона', max_length=15, validators=[validate_phone_number])
    test = models.CharField('Тестовое поле', max_length=15, default="")

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Car(models.Model):
    brand = models.CharField("Марка авто", max_length=40)
    model = models.CharField("Модель авто", max_length=60)
    description = models.CharField("Описание авто", max_length=255)

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'


class Order(models.Model):
    STATUSES = (
        (0, 'Новое'),
        (1, 'Отклонено'),
        (2, 'Подтверждено')
    )

    user_creator = models.ForeignKey(User, verbose_name='Создатель заявления', on_delete=models.PROTECT, default=1)
    car = models.ForeignKey(Car, verbose_name="Выбранное авто", on_delete=models.PROTECT)
    status = models.IntegerField('Статус заявления', choices=STATUSES, default=0)

    class Meta:
        verbose_name = 'Заявление'
        verbose_name_plural = 'Заявления'
