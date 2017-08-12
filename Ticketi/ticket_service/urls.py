from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import url, include

urlpatterns = [
    url(r'^addd/', admin.site.urls),
]
