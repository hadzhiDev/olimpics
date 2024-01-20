from django.urls import path, include
from . import views

from .yasg import urlpatterns as url_doc

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

# router.register('register', views.RegisterViewSet)
router.register('languages', views.ProgramingLanguageViewSet)


urlpatterns = [
    path('register/', views.RegisterGenericAPIView.as_view()),
    path('confirm-request-to-application/', views.ConfirmEmailApiView.as_view()),

    path('', include(router.urls))
]

urlpatterns += url_doc