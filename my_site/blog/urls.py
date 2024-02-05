from django.urls import path
from . import views


urlpatterns = [
    path("", views.StaringView.as_view(), name="start-page"),
    path("posts", views.PostListView.as_view(), name="post-page"),
    path("posts/<slug:slug>", views.DetailPostView.as_view(), name="post-detail-page"),
    path("read-later", views.ReadLaterView.as_view(), name="read-later")
]
