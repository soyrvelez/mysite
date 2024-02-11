from django.contrib import admin

from .models import Album, Artist, Choice, Question, Song


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class AlbumInline(admin.TabularInline):
    model = Album
    extra = 3
class SongInline(admin.TabularInline):
    model = Song
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ["question_text", "pub_date", "was_published_recently"]
    list_filter = ["pub_date"]
    search_fields = ["question_text"]

class ArtistAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name"]}),
    ]
    inlines = [AlbumInline]
    list_filter = ["name"]
    search_fields = ["name"]

class AlbumAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["title", "artist"]}),
    ]
    inlines = [SongInline]
    list_filter = ["artist"]
    search_fields = ["title"]

class SongAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["title", "album", "artist"]}),
    ]
    list_filter = ["album"]
    search_fields = ["title", "album", "artist"]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Song, SongAdmin)
