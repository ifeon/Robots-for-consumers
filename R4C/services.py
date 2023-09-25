from django.utils import timezone
import xlsxwriter

from robots.models import Robot


def robots_for_the_period():
    """Берем текущий день с 00:00, чтобы не показывать роботов за сегодня"""
    end_date = timezone.now()
    end_date = end_date.replace(hour=0, minute=0, second=0, microsecond=0)
    start_date = end_date - timezone.timedelta(days=7)

    """Получаем все объекты модели Robot, созданные за последнюю неделю"""
    robots = Robot.objects.filter(created__gte=start_date, created__lte=end_date)

    manufactured_robots = {}
    for robot in robots:
        if robot.model not in manufactured_robots:
            manufactured_robots[robot.model] = {}
        if robot.version not in manufactured_robots[robot.model]:
            manufactured_robots[robot.model][robot.version] = 1
        else:
            manufactured_robots[robot.model][robot.version] += 1

    return manufactured_robots


def dict_to_excel(robot_dictionary, path):
    """Из словаря делаем excel файл"""
    workbook = xlsxwriter.Workbook(path + 'robots.xlsx')
    for model in robot_dictionary.keys():
        worksheet = workbook.add_worksheet(model)
        worksheet.set_column(2, 2, 20)
        worksheet.write(0, 0, 'Модель')
        worksheet.write(0, 1, 'Версия')
        worksheet.write(0, 2, 'Количество за неделю')
        row = 1
        for version, count in robot_dictionary[model].items():
            worksheet.write(row, 0, model)
            worksheet.write(row, 1, version)
            worksheet.write(row, 2, count)
            row += 1
    workbook.close()
