
from django.urls import path 
from management_system import views


urlpatterns = [
    path('', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),

    path('dashboard/', views.dashboard_view, name="dashboard"),
    path('search/', views.search_results_view, name="search_result"),

    path('client/list/', views.client_list_view, name="all_client_list"),
    path('item/list/', views.item_list_view, name="all_item_list"),
    path('transaction/list/', views.transaction_list_view, name="all_transaction_list"),

    path('client/add/form/', views.client_form_view, name="client_form"),
    path('item/add/form/', views.item_form_view, name="item_form"),
    path('transaction/add/form/', views.transaction_form_view, name="transaction_form"),

    
    path('client/<int:pk>/', views.client_detail_view, name="client_detail"),
    path('item/<int:pk>/', views.item_detail_view, name="item_detail"),
    path('transaction/<int:pk>/', views.transaction_detail_view, name="transaction_detail"),

    path('client/update/<int:pk>', views.client_update_view, name="client_update"),
    path('item/update/<int:pk>', views.item_update_view, name="item_update"),
    path('transaction/update/<int:pk>', views.transaction_update_view, name="transaction_update"),
    
]




