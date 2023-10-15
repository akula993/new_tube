from django.contrib import admin

from app.tube.models import Category, Video


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    pass


@admin.register(Video)
class AdminVideo(admin.ModelAdmin):
    list_display = ('id', 'title', 'duration', 'category', 'user',)
    list_display_links = ('id', 'title',)

    # list_editable = ( 'duration',)
    # search_fields = ()
    # search_help_text = None
    # date_hierarchy = None
    save_as = True
    # save_as_continue = True
    save_on_top = True
    # paginator = Paginator
    # preserve_filters = True
    # inlines = ()
    readonly_fields = ('duration',)
    exclude = ('user',)

    def save_model(self, request, obj, form, change):
        # Установить пользователя, загрузившего видео
        if not obj.user:
            obj.user = request.user
        obj.save()
