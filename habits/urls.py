from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('habits/new/', views.habit_create_view, name='habit_create'),
    path('habits/<int:habit_id>/edit/', views.habit_edit_view, name='habit_edit'),
    path('habits/<int:habit_id>/delete/', views.habit_delete_view, name='habit_delete'),
    path('habits/<int:habit_id>/toggle-today/', views.habit_toggle_today_view, name='habit_toggle_today'),
]

