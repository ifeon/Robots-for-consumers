import json
from django.http import JsonResponse

from orders.forms import OrderCreateForm
from orders.models import OrderQueue
from robots.models import Robot


def order_create(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        form = OrderCreateForm(data)
        if form.is_valid():
            order_serial = form.cleaned_data['robot_serial']
            if Robot.objects.filter(serial=order_serial).exists():
                form.save()
                return JsonResponse({'message': 'Order added'})
            else:
                customer_id = form.cleaned_data['customer']
                OrderQueue.objects.create(robot_serial=order_serial, customer=customer_id)
                return JsonResponse({'message': 'Order queue'})
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method'})

