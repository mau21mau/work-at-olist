from django.conf.urls import url, include
from django.contrib import admin
import approachone.urls
from core.views import IndexView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'approachone/', include(approachone.urls)),
    url(r'^$', IndexView.as_view())
]
