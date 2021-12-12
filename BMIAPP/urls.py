from django.urls import path
from django.urls.resolvers import URLPattern
from rest_framework import routers
from BMIAPP import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('bmi', views.BMIViewSet)
urlpatterns = [
    path("create-user", views.create_user),
    path ('profile', views.profile),
    path ('fall-precategory', views.fall_precategory),
]
urlpatterns += router.urls
