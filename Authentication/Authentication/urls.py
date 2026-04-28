from django.contrib import admin
from django.urls import path, include
from rest_framework import settings
from Authentication.Authentication import settings
from rest_framework.routers import DefaultRouter
from api import views
from api.auth import CustomAuthToken_view
### For JWT Authentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
#from rest_framework.authtoken.views import obtain_auth_token
from datetime import timedelta

router = DefaultRouter()

# Register StudentViewSet with Router
#router.register('studentapi', views.StudentModelViewSet, basename='student')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    # Used for SessionAuthentication
    path('auth/', include('rest_framework.urls',
                          namespace='rest_framework')),
    # Used for TokenAuthentication
    # as_view() is used for class
    path('gettoken/', CustomAuthToken_view.as_view()),
    ## For Filtering
    path('studentapi/', views.StudentList.as_view()),
    # For JWT Authentication
    path('gettoken/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refreshtoken/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verifytoken/', TokenVerifyView.as_view(), name='token_verify'),
]

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': settings.SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': 'Bearer',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

