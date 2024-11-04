from django.http import JsonResponse
from django.urls import include, path, re_path

from core.utils.urls import urlpatterns

urlpatterns += [
    path('api/v1/', include('user.urls')),
    re_path('api/v1/ready/?$', lambda request: JsonResponse(data={'success': True})),
]
