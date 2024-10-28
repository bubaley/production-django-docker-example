from django.urls import include, path

from core.utils.urls import urlpatterns

urlpatterns += [
    path('api/v1/', include('user.urls')),
]
