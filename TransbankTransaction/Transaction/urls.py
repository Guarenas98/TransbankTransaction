from django.conf.urls import url
from . import views
from django.views.generic import RedirectView


#URLs reached this URL Dispath must start with "Transaction/"
# name let use href = {%create%} insteand of href = /create/ in templates
urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url('create/', views.doTransaction, name = "create"),
]
