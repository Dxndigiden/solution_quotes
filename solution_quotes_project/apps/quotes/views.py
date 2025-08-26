from django.contrib import messages
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import QuoteForm
from .models import Quote


def random_quote_view(request: HttpRequest):
    """Главная страница со случайной цитатой."""
    quote = Quote.objects.weighted_random()
    if quote:
        quote.views += 1
        quote.save(update_fields=["views"])
    return render(
        request, "quotes/random_quote.html", {"quote": quote}
    )


def top_quotes_view(request: HttpRequest):
    """Топ-10 цитат по лайкам."""
    top_quotes = Quote.objects.order_by("-likes")[:10]
    return render(
        request, "quotes/top_quotes.html", {"quotes": top_quotes}
    )


def _update_counter(request: HttpRequest, quote_id: int, field: str):
    """Обновляет счетчик лайков или дизлайков. Поддержка AJAX."""
    quote = get_object_or_404(Quote, id=quote_id)

    if field not in ("likes", "dislikes"):
        return redirect(
            request.META.get(
                "HTTP_REFERER", reverse("quotes:random_quote")
            )
        )

    # Увеличиваем нужный счетчик
    setattr(quote, field, getattr(quote, field) + 1)
    quote.save(update_fields=[field])

    # AJAX ответ
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({field: getattr(quote, field)})

    return redirect(
        request.META.get(
            "HTTP_REFERER", reverse("quotes:random_quote")
        )
    )


def like_quote(request: HttpRequest, quote_id: int):
    """Добавляем лайк цитате."""
    return _update_counter(request, quote_id, "likes")


def dislike_quote(request: HttpRequest, quote_id: int):
    """Добавляем дизлайк цитате."""
    return _update_counter(request, quote_id, "dislikes")


def add_quote_view(request):
    """Страница добавления новой цитаты через веб-форму."""
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Цитата успешно добавлена!")
                form = (
                    QuoteForm()
                )  # очищаем форму после успешного сохранения
            except Exception as e:
                form.add_error(None, str(e))
    else:
        form = QuoteForm()

    return render(request, "quotes/add_quote.html", {"form": form})
