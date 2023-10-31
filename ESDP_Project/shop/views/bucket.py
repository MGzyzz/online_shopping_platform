from django.views.generic import ListView

from shop.models import Bucket


class BucketListView(ListView):
    template_name = 'shop/bucket.html'
    model = Bucket
    context_object_name = 'bucket'
