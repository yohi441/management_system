
from django.urls import path 
from management_system import views


urlpatterns = [
    path('', views.login_view, name="login"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('logout/', views.logout_view, name="logout")
]

htmx_urlpatterns = [
    path('client/list', views.all_client_list, name="all_client_list"),
    path('item/list', views.all_item_list, name="all_item_list")
]

urlpatterns += htmx_urlpatterns
