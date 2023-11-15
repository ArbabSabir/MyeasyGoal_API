from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import Goal_view,UserViewSet



router = DefaultRouter()
router.register(r'goals', Goal_view)
router.register(r'users', UserViewSet)

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('',include(router.urls)),
    

]