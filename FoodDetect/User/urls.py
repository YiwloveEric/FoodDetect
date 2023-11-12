from django.urls import path, include

from User import views

urlpatterns = [
    path("login/", views.LoginView.as_view()),
    path("ocr/", views.OCRIngredient.as_view()),
    # path("fav/", ),
]
