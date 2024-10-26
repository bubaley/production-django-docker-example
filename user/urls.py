from core.utils.base_router import BaseRouter

from .views import UserViewSet

router = BaseRouter()
router.register(r'users', UserViewSet, basename='users')
urlpatterns = router.urls
