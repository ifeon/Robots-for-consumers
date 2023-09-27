from django.forms import ModelForm

from orders.models import Order


class OrderCreateForm(ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'robot_serial']