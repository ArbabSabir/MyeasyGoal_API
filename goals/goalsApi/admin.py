from django.contrib import admin
from django.contrib.auth.models import User
from .models import Goal_model

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('id', 'username', 'email', 'date_joined')
#     search_fields = ('username', 'email')
#     list_filter = ('date_joined',)

@admin.register(Goal_model)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'description')
    list_filter = ('user',)