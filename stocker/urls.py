from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('add_stock/', views.add_stock, name='add_stock'),
    path('get_graph/<str:symbol>/<str:period>/', views.get_graph, name='get_graph'),
    path('get_arbitrage/<str:xSymbol>/<str:ySymbol>/<str:period>/', views.get_arbitrage, name='get_arbitrage'),
    path('get_stock_info/<str:symbol>/', views.get_stock_info, name='get_stock_info'),
    path('get_index/<str:index>/', views.get_index, name='get_index'),
    path('get_portfolio/', views.get_portfolio, name='get_portfolio'),
    #Authentication Urls
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]
