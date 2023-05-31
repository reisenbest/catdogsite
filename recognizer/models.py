from django.db import models
from django.urls import reverse

# Create your models here.


class Data(models.Model):
    class class_by_recognizer(models.TextChoices):
        # будет определятся после того как пользователь произведет определение фото
        UNREAD = 'UNREAD_YET' #пользовтель еще не произвел определение, но уже загрузил фото
        UNKNOW = 'UNKNOWN (probability<60%)' #определитель не дал ни одному из классов больше 60% вероятности
        CAT = 'CAT' #более 60%, что на фото пользователя кот по мнению модели обученной
        DOG = 'DOG' #более 60%, что на фото пользователя собака по мнению модели обученной

    class class_by_user(models.TextChoices):
        #поле заполняется по результату опроса пользователя
        EMPTY = 'EMPTY' #юзер не прошел опрос и не дал данных о своем фото
        CAT_ONE = 'CAT_ONE' #юзер заявил, что на его изображении один кот
        DOG_ONE = 'DOG_ONE' #юзер заявил, что на его изображении одна собака
        CATS_MANY = 'CATS_MANY' #юзер заявил, что на его изображении >1 кота
        DOGS_MANY = 'DOGS_MANY' #юзер заявил, что на его изображении >1 собаки
        CAT_AND_DOG = 'CAT_AND_DOG' #юзер заявил, что на его изображении и коты и собаки одновременно
        BAD_IMAGE = 'BAD_IMAGE' #юзер заявил, что на его изображении нет ни котов, ни собак


    image = models.ImageField(upload_to='users_images/%Y/%m/%d')
    time_upload = models.DateTimeField(auto_now_add=True)
    class_by_recognizer = models.CharField(max_length=100,
                                           choices=class_by_recognizer.choices,
                                           default=class_by_recognizer.UNREAD)
    class_by_user = models.CharField(max_length=100,
                                    choices=class_by_user.choices,
                                    default=class_by_user.EMPTY,
                                    verbose_name='Охарактеризуйте ваше изображение')

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse()

    class Meta:
        verbose_name = 'База данных с изображениями'
        verbose_name_plural = 'База данных с изображениями'
        ordering = ['class_by_recognizer', 'time_upload']


class Feedback(models.Model):
    name = models.CharField(max_length=30, verbose_name='Ваше имя')
    feedback = models.TextField(verbose_name='Напишите что-нибудь')
    time_upload = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'
        ordering = ['time_upload', 'name']

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse()