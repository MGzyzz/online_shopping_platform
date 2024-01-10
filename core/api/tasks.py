import redis
from celery import shared_task
from django.utils import timezone

from shop.models import TimeDiscount


def delete_keys_with_prefix(redis_client, prefix):
    keys_to_delete = redis_client.keys(f'{prefix}*')
    for key in keys_to_delete:
        redis_client.delete(key)


@shared_task
def check_expiration():
    discounts = TimeDiscount.objects.all()
    now = timezone.now()

    for discount in discounts:
        end_date = discount.end_date.astimezone(timezone.get_current_timezone())

        if now >= end_date:
            discount.delete()


@shared_task
def cleanup_old_task_metadata():
    redis_client = redis.StrictRedis(host='redis', port=6379, db=0)
    keys_to_delete = redis_client.keys('celery-task-meta-*')

    for key in keys_to_delete:
        redis_client.delete(key)

