from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("polls/", include("polls.urls")),
	path("lunch_time/", include("lunch_time.urls")),
    path("admin/", admin.site.urls),
]