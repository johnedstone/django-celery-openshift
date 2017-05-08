from django.conf import settings
from django.conf.urls import include, url
from django.http import HttpResponse
from django.shortcuts import redirect

handler404 = 'dashboard.common.custom_page_not_found_json_view'

urlpatterns = [
    url(r'^health$', lambda request:HttpResponse(status=200)),
    url(r'^alive$', lambda request:HttpResponse(status=200)),

    url(r'^$', lambda x: redirect('dashboard:image_counts', permanent=False), name='home'),
    url(r'^dashboard/', include('dashboard.urls', namespace='dashboard')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

# vim: ai et ts=4 sw=4 sts=4 nu
