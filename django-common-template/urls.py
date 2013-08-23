from django.conf import settings
from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    ('^$', views.home),
    ('^admin/', include('cardea.cadmin.urls')),
    ('^account/', include('cardea.account.urls')),
    ('^pub/', include('cardea.pub.urls')),
#    ('^test/', include('cardea.test.urls')),
#    url(r'^django-admin/', include(admin.site.urls)),
    (r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT})
)