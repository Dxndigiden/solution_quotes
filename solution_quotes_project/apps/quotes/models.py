import random

from django.core.exceptions import ValidationError
from django.db import models


class QuoteManager(models.Manager):
    def weighted_random(self):
        """Возвращает случайную цитату с учетом веса."""
        all_quotes = list(self.all())
        if not all_quotes:
            return None

        weights = [quote.weight for quote in all_quotes]
        return random.choices(all_quotes, weights=weights, k=1)[0]


class Quote(models.Model):
    """Модель цитаты с уникальностью, лимитом по источнику и весом."""

    text = models.TextField(
        unique=True, help_text="Уникальный текст цитаты"
    )
    source = models.CharField(
        max_length=200,
        help_text="Откуда цитата: фильм, книга и т.д.",
    )
    weight = models.PositiveIntegerField(
        default=1,
        help_text="Чем выше, тем чаще будет показываться",
    )
    likes = models.PositiveIntegerField(default=0, help_text="Лайки")
    dislikes = models.PositiveIntegerField(
        default=0, help_text="Дизлайки"
    )
    views = models.PositiveIntegerField(
        default=0, help_text="Количество просмотров"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Дата создания"
    )

    objects = QuoteManager()

    class Meta:
        ordering = ["-likes", "-views", "-created_at"]
        indexes = [
            models.Index(fields=["source"]),
            models.Index(fields=["-likes"]),
        ]
        verbose_name = "Цитата"
        verbose_name_plural = "Цитаты"

    def __str__(self):
        return f"{self.text[:50]} — {self.source}"

    def clean(self):
        """Валидирует уникальность (без учета пробелов и регистра),
        лимит источника и вес ≥ 1."""

        cleaned_text = " ".join(self.text.strip().split())
        cleaned_source = self.source.strip()

        # Проверка дубликатов с нормализацией текста
        duplicates = (
            Quote.objects.exclude(pk=self.pk)
            if self.pk
            else Quote.objects.all()
        )
        for quote in duplicates:
            quote_text_normalized = " ".join(
                quote.text.strip().split()
            )
            if quote_text_normalized.lower() == cleaned_text.lower():
                raise ValidationError(
                    {"text": "Такая цитата уже есть."}
                )

        # Проверка лимита цитат по источнику
        source_quotes = Quote.objects.filter(
            source__iexact=cleaned_source
        )
        if self.pk:
            source_quotes = source_quotes.exclude(pk=self.pk)
        if source_quotes.count() >= 3:
            raise ValidationError(
                {"source": "У этого источника уже есть 3 цитаты."}
            )

        if self.weight < 1:
            raise ValidationError({"weight": "Вес должен быть ≥ 1."})

        self.text = cleaned_text
        self.source = cleaned_source

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
