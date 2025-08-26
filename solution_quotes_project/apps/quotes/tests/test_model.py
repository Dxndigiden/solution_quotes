import pytest
from django.core.exceptions import ValidationError

from apps.quotes.models import Quote


@pytest.mark.django_db
def test_limit_citata_source():
    """Проверка: у одного источника не больше 3 цитат."""
    source_name = "ТестовыйИсточник"
    Quote.objects.create(
        text="Цитата 1", source=source_name, weight=1
    )
    Quote.objects.create(
        text="Цитата 2", source=source_name, weight=1
    )
    Quote.objects.create(
        text="Цитата 3", source=source_name, weight=1
    )

    fourth_quote = Quote(
        text="Цитата 4", source=source_name, weight=1
    )
    with pytest.raises(ValidationError):
        fourth_quote.full_clean()


@pytest.mark.django_db
def test_weight_must_be_at_least_one():
    """Проверка: вес цитаты >= 1"""
    bad_quote = Quote(
        text="Плохая цитата", source="Источник", weight=0
    )
    with pytest.raises(ValidationError):
        bad_quote.full_clean()


@pytest.mark.django_db
def test_text_normalization_and_unique_check():
    """Проверка: нормализация текста и уникальность."""
    Quote.objects.create(text="Привет Мир", source="Книга1", weight=1)
    duplicate_quote = Quote(
        text="  привет   мир  ", source="Книга2", weight=1
    )
    with pytest.raises(ValidationError):
        duplicate_quote.full_clean()
