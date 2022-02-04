from django.urls import path, include
from core.utils.urls import urlpatterns

urlpatterns += [
    path('api/v1/', include('user.urls')),
]
