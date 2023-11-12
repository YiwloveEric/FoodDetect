from django.urls import path, include

from .views import OCRIngredient

urlpatterns = [
    path("ocr/", OCRIngredient.as_view()),
    path("fav/",)
]
