import urllib
from django.views.decorators.csrf import csrf_protect
from django.apps import apps
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from matplotlib import pyplot as plt
from catdogsite import settings
from catdogsite.settings import STATIC_ROOT
from .forms import *
from .models import *
from imageai.Classification.Custom import CustomImageClassification
from PIL import Image
import json
import matplotlib
import matplotlib.pyplot as plt


# Create your views here.

matplotlib.use('Agg')  # Используем фоновый режим Matplotlib


menu = [
        {'title':'Главная', 'name':'home'},
        {'title': 'Распознать изображение', 'name': 'recognize'},
        {'title': 'Cтатистика', 'name': 'stats'},
        {'title': 'Техническая информация', 'name': 'about'},
        {'title': 'Обратная связь', 'name': 'feedback'}
        ]



def main(request):
    return render(request, 'recognizer/main.html', {'menu': menu})

def about(request):
    return render(request, 'recognizer/about.html', { 'menu': menu})

from django.db.models import Count

def stats(request):
    # Получаем статистику для классификатора
    recognizer_stat = Data.objects.values('class_by_recognizer').annotate(count=Count('class_by_recognizer')).order_by('class_by_recognizer')

    # Получаем статистику для пользователей
    user_stat = Data.objects.values('class_by_user').annotate(count=Count('class_by_user')).order_by('class_by_user')

    # Преобразуем QuerySet в словари
    recognizer_stat_dict = {item['class_by_recognizer']: item['count'] for item in recognizer_stat}
    user_stat_dict = {item['class_by_user']: item['count'] for item in user_stat}

    # Сохраняем статистику в сессии
    request.session['user_stat'] = user_stat_dict
    request.session['recognizer_stat'] = recognizer_stat_dict

    return render(request, 'recognizer/stats.html', {
        'menu': menu,
        'user_stat': user_stat_dict,
        'recognizer_stat': recognizer_stat_dict,
    })

def show_stats(request):
    user_stat = request.session.get('user_stat')
    recognizer_stat = request.session.get('recognizer_stat')
    chart_path_user = ''
    chart_path_recognizer = ''

    def create_pie_chart_for_users(data):
        # Извлекаем метки и размеры из данных
        labels = data.keys()
        sizes = data.values()

        # Настройка цветов
        colors = ['tomato', 'cornflowerblue', 'gold', 'orchid', 'green', '#00fdff']

        # Настройка текста внутри диаграммы
        textprops = {'fontsize': 8, 'color': 'black', 'weight': 'bold'}

        # Создаем новый графический объект и подготавливаем круговую диаграмму
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.pie(sizes,
               labels=labels,
               autopct=lambda p: f'{p:.1f}%, ({p * sum(sizes) / 100.0 :.0f})',
               startangle=90,
               textprops=textprops,
               colors=colors,
               )

        # Устанавливаем равное соотношение осей для круговой диаграммы
        ax.axis('equal')

        # Устанавливаем заголовок диаграммы
        ax.set_title(f'Статистика по пользователям (Всего: {Data.objects.count()} записей).', fontsize=14,
                     fontweight='bold', fontstyle='italic')

        # Определяем путь для сохранения графика
        nonlocal chart_path_user
        if settings.DEBUG:
            chart_path_user = 'E:\cat_vs_dog_project\catdogsite\static_debug\\recognizer\images\stat_user.png'
        else:
            chart_path_user = STATIC_ROOT + 'recognizer\\images\\stat_user.png'

        # Сохраняем график
        fig.savefig(chart_path_user)
        plt.close(fig)

    def create_pie_chart_for_recognizer(data):
        # Извлекаем метки и размеры из данных
        labels = data.keys()
        sizes = data.values()

        # Настройка цветов
        colors = ['tomato', 'cornflowerblue', 'gold', 'orchid', 'green', '#00fdff']

        # Настройка текста внутри диаграммы
        textprops = {'fontsize': 8, 'color': 'black', 'weight': 'bold'}

        # Создаем новый графический объект и подготавливаем круговую диаграмму
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.pie(sizes,
               labels=labels,
               autopct=lambda p: f'{p:.1f}%, ({p * sum(sizes) / 100.0 :.0f})',
               startangle=90,
               textprops=textprops,
               colors=colors)

        # Устанавливаем равное соотношение осей для круговой диаграммы
        ax.axis('equal')

        # Устанавливаем заголовок диаграммы
        ax.set_title(f'Статистика классификатора (Всего: {Data.objects.count()} записей).', fontsize=14,
                     fontweight='bold', fontstyle='italic')

        # Определяем путь для сохранения графика
        nonlocal chart_path_recognizer
        if settings.DEBUG:
            chart_path_recognizer = 'E:\cat_vs_dog_project\catdogsite\static_debug\\recognizer\images\stat_recognizer.png'
        else:
            chart_path_recognizer = STATIC_ROOT + 'recognizer\\images\\stat_recognizer.png'

        # Сохраняем график
        fig.savefig(chart_path_recognizer)
        return

    create_pie_chart_for_users(user_stat)
    create_pie_chart_for_recognizer(recognizer_stat)

    return render(request, 'recognizer/show_stats.html', {
        'menu': menu,
        'title': 'Статистика',
        'user_stat': user_stat,
        'recognizer_stat': recognizer_stat,
        'chart_path_user': chart_path_user,
        'chart_path_recognizer': chart_path_recognizer
    })

def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = FeedbackForm()

    return render(request, 'recognizer/feedback.html', {'menu': menu,  'form': form})




def recognize_image(request):
    def process_image(image):
        app_config = apps.get_app_config('recognizer')
        prediction = app_config.prediction_model
        predictions, probabilities = prediction.classifyImage(image, result_count=1)
        return predictions, probabilities

    def update_data_object(data, predictions, probabilities):
        if predictions[0] == 'dogs' and probabilities[0] > 59.99:
            data.class_by_recognizer = 'DOG'
        elif predictions[0] == 'cats' and probabilities[0] > 59.99:
            data.class_by_recognizer = 'CAT'
        elif probabilities[0] < 59.99:
            data.class_by_recognizer = 'UNKNOWN (probability<60%)'
        else:
            data.class_by_recognizer = 'UNREAD_YET'
        data.save()

    if request.method == 'POST':
        form = ClassByRecognizerForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.class_by_recognizer = 'UNREAD'
            data.class_by_user = 'EMPTY'
            data.save()
            tmp_for_database_object = data.pk
            image = get_object_or_404(Data, pk=tmp_for_database_object)
            image_path = image.image.path
            image = Image.open(image_path)

            predictions, probabilities = process_image(image)
            request.session['result_of_recognizer'] = {
                'predictions': predictions,
                'probabilities': probabilities,
            }

            current_obj = get_object_or_404(Data, pk=tmp_for_database_object)
            update_data_object(current_obj, predictions, probabilities)
            return redirect('after_recognize', tmp_for_database_object=data.pk)
    else:
        form = ClassByRecognizerForm()
    return render(request, 'recognizer/recognize.html', {'form_for_rec': form, 'menu': menu})


def after_recognize_image(request, tmp_for_database_object):
    current_obj = get_object_or_404(Data, pk=tmp_for_database_object)  # Получаем объект модели по первичному ключу
    current_image = current_obj.image
    result_of_recognize = request.session.get('result_of_recognizer')
    if request.method == 'POST':
        form = ClassByUserForm(request.POST, request.FILES)
        if form.is_valid():
            current_image = current_obj.image
            current_obj.class_by_user = form.cleaned_data['class_by_user']
            current_obj.save()  # Сохраняем обновленный объект модели
            return redirect('home')


    else:
        form = ClassByUserForm()

    categories = [choice[0] for choice in Data._meta.get_field('class_by_user').choices] #спопоб запросить категории у отложенного атрибута
    return render(request, 'recognizer/after_rec.html', {'form_after_rec': form,
                                                         'menu': menu,
                                                         'tmp_for_database_object': tmp_for_database_object,
                                                         'current_image' : current_image,
                                                         'result_of_rec' : result_of_recognize,
                                                         'current_obj': current_obj,
                                                         'categories': categories})


def pageNotFound(request, exeception):
    return HttpResponseNotFound('Страница не найдена')