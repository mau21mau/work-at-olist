from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
import approachone.urls
from core import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'approachone/', include(approachone.urls)),
    url(r'^$', views.index)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
