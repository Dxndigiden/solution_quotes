from django.contrib import admin

from .models import Quote


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = (
        "short_text",
        "source",
        "weight",
        "likes",
        "dislikes",
        "views",
        "created_at",
    )
    search_fields = ("text", "source")
    list_filter = ("source",)
    readonly_fields = (
        "likes",
        "dislikes",
        "views",
        "created_at",
    )

    def short_text(self, obj):
        return obj.text[:70] + ("..." if len(obj.text) > 70 else "")

    short_text.short_description = "Цитата"
