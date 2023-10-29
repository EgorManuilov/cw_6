from django.db import models

from config import settings


class Client(models.Model):
    """Модель клиента для рассылки"""
    mail_client = models.CharField(max_length=25, verbose_name='Почта клиента')
    name_client = models.CharField(max_length=20, verbose_name='Имя клиента')
    first_name_client = models.CharField(max_length=20, verbose_name='Фамилия клиента', null=True, blank=True)
    last_name_client = models.CharField(max_length=20, verbose_name='Отчество клиента', null=True, blank=True)

    client_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='владелец',
                                     null=True, blank=True)

    def __str__(self):
        return f"Клиент: Ф-{self.name_client} И-{self.first_name_client} О-{self.last_name_client}.Письмо отправляем на {self.mail_client}"

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Mailing(models.Model):
    """Модель рассылки, время, периодичность, статус"""
    PERIOD_DAILY = 'daily'
    PERIOD_WEEKLY = 'weekly'
    PERIOD_MONTHLY = 'monthly'

    PERIODS = (
        (PERIOD_DAILY, 'Ежедневная'),
        (PERIOD_WEEKLY, 'Раз в неделю'),
        (PERIOD_MONTHLY, 'Раз в месяц'),
    )

    STATUS_CREATED = 'created'
    STATUS_STARTED = 'started'
    STATUS_DONE = 'done'
    STATUSES = (
        (STATUS_STARTED, 'Запущена'),
        (STATUS_CREATED, 'Создана'),
        (STATUS_DONE, 'Завершена'),
    )

    send_time = models.TimeField(auto_now_add=False, default='Время в формате Ч:М', verbose_name='Время рассылки')
    frequency = models.CharField(max_length=20, choices=PERIODS, verbose_name='Периодичность рассылки')
    status = models.CharField(max_length=20, choices=STATUSES, default=STATUS_CREATED, verbose_name='Статус рассылки')

    name_mailing = models.CharField(max_length=15, verbose_name='Название рассылки')
    theme_mess = models.CharField(max_length=200, verbose_name='Тема письма')
    body_mess = models.TextField(verbose_name='Тело письма')

    # Зависимость от владельца продукта
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='владелец', null=True,
                              blank=True)

    client = models.ManyToManyField(Client)

    def __str__(self):
        return (f"Рассылка #{self.pk}. Время отправки- {self.send_time} "
                f"Периодичность- {self.frequency}. Статутс {self.status}"
                f"Название рассылки - {self.name_mailing}")

    class Meta:
        verbose_name_plural = "Рассылки"


class MailingLog(models.Model):
    """Модель логов рассылки"""

    STATUS_OK = 'ok'
    STATUS_FAILED = 'failed'
    STATUSES = (
        (STATUS_OK, 'Успешно'),
        (STATUS_FAILED, 'Ошибка'),
    )

    created_time = models.DateTimeField(auto_now_add=True, verbose_name='дата и время последней попытки')
    log_status = models.CharField(max_length=20, choices=STATUSES, verbose_name='статус попытки')
    log_client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='подписчик')
    log_mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='рассылка')
    response = models.TextField(null=True,
                                blank=True, verbose_name='ответ сервера')

    def __str__(self):
        return f"{self.log_client} - {self.log_mailing} ({self.log_status}) в {self.created_time}"

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'
