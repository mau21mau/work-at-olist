from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
import approachone.urls
from core.views import IndexView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'approachone/', include(approachone.urls)),
    url(r'^$', IndexView.as_view())
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
