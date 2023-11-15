from django.contrib.auth import views, login, get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView

from accounts.forms import RegisterForm, LoginForm, UserUpdateForm, PasswordChangeForm
from accounts.models import User


class LoginView(views.LoginView):
    template_name = 'main.html'
    form_class = LoginForm

    def get_success_url(self):
        return reverse('home')

    def form_invalid(self, form):
        self.request.session['dropdown'] = 'show'
        return render(self.request, 'main.html', {'form': form})


class Logout(views.LogoutView):
    def get_next_page(self):
        return self.request.META.get('HTTP_REFERER')


class RegisterView(CreateView):
    template_name = 'register.html'
    model = User
    form_class = RegisterForm

    def form_valid(self, form):
        phone_number = form.cleaned_data.get('phone')
        self.request.session['phone'] = phone_number
        self.request.session['user_data'] = form.cleaned_data

        return redirect('sms-verification')

    def form_invalid(self, form):
        return render(self.request, 'register.html', {'form': form})


class Sms_Verification(TemplateView):
    template_name = 'sms.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        phone_number = self.request.session.get('phone', 'Неизвестный номер')
        context['phone_number'] = phone_number
        return context

    def post(self, request, *args, **kwargs):
        code_1 = request.POST.get('code_1')
        code_2 = request.POST.get('code_2')
        code_3 = request.POST.get('code_3')
        code_4 = request.POST.get('code_4')

        input_code = f"{code_1}{code_2}{code_3}{code_4}"
        if input_code == '4444':
            user_data = self.request.session.get('user_data')
            password = user_data.pop('password1')
            user_data.pop('password2', None)
            user = User(**user_data)
            user.set_password(password)
            user.save()
            login(self.request, user)

        return redirect('home')


class UserUpdate(UpdateView):
    model = get_user_model()
    form_class = UserUpdateForm
    template_name = 'update-user.html'
    pk_url_kwarg = 'id'
    context_object_name = 'user'

    def test_func(self):
        return self.request.user == self.get_object()

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'id': self.request.user.id})


class PasswordChangeView(UpdateView):
    model = get_user_model()
    template_name = 'change-password.html'
    form_class = PasswordChangeForm
    context_object_name = 'user'
    pk_url_kwarg = 'id'

    def get_success_url(self):
        return reverse('profile', kwargs={'id': self.request.user.id})
