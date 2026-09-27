from django.contrib import admin

from .models import Inquiry


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "company", "project", "created_at")
    search_fields = ("name", "email", "company", "message")
    list_filter = ("project", "created_at")
    readonly_fields = ("created_at",)
