from django.contrib import admin
from django.urls import path
from .views import RegistrationAPIView, LoginAPIView, LogoutAPIView, GoalListAPIView, GoalDetailAPIView

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('goals/', GoalListAPIView.as_view(), name='goal-list'),
    path('goals/<int:pk>/', GoalDetailAPIView.as_view(), name='goal-detail'),
]

