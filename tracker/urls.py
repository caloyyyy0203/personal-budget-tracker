from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='tracker/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add/', views.add_entry, name='add_entry'),
    path('entry/edit/<int:entry_id>/', views.edit_entry, name="edit_entry"),
    path('export_csv/', views.export_csv, name='export_csv'),
    path('delete_entry/<int:id>/', views.delete_entry, name='delete_entry'),
    path('set_budget/', views.set_budget, name='set_budget'),
    path('get_budget_for_category/<int:category_id>/', views.get_budget_for_category, name='get_budget_for_category'),


    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', views.category_update, name='category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    path('get_categories/', views.get_categories, name='get_categories'),
]
