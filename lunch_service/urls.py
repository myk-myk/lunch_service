"""
URL configuration for lunch_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from service.routers import router


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('service.urls')),
    path('api/service-auth/', include('rest_framework.urls')),
    path('api/service/', include(router.urls)),
    path('api/service/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/service/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/service/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
