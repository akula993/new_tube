from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView

from app.tube.forms import FormVideoCreateFirstStep, FormVideoCreateSecondStep
from app.tube.models import Video


def home(request):
    video = Video.objects.all()
    context = {
        'video': video
    }

    return render(request, 'tube/home.html', context)

class VideoUploadFirstStep(View):
    template_name = 'tube/create_first_step.html'

    def get(self, request, *args, **kwargs):
        form = FormVideoCreateFirstStep()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = FormVideoCreateFirstStep(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.user = request.user
            video.save()
            request.session['video_id'] = video.id  # Сохраняем id видео в сессии
            return redirect('create_second_step')
        return render(request, self.template_name, {'form': form})

class VideoUploadSecondStep(View):
    template_name = 'tube/create_second_step.html'

    def get(self, request, *args, **kwargs):
        video_id = request.session.get('video_id')
        if video_id:
            video = Video.objects.get(id=video_id)
            form = FormVideoCreateSecondStep(instance=video)
            return render(request, self.template_name, {'form': form})
        else:
            return redirect('create_first_step')

    def post(self, request, *args, **kwargs):
        video_id = request.session.get('video_id')
        if video_id:
            video = Video.objects.get(id=video_id)
            form = FormVideoCreateSecondStep(request.POST, instance=video)
            if form.is_valid():
                form.save()
                del request.session['video_id']  # Удаляем id видео из сессии
                return redirect('home')
            return render(request, self.template_name, {'form': form})
        else:
            return redirect('create_first_step')