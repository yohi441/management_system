
from django.urls import path 
from management_system import views


urlpatterns = [
    path('', views.login_view, name="login"),
    path('dashboard/', views.dashboard_view, name="dashboard"),
    path('logout/', views.logout_view, name="logout"),
    path('client/list/', views.client_list_view, name="all_client_list"),
    path('item/list/', views.item_list_view, name="all_item_list"),
    path('client/add/form/', views.client_form_view, name="client_form"),
    path('item/add/form/', views.item_form_view, name="item_form"),
]




