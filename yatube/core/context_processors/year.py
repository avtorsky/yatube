import datetime

current_time = datetime.datetime.now()


def year(request):
    """Добавляет переменную с текущим годом."""
    return {'year': current_time.year}
