from django.contrib.auth.views import LoginView
from django.urls import path, include
from django.views.decorators.cache import cache_page

from . import views
from .models import Mailing
from .views import MailingListView, MailingCreateView, MailingDeleteView, \
    MailingUpdateView, ClientListView, ClientDeleteView, ClientUpdateView, ClientCreateView, MailingLogListView

# from main.views import

urlpatterns = [
    path('', MailingListView.as_view(), name='index'),
    path('mailinglogs/', MailingLogListView.as_view(), name='logs'),

    path('create/', MailingCreateView.as_view(), name='create_mailing'),
    path('update/<int:pk>', MailingUpdateView.as_view(), name='update_mailing'),
    path('delete/<int:pk>/', MailingDeleteView.as_view(), name='delete'),

    path('create_client/', ClientCreateView.as_view(), name='create_client'),
    path('client_update/<int:pk>', ClientUpdateView.as_view(), name='update_client'),
    path('client_delete/<int:pk>/', ClientDeleteView.as_view(), name='delete_client'),
    path('client/', ClientListView.as_view(), name='client')
]