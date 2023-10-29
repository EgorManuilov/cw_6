from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
import random

from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


# Create your views here.
class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        new_user = form.save()
        activ_pass = ''.join(str(random.randint(0, 9)) for _ in range(6))

        # Запишите сгенерированный код в поле key_active модели User
        new_user.key_active = activ_pass
        new_user.save()

        send_mail(
            subject='Вы зарегестрировались на сервисе',
            message=f'Нужно срочно пройти авторизацию Ваш код {activ_pass}'
                    f'\nВаш код {activ_pass}, введите в личном кабинете',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
        )
        return super().form_valid(form)


class ProfileView(UpdateView, LoginRequiredMixin):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        kod_active_true = request.POST.get('kod_active')
        print(kod_active_true)
        print(request.user.key_active)
        if request.user.key_active == kod_active_true:
            # Если введенный код совпадает с key_active пользователя,
            # активируем пользователя
            request.user.user_active = True
            request.user.save()

            return redirect('users:profile')

        else:
            return redirect('users:profile')


def generate_new_password(request):
    new_password = ''.join(str(random.randint(0, 9)) for _ in range(6))
    send_mail(
        subject='Изменение пароля',
        message=f'Ваш новый пароль {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse_lazy('users:login'))

