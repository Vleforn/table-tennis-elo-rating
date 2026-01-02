from django.urls import path, include
from . import views

urlpatterns = [
        path('', views.home, name='home'),
        path('player', views.player, name='player'),
        path('add_player', views.add_player, name='add_player'),
        path('match', views.match, name='match'),
        path('add_match', views.add_match, name='add_match'),
        path('rating', views.rating, name='rating'),
        path('controlcenter', views.control_center, name='control_center'),
        path('login_page', views.login_page, name='login_page'),
        path('logout', views.logout_user, name='logout_user'),
]
