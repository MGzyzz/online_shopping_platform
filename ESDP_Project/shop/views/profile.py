from django.urls import reverse
from django.views.generic import DetailView
from accounts.models import User
from shop.models import *

class Profile(DetailView):
    template_name = 'profile/profile.html'
    context_object_name = 'user'
    model = User
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shops = Shop.objects.filter(user_id=self.request.user.id)
        context['shops'] = shops
        print(shops)
        return context
