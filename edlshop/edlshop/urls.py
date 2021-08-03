from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('trander/', trander_home, name='trander'),
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', logout, name='logout'),
    path('gestion/articles/', gestionArticles, name='gestionArticles'),
    path('gestion/articles/add', addArticles, name='addArticles'),
    path('gestion/articles/delete/<int:pk>/', deleteArticles, name='deleteArticles'),
    path('gestion/articles/update/<int:pk>/', updateArticles, name='updateArticles'),
    path('gestion/cpu/', gestioncpus, name='gestioncpus'),
    path('gestion/cpu/add', addcpus, name='addcpus'),
    path('gestion/cpu/delete/<int:pk>/', deletecpus, name='deletecpus'),
    path('gestion/cpu/update/<int:pk>/', updatecpus, name='updatecpus'),
    path('gestion/fan/', gestionfans, name='gestionfans'),
    path('gestion/fan/add', addfans, name='addfans'),
    path('gestion/fan/delete/<int:pk>/', deletefans, name='deletefans'),
    path('gestion/fan/update/<int:pk>/', updatefans, name='updatefans'),

    path('gestion/motherboards/', gestionmotherboards, name='gestionmotherboards'),
    path('gestion/motherboard/add', addmotherboard, name='addmotherboard'),
    path('gestion/motherboard/delete/<int:pk>/', deletemotherboard, name='deletemotherboard'),
    path('gestion/motherboard/update/<int:pk>/', updatemotherboard, name='updatemotherboard'),

    path('gestion/ram/', gestionrams, name='gestionrams'),
    path('gestion/ram/add', addram, name='addram'),
    path('gestion/ram/delete/<int:pk>/', deleteram, name='deleteram'),
    path('gestion/ram/update/<int:pk>/', updateram, name='updateram'),

    path('gestion/GraphicCard/', gestiongraphiccard, name='gestiongraphiccard'),
    path('gestion/GraphicCard/add', addgraphiccard, name='addgraphiccard'),
    path('gestion/GraphicCard/delete/<int:pk>/', deletegraphiccard, name='deletegraphiccard'),
    path('gestion/GraphicCard/update/<int:pk>/', updategraphiccard, name='updategraphiccard'),

    path('gestion/DisqueDur/', gestionDisqueDurs, name='gestionDisqueDurs'),
    path('gestion/DisqueDur/add', addDisqueDur, name='addDisqueDur'),
    path('gestion/DisqueDur/delete/<int:pk>/', deleteDisqueDur, name='deleteDisqueDur'),
    path('gestion/DisqueDur/update/<int:pk>/', updateDisqueDur, name='updateDisqueDur'),

    path('gestion/Case/', gestionCases, name='gestionCases'),
    path('gestion/Case/add', addCase, name='addCase'),
    path('gestion/Case/delete/<int:pk>/', deleteCase, name='deleteCase'),
    path('gestion/Case/update/<int:pk>/', updateCase, name='updateCase'),

    path('gestion/PowerSupply/', gestionPowerSupplys, name='gestionPowerSupplys'),
    path('gestion/PowerSupply/add', addPowerSupply, name='addPowerSupply'),
    path('gestion/PowerSupply/delete/<int:pk>/', deletePowerSupply, name='deletePowerSupply'),
    path('gestion/PowerSupply/update/<int:pk>/', updatePowerSupply, name='updatePowerSupply'),

    path('gestion/SoundCard/', gestionSoundCards, name='gestionSoundCards'),
    path('gestion/SoundCard/add', addSoundCard, name='addSoundCard'),
    path('gestion/SoundCard/delete/<int:pk>/', deleteSoundCard, name='deleteSoundCard'),
    path('gestion/SoundCard/update/<int:pk>/', updateSoundCard, name='updateSoundCard'),

    path('gestion/NetworkCard/', gestionNetworkCards, name='gestionNetworkCards'),
    path('gestion/NetworkCard/add', addNetworkCard, name='addNetworkCard'),
    path('gestion/NetworkCard/delete/<int:pk>/', deleteNetworkCard, name='deleteNetworkCard'),
    path('gestion/NetworkCard/update/<int:pk>/', updateNetworkCard, name='updateNetworkCard'),


    path('articles', articles, name='articles'),

    path('article/<int:pk>/', article, name='article'),

    path('profile/<int:pk>/', profile, name='profile'),
    path('profilePhotoUpadte/', profilePhotoUpadte, name='profilePhotoUpadte'),

    path('deletecard/', deletecard, name='deletecard'),

    path('addcard/', addcard, name='addcard'),

    path('updatedata/', updatedata, name='updatedata'),

    path('passwordUpdate/', passwordUpdate, name='passwordUpdate'),


    path('addshopcard/', addshopcard, name='addshopcard'),

    path('deleteItemFromCard/<int:pk>/', deleteItemFromCard, name='deleteItemFromCard'),

    path('validerPainer/', validerPainer, name='validerPainer'),

    path('achatverfication/', achatverfication, name='achatverfication'),

    path('achat/', achat, name='achat'),

    path('demmand/', demmand, name='demmand'),

    path('demmand/<int:pk>/', DeleteDemmand, name='DeleteDemmand'),

    path('AccepterDemmandclient/<int:pk>/', AccepterDemmandclient, name='AccepterDemmandclient'),

    path('historique/', historique, name='historique'),

    path('ReturnDemmand/<int:pk>/', ReturnDemmand, name='ReturnDemmand'),

    path('ReturnDemmandPage/', ReturnDemmandPage, name='ReturnDemmandPage'),

    path('ListAttendPage/', ListAttendPage, name='ListAttendPage'),

    path('addListAttendPage/<int:pk>/', addListAttendPage, name='addListAttendPage'),

    path('deleteListAttendPage/<int:pk>/', deleteListAttendPage, name='deleteListAttendPage'),

    path('outOfStock/', outOfStock, name='outOfStock'),

    path('demmand_t/', demmand_t, name='demmand_t'),

    path('acceptDemmand/<int:pk>/', acceptDemmand, name='acceptDemmand'),

    path('returnarticle/', returnarticle, name='returnarticle'),

    path('acceptReturn/<int:pk>/', acceptReturn, name='acceptReturn'),

    path('refuserReturn/<int:pk>/', refuserReturn, name='refuserReturn'),

    path('statistique/', statistique, name='statistique'),

    path('confpc/', confpc, name='confpc'),

    path('cpuselected/', cpuselected, name='cpuselected'),

    path('fanselected/', fanselected, name='fanselected'),
    


    path('moderselected/', moderselected, name='moderselected'),

    path('ramselected/', ramselected, name='ramselected'),
    
    path('graphselecte/', graphselecte, name='graphselecte'),
    

]