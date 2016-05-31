from django.conf.urls import url, include
from django.contrib import admin
import approachone.urls
import approachtwo.urls
from core import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'approachone/', include(approachone.urls)),
    url(r'approachtwo/', include(approachtwo.urls)),
    url(r'^$', views.index)
]
