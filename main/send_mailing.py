import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

import pytz

from main.models import Mailing, MailingLog

SENDER_EMAIL = "testdomsaitov123@yandex.ru"
PASSWORD = "cjiuuitudkuqhzot"


def sender_mail():
    now = datetime.datetime.now()
    print(now)
    for mailing in Mailing.objects.filter(status=Mailing.STATUS_STARTED):
        for client in mailing.client.all():
            mailing_log = MailingLog.objects.filter(log_client=client, log_mailing=mailing)
            if mailing_log.exists():
                last_try = mailing_log.order_by('-created_time').first()
                desired_timezone = pytz.timezone('Europe/Moscow')
                last_try_date = last_try.created_time.astimezone(desired_timezone)
                if mailing.PERIOD_DAILY:
                    if (now.date() - last_try_date.date()).days >= 1:
                        sent_mail(mailing, client)
                elif mailing.PERIOD_WEEKLY:
                    if (now.date() - last_try_date.date()).days >= 7:
                        sent_mail(mailing, client)
                elif mailing.PERIOD_MONTHLY:
                    if (now.date() - last_try_date.date()).days >= 30:
                        sent_mail(mailing, client)
            else:
                sent_mail(mailing, client)


def sent_mail(mailing, client):
    """Отправка писем"""
    date_time_now = datetime.datetime.now()
    email = client.mail_client
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['Subject'] = mailing.theme_mess
    msg.attach(MIMEText(mailing.body_mess, 'plain'))

    try:
        # Заполнение письма
        with smtplib.SMTP_SSL('smtp.yandex.ru', 465) as server:
            server.login(SENDER_EMAIL, PASSWORD)
            msg['To'] = email  # почта на которую отправляем
            server.sendmail(SENDER_EMAIL, email, msg.as_string())  # подключаемся к сервреу

            # записываем логи рассылки
            MailingLog.objects.create(
                created_time=date_time_now,
                log_status=MailingLog.STATUS_OK,
                log_client=client,
                log_mailing=mailing,
                response='доставлено',
            )

        # Обработка ошибкаи
    except Exception as e:  # обработка ошибки
        MailingLog.objects.create(
            created_time=date_time_now,
            log_status=MailingLog.STATUS_FAILED,
            log_client=client,
            log_mailing=mailing,
            response=f'Error {e}',
        )


sender_mail()