from django.urls import path

from robots import views

app_name = 'robots'

urlpatterns = [
    path('', views.create_robot, name='create_robot'),
]
