from django.contrib.auth import views, login, get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from accounts.forms import RegisterForm, LoginForm, UserUpdateForm, PasswordChangeForm
from accounts.models import User


# Create your views here.
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
        user = form.save()
        login(self.request, user)
        return redirect('home')

    def form_invalid(self, form):
        return render(self.request, 'register.html', {'form': form})


class UserUpdate(UpdateView):
    model = get_user_model()
    form_class = UserUpdateForm
    template_name = 'update-user.html'
    pk_url_kwarg = 'id'
    context_object_name = 'user'

    def test_func(self):
        return self.request.user == self.get_object()

    def get_success_url(self):
        return reverse_lazy('home')


class PasswordChangeView(UpdateView):
    model = get_user_model()
    template_name = 'change-password.html'
    form_class = PasswordChangeForm
    context_object_name = 'user'
    pk_url_kwarg = 'id'

    def get_success_url(self):
        return reverse('home')
