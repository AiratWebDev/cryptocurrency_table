from rest_framework import serializers
from currencies.models import Currency


class CurrencySerializer(serializers.ModelSerializer):
    """Serializer for currencies"""
    class Meta:
        model = Currency
        fields = '__all__'
    