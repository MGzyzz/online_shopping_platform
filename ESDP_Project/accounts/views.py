from django.contrib.auth import views, login
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView

from accounts.forms import RegisterForm, LoginForm
from accounts.models import User


# Create your views here.
class LoginView(views.LoginView):
    template_name = 'login.html'
    form_class = LoginForm

    def get_success_url(self):
        return redirect('home')

    def form_invalid(self, form):
        return render(self.request, 'login.html', {'form': form})




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