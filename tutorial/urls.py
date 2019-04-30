"""tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from snippets import views

# View 대신 ViewSet클래스를 사용해서 url설정할 필요가 없다.
# Router 클래스를 사용하면 view코드와 view, url이 자동연결된다.

#라우터를 생성하고 viewset을 등록한다.
router = DefaultRouter()
router.register(r'snippets',views.SnippetViewSet)
router.register(r'users',views.UserViewSet)

#API URL을 라우터가 자동으로 인식한다.
urlpatterns = [
    path('',include(router.urls)),
]
