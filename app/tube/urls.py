from django.urls import path

from app.tube.views import home, VideoUploadFirstStep, VideoUploadSecondStep

urlpatterns = [
    path('', home, name='home'),
    path('create/', VideoUploadFirstStep.as_view(), name='create_first_step'),
    path('create/second/', VideoUploadSecondStep.as_view(), name='create_second_step'),
]