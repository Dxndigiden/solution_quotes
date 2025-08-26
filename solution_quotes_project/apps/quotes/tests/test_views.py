import pytest
from django.urls import reverse

from apps.quotes.models import Quote


@pytest.mark.django_db
def test_random_quote_view(client):
    """Проверяем, что случайная цитата возвращается корректно."""

    quote = Quote.objects.create(
        text="Hello World", source="Book", weight=1
    )
    url = reverse("quotes:random_quote")
    response = client.get(url)

    assert response.status_code == 200
    assert quote.text in response.content.decode()


@pytest.mark.django_db
def test_like_dislike_ajax(client):
    """Проверяем лайк и дизлайк через AJAX."""

    quote = Quote.objects.create(
        text="Vote Test", source="Book", weight=1
    )

    url_like = reverse("quotes:like_quote", args=[quote.id])
    url_dislike = reverse("quotes:dislike_quote", args=[quote.id])

    # Лайк
    response_like = client.post(
        url_like, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
    )
    quote.refresh_from_db()
    assert quote.likes == 1

    # Дизлайк
    response_dislike = client.post(
        url_dislike, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
    )
    quote.refresh_from_db()
    assert quote.dislikes == 1
