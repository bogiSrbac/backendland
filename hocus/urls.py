from django.urls import path
from . import views

new_app = 'hocus'

urlpatterns = [
    path('', views.index, name='hocus-index'),
    path('create-defender/', views.createDefenders, name='create'),
    path('play-game/', views.play_game, name='paly-game'),
    path('create-nick/<str:var_X>/', views.sendNick, name='create-nick'),
    path('create-first-round/', views.createFirstRound, name='create-first-round'),
    path('hocus-won/', views.hocusWon, name='hocus-won'),
    path('pocus-won/', views.pocusWon, name='pocus-won'),
]