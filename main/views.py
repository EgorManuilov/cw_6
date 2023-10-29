from random import sample

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from pytils.translit import slugify
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from blog.models import Blog
from main.models import Client, Mailing, MailingLog


# Create your views here.
class MailingListView(ListView):
    """Показывает все рассылки"""
    model = Mailing
    template_name = 'main/index.html'
    context_object_name = 'object'

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        if user.groups.filter(name='manager').exists() or user.is_superuser:
            queryset = super().get_queryset()
        else:
            queryset = super().get_queryset().filter(
                owner=user.pk
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailing_count = Mailing.objects.count()
        context['mailing_count'] = mailing_count

        active_mailings = Mailing.objects.filter(status='created').count()
        context['active_mailings'] = active_mailings

        unique_clients = Client.objects.count()
        context['unique_clients'] = unique_clients

        blogs = Blog.objects.filter(publ_on_off=True)
        all_post = list(blogs)
        if len(all_post) >= 3:
            blog_list = sample(list(blogs), 3)
            context['blog_list'] = blog_list

        else:
            blog_list = all_post
            context['blog_list'] = blog_list

        return context


class MailingCreateView(CreateView, LoginRequiredMixin):
    """Класс для создания рассылки"""
    model = Mailing
    fields = ('name_mailing', 'theme_mess', 'body_mess', 'frequency', 'send_time')
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.name_mailing)
            new_mat.save()

        return super().form_valid(form)


class MailingDeleteView(DeleteView, LoginRequiredMixin):
    """Класс для удаления рассылки"""
    model = Mailing
    success_url = reverse_lazy('index')


class MailingUpdateView(UpdateView, LoginRequiredMixin):
    """Класс для изменения рассылки"""
    model = Mailing
    fields = ('status', 'name_mailing', 'theme_mess', 'body_mess', 'frequency', 'send_time', 'client')
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.name_mailing)
            new_mat.save()

        return super().form_valid(form)


class ClientListView(ListView, LoginRequiredMixin):
    """Вывод всех клиентов на странице"""
    model = Client
    template_name = 'main/client.html'

    def get_queryset(self):
        user = self.request.user
        if not user:
            queryset = None
        if user.is_superuser:
            queryset = super().get_queryset()
        else:
            queryset = super().get_queryset().filter(
                client_owner=user.pk
            )
        return queryset


class ClientDeleteView(DeleteView, LoginRequiredMixin):
    """Класс удаления клиентов для рассылок"""
    model = Client
    success_url = reverse_lazy('client')

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        if user.groups.filter(name='manager').exists() or user.is_superuser:
            queryset = super().get_queryset()
        else:
            queryset = super().get_queryset().filter(
                mailing_owner=user.pk
            )
        return queryset


class ClientUpdateView(UpdateView, LoginRequiredMixin):
    """Класс изменения клиентов для рассылок"""
    model = Client
    fields = ('mail_client', 'name_client', 'first_name_client', 'last_name_client')
    success_url = reverse_lazy('client')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.mail_client)
            new_mat.save()

        return super().form_valid(form)


class ClientCreateView(CreateView, LoginRequiredMixin):
    """Класс создания клиентов для рассылок"""
    model = Client
    fields = ('mail_client', 'name_client', 'first_name_client', 'last_name_client')
    success_url = reverse_lazy('client')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.mail_client)
            new_mat.save()

        return super().form_valid(form)


class MailingLogListView(ListView):
    """Показывает все логи"""
    model = MailingLog
    template_name = 'main/mailinglogs.html'
    context_object_name = 'object'

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            queryset = super().get_queryset()
        else:
            queryset = super().get_queryset().filter(
                log_mailing=user.pk
            )
        return queryset
