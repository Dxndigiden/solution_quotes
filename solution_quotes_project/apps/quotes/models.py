import random

from django.core.exceptions import ValidationError
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models


class QuoteManager(models.Manager):
    def weighted_random(self):
        """Возвращает случайную цитату с учетом веса."""
        quotes = list(self.all())
        if not quotes:
            return None
        weights = [q.weight for q in quotes]
        return random.choices(quotes, weights=weights, k=1)[0]


class Quote(models.Model):
    """Модель цитаты с уникальностью текста, лимитом по источнику и весом."""

    text = models.TextField(
        unique=True,
        help_text="Уникальный текст цитаты",
        verbose_name="Текст цитаты",
    )
    source = models.CharField(
        max_length=200,
        help_text="Источник цитаты",
        verbose_name="Источник",
    )
    weight = models.PositiveIntegerField(
        default=1,
        help_text="Чем больше вес, тем чаще цитата будет выпадать (от 1 до 7)",
        verbose_name="Вес цитаты",
        validators=[
            MinValueValidator(1, "Вес не может быть меньше 1"),
            MaxValueValidator(7, "Вес не может быть больше 7"),
        ],
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

    @staticmethod
    def normalize_text(text: str) -> str:
        """Удаляет лишние пробелы и нормализует строку."""
        return " ".join(text.strip().split())

    def clean(self):
        """Валидирует цитату: повтор текста,лимит по источнику, вес ≥ 1."""
        self.text = self.normalize_text(self.text)
        self.source = self.normalize_text(self.source)

        # Проверка уникальности текста (без учета регистра)
        qs = (
            Quote.objects.exclude(pk=self.pk)
            if self.pk
            else Quote.objects.all()
        )
        if any(
            self.normalize_text(q.text).lower() == self.text.lower()
            for q in qs
        ):
            raise ValidationError({"text": "Такая цитата уже есть."})

        # Проверка лимита цитат по источнику
        source_qs = Quote.objects.filter(source__iexact=self.source)
        if self.pk:
            source_qs = source_qs.exclude(pk=self.pk)
        if source_qs.count() >= 3:
            raise ValidationError(
                {"source": "У этого источника уже есть 3 цитаты."}
            )

        if self.weight < 1:
            raise ValidationError({"weight": "Вес должен быть ≥ 1."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
