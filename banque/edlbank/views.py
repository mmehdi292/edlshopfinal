from django.core.checks import messages
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets
from rest_framework.serializers import Serializer

from .serializers import *
from .models import *

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

class MoneyBackViewSet(viewsets.ModelViewSet):
    queryset = MoneyBack.objects.all()
    serializer_class = MoneyBackSerializer

def home(request):
    return HttpResponse("<h1>mehdi</h1>")

@api_view(['POST'])
def exsitant_card(request):

    cardNumber=request.data['cardNumber']
    name=request.data['name']
    mmyy=request.data['mmyy']
    cvv=request.data['cvv']
    prixtotale=request.data['prixtotale']
    try:
        
        card = Card.objects.get(cardNumber=cardNumber,name=name,mmyy=mmyy,cvv=cvv)
        print(card)
        if card.sold < float(prixtotale):
            message = 'votre sold est inssffisant'
        else:
            card.sold -= float(prixtotale)
            card.save()
            message = 'opération bien fait'
    except:
        print("here")
        card=None
        message = 'pas de carte avec votre information'

    context = {
        'message':message
    }
    
    return Response(context)


@api_view(['POST'])
def backarticle(request):

    cardNumber=request.data['cardNumber']
    name=request.data['name']
    mmyy=request.data['mmyy']
    cvv=request.data['cvv']
    prixtotale=request.data['prixtotale']
    try:
        
        card = Card.objects.get(cardNumber=cardNumber,name=name,mmyy=mmyy,cvv=cvv)
        print(card)
        card.sold = card.sold + float(prixtotale)
        card.save()
        message = 'Votre solde est bien récupéré'
        
    except:
        message = 'Erreur sur la transation'

    context = {
        'message':message
    }
    
    return Response(context)

