from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import DetailView
from accounts.models import User
from shop.models import *


class Profile(PermissionRequiredMixin, DetailView):
    template_name = 'profile/profile.html'
    context_object_name = 'user'
    model = User
    pk_url_kwarg = 'id'

    def has_permission(self):
        return self.request.user == self.get_object()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shops = Shop.objects.filter(user_id=self.kwargs['id'])
        context['shops'] = shops
        return context
