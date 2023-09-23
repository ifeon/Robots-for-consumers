import json
from django.http import JsonResponse

from robots.forms import RobotForm


def create_robot(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        form = RobotForm(data)
        robot_serial = data['model'] + '-' + data['version']
        if form.is_valid():
            robot = form.save(commit=False)
            robot.serial = robot_serial
            form.save()
            return JsonResponse({'message': 'Robot created successfully'})
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method'})
