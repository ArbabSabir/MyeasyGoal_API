from .models import Goal_model,User
from rest_framework import serializers


class Gole_Seri(serializers.ModelSerializer):
    class Meta:
        model=Goal_model
        fields=('id','user','title','description')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'date_joined')