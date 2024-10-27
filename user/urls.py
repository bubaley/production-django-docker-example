from core.utils.base_simple_router import BaseSimpleRouter

from .views import UserViewSet

router = BaseSimpleRouter()
router.register(r'users', UserViewSet, basename='users')
urlpatterns = router.urls
