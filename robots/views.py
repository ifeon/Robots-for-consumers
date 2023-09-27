import json
from django.http import JsonResponse, FileResponse

from R4C.services import robots_for_the_period, dict_to_excel
from robots.forms import RobotForm


def create_robot(request):
    """Добавление робота в базу"""
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


def download_report(request):
    """Скачивание отчета за неделю"""
    robots = robots_for_the_period()
    dict_to_excel(robots, 'media/')
    excel_file = open('media/robots.xlsx', 'rb')
    response = FileResponse(excel_file)
    response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response['Content-Disposition'] = 'attachment; filename="robots.xlsx"'
    return response
