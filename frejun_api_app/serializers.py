from django.contrib.auth.models import User
from .models import Account, PhoneNumber
from rest_framework import serializers

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'