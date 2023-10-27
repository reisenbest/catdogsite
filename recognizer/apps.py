from django.apps import AppConfig
from imageai.Classification.Custom import CustomImageClassification
from catdogsite.settings import STATIC_ROOT


class RecognizerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recognizer'
    verbose_name = 'классификатор кошек и собак'

    def initializing_the_image_classification_model(self):
        '''
        функция, которая автоматически вызывается Django при загрузке приложения.
        Здесь происходит инициализация модели классификации изображений с использованием библиотеки ImageAI.
        :return:
        '''
        prediction = CustomImageClassification()
        prediction.setModelTypeAsMobileNetV2()
        prediction.setModelPath(
            STATIC_ROOT + 'recognizer/modelsAI/mobileNet3_acc_88/MobileNetV2_epochs_30_batch_size_32/mobilenet_v2-data-test_acc_0.88384_epoch-28.pt')
        prediction.setJsonPath(
            STATIC_ROOT + 'recognizer/modelsAI/mobileNet3_acc_88/MobileNetV2_epochs_30_batch_size_32/data_model_classes.json')
        prediction.loadModel()
        self.prediction_model = prediction

    def ready(self):
        # Вызываем наш метод инициализации
        self.initializing_the_image_classification_model()

