from django.urls import path
from . import views

urlpatterns = [
    path('', views.game_list, name='game_list'),
    path('search/', views.game_search, name='game_search'),
    path('<int:pk>/', views.game_detail, name='game_detail'),
    path('rawg/<int:game_id>/', views.rawg_game_detail, name='rawg_game_detail'),
    path('library/', views.user_library, name='user_library'),
    path('library/<int:rawg_id>/status/', views.toggle_user_game_status, name='toggle_user_game_status'),
    path('library/<int:rawg_id>/remove/', views.remove_user_game, name='remove_user_game'),
    path('wishlist/', views.wishlist_view, name='wishlist_view'),
    path('wishlist/<int:rawg_id>/toggle/', views.toggle_wishlist, name='toggle_wishlist'),
]
