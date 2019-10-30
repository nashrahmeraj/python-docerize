from django.conf.urls import url

from .views import ProcessImage

urlpatterns = [
    url(r'detect_object', ProcessImage.as_view()),
]
