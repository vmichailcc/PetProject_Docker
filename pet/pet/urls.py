from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from accounts.urls import user_router, mailing_router
from accounts.views import CustomAuthToken
from store.urls import store_router, comment_router, order_router, product_router, order_detail_router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("store.urls")),
    path('', include("accounts.urls")),
    path('api/token-auth/', CustomAuthToken.as_view()),
    path('api/store/', include(store_router.urls)),
    path('api/product/', include(product_router.urls)),
    path('api/comment/', include(comment_router.urls)),
    path('api/order/', include(order_router.urls)),
    path('api/order_detail/', include(order_detail_router.urls)),
    path('api/profile/', include(user_router.urls)),
    path('api/mailing/', include(mailing_router.urls)),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
