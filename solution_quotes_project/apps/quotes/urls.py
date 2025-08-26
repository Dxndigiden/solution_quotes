from django.urls import path

from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.random_quote_view, name="random_quote"),
    path("top/", views.top_quotes_view, name="top_quotes"),
    path("like/<int:quote_id>/", views.like_quote, name="like_quote"),
    path(
        "dislike/<int:quote_id>/",
        views.dislike_quote,
        name="dislike_quote",
    ),
]
