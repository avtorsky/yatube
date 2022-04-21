from django.shortcuts import render

ERROR_400_TEXT = 'Ошибка в запросе к HTTP-серверу'
ERROR_403_TEXT = 'Доступ к странице ограничен'
ERROR_404_TEXT = 'Страница не найдена'
ERROR_500_TEXT = 'Ошибка обработки запроса на сервере'


def bad_request(request, exception):
    return render(
        request,
        'core/400.html',
        {'path': request.path, 'text': ERROR_400_TEXT},
        status=400,
    )


def permission_denied(request, exception):
    return render(
        request,
        'core/403.html',
        {'path': request.path, 'text': ERROR_403_TEXT},
        status=403,
    )


def csrf_error(request, reason=''):
    return render(
        request,
        'core/403.html',
        {'path': request.path, 'text': ERROR_403_TEXT},
    )


def page_not_found(request, exception):
    return render(
        request,
        'core/404.html',
        {'path': request.path, 'text': ERROR_404_TEXT},
        status=404,
    )


def server_error(request):
    return render(
        request, 'core/500.html', {'text': ERROR_500_TEXT}, status=500
    )
