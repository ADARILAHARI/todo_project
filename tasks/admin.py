from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "completed", "created_by", "created")
    list_filter = ("completed", "created")
    search_fields = ("title",)
    ordering = ("-created",)
    list_display_links = ("id", "title")

