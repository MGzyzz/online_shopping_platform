import httpx as httpx
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from accounts.models import User
from shop.models import Order


@method_decorator(csrf_exempt, name='dispatch')
class Recarring(View):
    def post(self, request, *args, **kwargs):
        for k in request.POST.keys():
            print(f'{k} = {request.POST.get(k)}')
            token = request.POST.get('Token')
            account_id = request.POST.get('AccountId')
            user = User.objects.filter(pk=account_id).first()
            print(user)
            print(account_id)
            print(token)
            order = Order(
                payer_id=account_id,

            )
            httpx.post(
                'https://api.cloudpayments.ru/payments/void',
                auth=('pk_3d2e6006deeae8feba63160d9efd2', '6bdcf4e0a6dd4adb7f2671a524deaa38'),
                json={'TransactionId': request.POST.get('TransactionId')},
            )

            return HttpResponse(status=201)

        return HttpResponse(status=201)