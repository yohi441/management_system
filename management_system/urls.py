
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
    
    path('transaction/renew/<int:pk>', views.renew_transaction_view, name="transaction_renew"),
    path('transaction/paid/<int:pk>', views.paid_transaction_view, name="transaction_paid"),
    path('transaction/forfeit/<int:pk>', views.forfeit_item, name="transaction_forfeit"),
    
    
    path('transaction/pending/list/', views.transaction_list_pending_view, name="transaction_pending_list"),
    path('transaction/paid/list/', views.transaction_list_paid_view, name="transaction_paid_list"),
    path('transaction/renew/list/', views.transaction_list_renew_view, name="transaction_renew_list"),
    path('transaction/new/list/', views.transaction_list_new_view, name="transaction_new_list"),


    path('transaction/five/days/due/', views.five_days_before_due_date, name="five-days-due"),
    path('items/category/<int:pk>/', views.category_list_view, name="item_category")
    
]




