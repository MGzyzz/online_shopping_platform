from celery import shared_task
from django.utils import timezone

from shop.models import TimeDiscount


@shared_task
def check_expiration():
    discounts = TimeDiscount.objects.all()
    now = timezone.now()

    for discount in discounts:
        end_date = discount.end_date.astimezone(timezone.get_current_timezone())

        if now >= end_date:
            discount.delete()


