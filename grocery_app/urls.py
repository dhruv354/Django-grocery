
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
   path('register/', views.register, name='register'),
   path('login/', auth_views.LoginView.as_view(template_name='grocery_app/login.html'), name='login'),
   path('logout/', auth_views.LogoutView.as_view(template_name='/logout.html'), name='logout'),
   path('', views.GroceryListView.as_view(), name='home'),
   path('create-grocery/', views.GroceryCreateView.as_view(), name='create-grocery'),
   path('update-grocery/<int:pk>/', views.GroceryUpdateView.as_view(), name='update-grocery'),
   path('delete-grocery/<int:pk>/', views.GroceryDeleteView.as_view(), name='delete-grocery'),
   path('saved/', views.PersonSavedList, name='saved'),
   path('update-saved-grocery/<int:id>/', views.PersonSavedUpdateView, name='update-saved-grocery'),
   path('delete-saved-grocery/<int:id>/', views.PersonSavedDeleteView, name='delete-saved-grocery'),
]
