from core.utils.router import BaseSimpleRouter

from .views import UserViewSet

router = BaseSimpleRouter()
router.register(r'users', UserViewSet, basename='users')
urlpatterns = router.urls
