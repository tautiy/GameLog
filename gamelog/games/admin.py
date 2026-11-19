from django.contrib import admin

from .models import (
    Genre,
    Developer,
    Publisher,
    Platform,
    Game,
    GamePublisher,
)


class GamePublisherInline(admin.TabularInline):
    model = GamePublisher
    extra = 1


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    inlines = [GamePublisherInline]


admin.site.register(Genre)
admin.site.register(Developer)
admin.site.register(Publisher)
admin.site.register(Platform)
admin.site.register(GamePublisher)
