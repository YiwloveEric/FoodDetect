from django.urls import path, include

from User import views

urlpatterns = [
    path("login/", views.LoginView.as_view()),
    path("ocr/", views.OCRIngredient.as_view()),
    path("regisfav/", views.RegisFavorView.as_view()),
    path("reviewfavor/", views.ReviewFavorView.as_view())
]
