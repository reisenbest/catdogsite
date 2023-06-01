DEPLOY-django:

в гитигнор добавить все что связано с админ-панелью, 
settings.py инфу. сикрет кей, allowed хосты, DB-files
DB
users-files
создать новый settings.py без конфеденциальной инфы
и вообще все ненужное для функционирвоания в гитигнор
https://youtu.be/03egj6YEUFY в этом видео инструкция +-

проброска локального порта Ngrok 
https://youtu.be/NrSS6TCBP-Y
нужно для демонстрации приложения без его развертывания
в кратце - разрешаем открываем порт через компанду ngrok http 8000 (например)
+ нужно помучаться с csrf token
в settings.py:
CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = ['https://b04c-95-27-41-124.ngrok-free.app']
в allowed-host добавить открывшийся порт
в views.py:
from django.views.decorators.csrf import csrf_protect

