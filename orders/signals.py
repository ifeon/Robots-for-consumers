from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.models import OrderQueue
from robots.models import Robot


@receiver(post_save, sender=Robot)
def check_robot_in_queue(sender, instance, created, **kwargs):
    if created:
        orders = OrderQueue.objects.all()
        for order in orders:
            if order.robot_serial == instance.serial and order.message_status is not True:
                send_mail(
                    f'Робот {instance.serial} появился в наличии!',
                    'Добрый день!'
                    f'Недавно вы интересовались нашим роботом модели {instance.model}, версии {instance.version}.'
                    'Этот робот теперь в наличии.Если вам подходит этот вариант - пожалуйста, свяжитесь с нами',
                    settings.EMAIL_HOST_USER,
                    [order.customer.email],
                    fail_silently=False,
                )
                order.message_status = True
                order.save()
                break
