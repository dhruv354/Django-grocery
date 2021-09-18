
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path, include, register_converter

from django.contrib.auth import views as auth_views
from . import views
import datetime


class DateConverter:
    regex = '\d{2}-\d{2}-\d{4}'

    def to_python(self, value):
        return datetime.datetime.strptime(value, '%d-%m-%Y')

    def to_url(self, value):
        return value

register_converter(DateConverter, 'yyyy')

urlpatterns = [
   path('register/', views.register, name='register'),
   path('login/', auth_views.LoginView.as_view(template_name='grocery_app/login.html'), name='login'),
   path('logout/', auth_views.LogoutView.as_view(template_name='grocery_app/logout.html'), name='logout'),
   path('', views.GroceryItemListView.as_view(), name='home'),
   path('create-grocery/', views.GroceryCreateView.as_view(), name='create-grocery'),
   path('update-grocery/<int:pk>/', views.GroceryUpdateView.as_view(), name='update-grocery'),
   path('delete-grocery/<int:pk>/', views.GroceryDeleteView.as_view(), name='delete-grocery'),
   path('view-helper/', views.helper1, name='views-helper'),
   path('view-grocery/<yyyy:date>', views.helper, name='view-grocery'),
   path('create-grocery-list/<str:date>/', views.GroceryCreateViewList, name='create-grocery-list'),
   path('update-grocery-list/<int:pk>/<str:date>/', views.GroceryUpdateViewList.as_view(), name='update-grocery-list'),
   path('remove-grocery-list/<int:pk>/<str:date>/', views.GroceryDeleteViewList, name='remove-grocery-list'),
   path('add-grocery-list-item/', views.AddGroceryListItem, name='add-grocery-list-item'),
   path('complete-grocery-list/', views.CompleteGroceryList, name='complete-grocery-list'),
   path('save-list/<str:date>', views.SaveList, name='save-list'),
   path('new-list-template/', views.NewListTemplate, name='new-list-template'),
   path('create-new-list/', views.CreateNewList, name='create-new-list')
   # path('update-saved-grocery/<int:id>/', views.PersonSavedUpdateView, name='update-saved-grocery'),
   # path('delete-saved-grocery/<int:id>/', views.PersonSavedDeleteView, name='delete-saved-grocery'),
]
