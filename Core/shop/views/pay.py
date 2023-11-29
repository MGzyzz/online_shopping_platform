from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from accounts.models import User, Account
from shop.models import Order, Bucket


@method_decorator(csrf_exempt, name='dispatch')
class Pay(View):
    def post(self, request, *args, **kwargs):
        account_id = request.POST.get('AccountId')
        token = request.POST.get('Token')
        if account_id and token:
            account = Account.objects.get(id=account_id)
            account.token = token
            account.save()

        order_id = request.POST.get('InvoiceId')
        order = Order.objects.get(id=order_id)
        order.is_paid = True
        order.save()
        return JsonResponse({'code':0})