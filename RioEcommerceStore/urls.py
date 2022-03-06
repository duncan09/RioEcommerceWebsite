from django.contrib import admin
from django.urls import path,include
from django.conf import settings

urlpatterns = [
    path('',include('store.urls',namespace='store')),
    path('account/',include('allauth.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns +=[path('__debug__/',include(debug_toolbar.urls))]
