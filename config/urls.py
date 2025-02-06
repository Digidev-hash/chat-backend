from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import UserViewSet
from chat.views import ConversationViewSet, MessageViewSet
from .views import redirect_to_api_root, APIRoot

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'conversations', ConversationViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('', redirect_to_api_root, name='root'),
    path('admin/', admin.site.urls),
    path('api/', APIRoot.as_view(), name='api-root'),
    path('api/', include(router.urls)),
    path('api/auth/', include('accounts.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

