"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib.auth import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from ecomm import views
# from ecomm.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ecomm.urls')), # all the routes related to the main marketplace
    path('account/', include('account.urls')),
    path('updatecart', views.updateCart, name='update-cart'),
    path('api/', include('api.urls')), # API endpoints
    path('seller/', include('sellercentral.urls')),
    path('checkout/', include('checkout.urls'))
] 


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
