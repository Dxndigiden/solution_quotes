import pytest

from apps.quotes.forms import QuoteForm


@pytest.mark.django_db
def test_weight_too_low():
    """Вес < 1 не проходит валидацию."""

    form = QuoteForm(
        data={"text": "Тест", "source": "Источник", "weight": 0}
    )
    assert not form.is_valid()
    assert "weight" in form.errors


@pytest.mark.django_db
def test_weight_too_high():
    """Вес > 7 не проходит валидацию."""

    form = QuoteForm(
        data={"text": "Тест", "source": "Источник", "weight": 8}
    )
    assert not form.is_valid()
    assert "weight" in form.errors


@pytest.mark.django_db
def test_empty_fields():
    """Пустые поля не проходят валидацию."""

    form = QuoteForm(data={})
    assert not form.is_valid()
    assert "text" in form.errors
    assert "source" in form.errors
    assert "weight" in form.errors
