from django.conf.urls import url
from . import views


""" REST API """
urlpatterns = [
    url(r'rest/category/$', views.api_category),
    url(r'rest/channel/$', views.api_channel),
    url(r'rest/channels/$', views.api_channels),
]

""" WEBSITE """
urlpatterns += [
    url(r'$', views.approach_one_view),
]
