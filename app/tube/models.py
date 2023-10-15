from datetime import timedelta

from django.db import models, transaction
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timesince
from moviepy.video.io.VideoFileClip import VideoFileClip

""" Давайте рассмотрим, как будут работать модели, которые я описал в предыдущем ответе:
1. Category (Категории): Модель для хранения категорий видео.
2. Video (Видеоролики): Модель для хранения информации о видеороликах. Внутри модели есть поля, такие как заголовок, описание, дата загрузки, длительность и ссылка на категорию. Связь с пользователем, который загрузил видео, устанавливается через поле "user".
3. Comment (Комментарии): Модель для хранения комментариев к видеороликам. Каждый комментарий связан с конкретным видеороликом (поле "video") и пользователем, который его оставил (поле "user").
4. Playlist (Плейлисты): Модель для хранения информации о плейлистах. Создатель плейлиста связан с пользователем (поле "user"). Возможно добавление нескольких видеороликов в один плейлист, и для этого используется поле "videos", которое устанавливает связь многие-ко-многим с моделью "Video".
5. Like (Лайки и дизлайки): Модель для отслеживания лайков и дизлайков видеороликов. Здесь также есть связи с пользователем (поле "user") и видеороликом (поле "video"), а поле "is_like" указывает, является ли это лайком (True) или дизлайком (False).
6. History (История просмотров): Модель для отслеживания истории просмотров. Связана с пользователем и видеороликом, и она хранит информацию о времени, когда видеоролик был просмотрен.

Теперь рассмотрим, как это работает:
1. Когда пользователь загружает видеоролик, запись о видеоролике добавляется в таблицу "Video", и она связана с пользователем, который загрузил видео.
2. При написании комментария к видеоролику создается запись в таблице "Comment", и она также связана с видеороликом и пользователем.
3. Если пользователь создает плейлист, то запись о плейлисте добавляется в таблицу "Playlist", и она связана с пользователем. Затем пользователь может добавлять видеоролики в этот плейлист.
4. Когда пользователь ставит лайк или дизлайк видеоролику, создается запись в таблице "Like", где указывается, что пользователь поставил лайк или дизлайк конкретному видеоролику.
5. Когда пользователь смотрит видеоролик, информация о просмотре добавляется в таблицу "History". Таким образом, вы можете отслеживать, какие видеоролики пользователь уже смотрел.
Связи между таблицами устанавливаются с использованием ForeignKey и ManyToManyField, что позволяет легко связывать данные между разными таблицами.
Для работы с этой базой данных в Django, вы можете использовать QuerySet'ы для извлечения и изменения данных. Например, вы можете получить список видеороликов, загруженных конкретным пользователем, или список комментариев к определенному видеоролику. 
"""


class Category(models.Model):
    name = models.CharField(max_length=255)


class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    upload_date = models.DateTimeField(auto_now_add=True)
    video_file = models.FileField(upload_to='videos/')
    duration = models.DurationField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,
                             blank=True)  # Связь с пользователем, который загрузил видео
    create_at = models.DateTimeField(auto_now_add=True)  # Когда было загружено видео

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Извлечь длительность видео и сохранить ее
        try:
            video_path = self.video_file.path
            clip = VideoFileClip(video_path)
            duration_seconds = clip.duration
            self.duration = timedelta(seconds=duration_seconds)
            clip.close()
        except Exception as e:
            # Обработайте ошибки, которые могут возникнуть при обработке видео
            # Например, файл не существует, не является видео и т.д.
            self.duration = None

        super().save(*args, **kwargs)

    def formatted_duration(self):
        return timesince.timesince(0, self.duration)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Установить пользователя, загрузившего видео
        if not self.user:
            self.user = kwargs.get('request').user


class Comment(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Связь с пользователем, который оставил комментарий
    video = models.ForeignKey(Video, on_delete=models.CASCADE)  # Связь с видеороликом


class Playlist(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Создатель плейлиста
    videos = models.ManyToManyField(Video)  # Связь многие-ко-многим с видеороликами


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    is_like = models.BooleanField()  # True - лайк, False - дизлайк


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    watched_at = models.DateTimeField(auto_now=True)
