# Generated by Django 4.2.6 on 2023-10-29 12:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mail_client', models.CharField(max_length=25, verbose_name='Почта клиента')),
                ('name_client', models.CharField(max_length=20, verbose_name='Имя клиента')),
                ('first_name_client', models.CharField(blank=True, max_length=20, null=True, verbose_name='Фамилия клиента')),
                ('last_name_client', models.CharField(blank=True, max_length=20, null=True, verbose_name='Отчество клиента')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('send_time', models.TimeField(default='Время в формате Ч:М', verbose_name='Время рассылки')),
                ('frequency', models.CharField(choices=[('daily', 'Ежедневная'), ('weekly', 'Раз в неделю'), ('monthly', 'Раз в месяц')], max_length=20, verbose_name='Периодичность рассылки')),
                ('status', models.CharField(choices=[('started', 'Запущена'), ('created', 'Создана'), ('done', 'Завершена')], default='created', max_length=20, verbose_name='Статус рассылки')),
                ('name_mailing', models.CharField(max_length=15, verbose_name='Название рассылки')),
                ('theme_mess', models.CharField(max_length=200, verbose_name='Тема письма')),
                ('body_mess', models.TextField(verbose_name='Тело письма')),
                ('client', models.ManyToManyField(to='main.client')),
            ],
            options={
                'verbose_name_plural': 'Рассылки',
            },
        ),
        migrations.CreateModel(
            name='MailingLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='дата и время последней попытки')),
                ('log_status', models.CharField(choices=[('ok', 'Успешно'), ('failed', 'Ошибка')], max_length=20, verbose_name='статус попытки')),
                ('response', models.TextField(blank=True, null=True, verbose_name='ответ сервера')),
                ('log_client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.client', verbose_name='подписчик')),
                ('log_mailing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.mailing', verbose_name='рассылка')),
            ],
            options={
                'verbose_name': 'лог',
                'verbose_name_plural': 'логи',
            },
        ),
    ]
