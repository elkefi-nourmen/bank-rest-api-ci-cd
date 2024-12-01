"""
URL configuration for bank_rest_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.shortcuts import redirect
from account_app.views import trigger_error
def redirect_to_account_app(request):
    return redirect('account_app/')

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', redirect_to_account_app),
    path('account_app/', include('account_app.urls')),
    path('transaction_app/', include('transaction_app.urls')),
    path('sentry-debug/', trigger_error, name='sentry-debug'),
    
]
