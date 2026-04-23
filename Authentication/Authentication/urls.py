from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views
from api.auth import CustomAuthToken
#from rest_framework.authtoken.views import obtain_auth_token

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
    path('gettoken/', CustomAuthToken.as_view()),
    ## For Filtering
    path('studentapi/', views.StudentList.as_view()),
]


