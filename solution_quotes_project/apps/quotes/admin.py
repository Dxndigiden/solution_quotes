from django.contrib import admin
from django.utils.html import format_html

from .models import Quote


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = (
        "short_text",
        "source",
        "weight",
        "likes_display",
        "dislikes_display",
        "views_display",
        "created_at",
    )
    search_fields = ("text", "source")
    list_filter = ("source", "created_at")
    readonly_fields = ("likes", "dislikes", "views", "created_at")
    ordering = ("-created_at",)

    def short_text(self, obj):
        """Короткий текст цитаты (для списка)."""
        return obj.text[:70] + ("..." if len(obj.text) > 70 else "")

    short_text.short_description = "Цитата"

    def likes_display(self, obj):
        """Подсветка лайков."""
        color = "green" if obj.likes > 0 else "gray"
        return format_html(
            '<span style="color:{};">{}</span>', color, obj.likes
        )

    likes_display.short_description = "👍 Лайки"
    likes_display.admin_order_field = "likes"

    def dislikes_display(self, obj):
        color = "red" if obj.dislikes > 0 else "gray"
        return format_html(
            '<span style="color:{};">{}</span>', color, obj.dislikes
        )

    dislikes_display.short_description = "👎 Дизлайки"
    dislikes_display.admin_order_field = "dislikes"

    def views_display(self, obj):
        color = "blue" if obj.views > 0 else "gray"
        return format_html(
            '<span style="color:{};">{}</span>', color, obj.views
        )

    views_display.short_description = "👁 Просмотры"
    views_display.admin_order_field = "views"
