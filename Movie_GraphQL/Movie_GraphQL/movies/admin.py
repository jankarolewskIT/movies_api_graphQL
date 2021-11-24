from django.contrib import admin

from .models import Movie, Director

admin.site.register(Movie, admin.ModelAdmin)
admin.site.register(Director, admin.ModelAdmin)
