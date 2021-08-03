from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('cards', views.CardViewSet)
router.register('MoneyBacks', views.MoneyBackViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('',views.home,name='home'),
    path('api/', include(router.urls)),
    path('paiement/', views.exsitant_card , name='paiement' ),
    path('back/', views.backarticle , name='back' ),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]