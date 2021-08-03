from rest_framework import serializers

from .models import *

class CardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Card
        fields = ('id','cardNumber','name','mmyy' ,'cvv','sold','isblocked')

class MoneyBackSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MoneyBack
        fields = ('id','cardFrom','cardTo','price','dateAdded')

    
    
    
    
    