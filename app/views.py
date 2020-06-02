from collections import Counter
from django.shortcuts import render

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter({'original': 0, 'test': 0})
counter_click = Counter({'original': 0, 'test': 0})


def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    from_me = request.GET.get('from-landing')
    if from_me:
        if from_me == 'original':
            counter_click['original'] += 1
        elif from_me == 'test':
            counter_click['test'] += 1
    return render(request, template_name='index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    ab_test_arg = request.GET.get('ab-test-arg')
    tmpl_name = 'landing.html'
    if ab_test_arg:
        if ab_test_arg == 'original':
            counter_show['original'] += 1
        elif ab_test_arg == 'test':
            tmpl_name = 'landing_alternate.html'
            counter_show['test'] += 1
    return render(request, template_name=tmpl_name)


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Чтобы отличить с какой версии лендинга был переход
    # проверяйте GET параметр marker который может принимать значения test и original
    # Для вывода результат передайте в следующем формате:
    try:
        test_conversion = counter_click['test'] / counter_show['test']
        original_conversion = counter_click['original'] / counter_show['original']
    except ZeroDivisionError:
        test_conversion = 0
        original_conversion = 0

    return render(request, template_name='stats.html', context={
        'test_conversion': test_conversion,
        'original_conversion': original_conversion,
    })
