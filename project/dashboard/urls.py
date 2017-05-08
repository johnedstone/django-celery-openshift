from django.conf.urls import url
from dashboard import views

urlpatterns = [
    url(r'^api/v1/images/counts$', views.get_image_counts, name='image_counts'),
    url(r'^api/v1/images/counts/(?P<day>\d{1,2})$', views.get_image_counts, name='image_counts_by_day'),

    url(r'^images/counts/html$', views.get_image_counts,
        {'response_type': 'html'},
        name='image_counts_html'),
    url(r'^images/counts/html/(?P<day>\d{1,2})$', views.get_image_counts,
        {'response_type': 'html'},
        name='image_counts_html_by_day'),
]

# vim: ai et ts=4 sw=4 sts=4 nu
