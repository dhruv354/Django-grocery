from typing import ValuesView
from django import urls
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import MyRegisterForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import *
from rest_framework import response
import datetime
from django.contrib import messages
import re
from rest_framework.response import Response

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = MyRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'successfully created account for {username}')
            return redirect('login')
        else:
            print('some error')
    else:
        form = MyRegisterForm()
    return render(request, 'grocery_app/register.html', {'form': form})


def home(request):
    if not User.is_authenticated():
        return redirect('login')
    context = {
        'groceries': Grocery.objects.all()
    }
    return render(request, 'grocery_app/home.html', context)


# def home2(request):
#     if not User.is_authenticated():
#         return redirect('login')
#     context = {
#         'GroceryList': GroceryList.objects.filter(user=request.user)[0]
#     }
#     return render(request, 'grocery_app/home.html', context)


class GroceryItemListView(LoginRequiredMixin,ListView):
    login_url = 'login/'
    model = Grocery
    template_name = 'grocery_app/home.html'
    context_object_name = 'groceries'
    # ordering = ['-time']


class GroceryCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login/'
    model = Grocery
    fields = ['name', 'price', 'quantity']
    success_url = '/'
    # template_name = 'grocery_app/home.html'

    def form_valid(self, form):
     
        return super().form_valid(form)
       

class GroceryUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login/'
    model = Grocery
    fields = ['name', 'price', 'quantity', 'status']
    success_url = '/'
   
    

    # def test_func(self):
    #     post = self.get_object()
    #     if self.request.is_superuser:
    #         return True
    #     return False

class GroceryUpdateViewList(LoginRequiredMixin, UpdateView):
    login_url = 'login/'
    model = Grocery
    fields = ['quantity', 'status']
    def get_success_url(self):
        temp = str(self.kwargs['date']).split('-')
        temp = reversed(temp)
        temp = "-".join(temp)
        return '/view-grocery/' + temp

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        return Grocery.objects.filter(id=self.kwargs['pk']).first()

# class GroceryDeleteViewList(LoginRequiredMixin, DeleteView):
#     login_url = 'login/'
#     model = GroceryList

#     def get_success_url(self):
#         temp = str(self.kwargs['date']).split('-')
#         temp = reversed(temp)
#         temp = "-".join(temp)
#         return '/view-grocery/' + temp

#     def get_object(self, queryset=None):
#         if queryset is None:
#             queryset = self.get_queryset()
#         temp = str(self.kwargs['date']).split('-')
#         temp = reversed(temp)
#         temp = "-".join(temp)
#         date = datetime.datetime.strptime(temp, '%d-%m-%Y')
#         return GroceryList.objects.filter(user=self.request.user).filter(time=date).filter(groceries__id=self.kwargs['pk']).first()

# class GroceryCreateViewList(LoginRequiredMixin, CreateView):
#     model = GroceryList
#     login_url = 'login/'
#     fields = ['groceries']
    
#     def get_success_url(self):
#         temp = str(self.kwargs['date']).split('-')
#         temp = reversed(temp)
#         temp = "-".join(temp)
#         return '/view-grocery/' + temp
    
#     def get_object(self, queryset=None):
#         if queryset is None:
#             queryset = self.get_queryset()
#         temp = str(self.kwargs['date']).split('-')
#         temp = reversed(temp)
#         temp = "-".join(temp)
#         grocery = self.request.GET.get('groceries')
#         date = datetime.datetime.strptime(temp, '%d-%m-%Y')
#         return GroceryList.objects.filter(user=self.request.user).filter(time=date).first()
    
#     def get_context_data(self, **kwargs):
#         data = super().get_context_data(**kwargs)
#         print(data)

#     def post(self, request, date):
#         grocery = self.request.GET.get('Groceries')
#         # print(self.request.body['groceries'])
#         # print("here")
#         # print(grocery)
#         # print(self.get_context_data())
#         grocery = Grocery.objects.filter(name=grocery)[0]
#         temp = str(self.kwargs['date']).split('-')
#         temp = reversed(temp)
#         temp = "-".join(temp)
#         grocery = Grocery.objects.get(name=grocery)
#         date = datetime.datetime.strptime(temp, '%d-%m-%Y')
#         my_groceries = GroceryList.objects.filter(user=self.request.user).filter(time=date).first()
#         my_groceries.groceries.add(grocery)
#         my_groceries.save()
#         return my_groceries



def GroceryCreateViewList(request, date):
    temp = str(date).split('-')
    temp = reversed(temp)
    temp = "-".join(temp)
    groceries = Grocery.objects.all()
    print("hello")
    return render(request, 'grocery_app/add_grocery_list_item.html', {'groceries': groceries, 'date': temp})

def AddGroceryListItem(request):
    date = request.GET.get('date', '')
    grocery = request.GET.get('item', )
    print(date)
    date = datetime.datetime.strptime(date, '%d-%m-%Y')
    grocery_list = GroceryList.objects.filter(user=request.user).filter(time=date).first()
    print(grocery_list)
    grocery = Grocery.objects.filter(name=grocery).first()
    grocery_list.groceries.add(grocery)
    grocery_list.save()
    temp = str(date.date()).split('-')
    temp = reversed(temp)
    temp = "-".join(temp)
    return redirect("/view-grocery/" + temp)

def GroceryDeleteViewList(request, pk, date):
    temp = str(date).split('-')
    temp = reversed(temp)
    temp = "-".join(temp)
    date = datetime.datetime.strptime(temp, '%d-%m-%Y')
    my_list = GroceryList.objects.filter(user=request.user).filter(time=date)[0]
    
    grocery = Grocery.objects.get(id=pk)
    my_list.groceries.remove(grocery)
    my_list.save()
    return redirect("/view-grocery/" + temp)


        

# def GroceryUpdateViewList(request, pk, date):

#     if not request.user.is_authenticated:
#         return redirect('login')
#     if not pk:
#        return redirect('login')
#     temp = date.split('-')
#     temp = reversed(temp)
#     temp = "-".join(temp)
#     grocery = Grocery.objects.filter(id=pk)[0]
#     if grocery.status == 'Not available':
#         return redirect(reverse('view-grocery') + '?search-text=' + temp)
#     if grocery.status == 'Pending':
#         grocery.status = 'Bought'
#     else:
#         grocery.status = 'Pending'
#     grocery.save()

#     print(temp)
#     # try:
#     #     date = datetime.datetime.strptime(temp, '%d-%m-%y')
#     # except ValueError as v:
#     #     print(v)
#     # print(date)
#     return redirect(reverse('view-grocery') + '?search-text=' + temp)


class GroceryDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login/'
    model = Grocery
    success_url = "/"


def GroceryListView(request, time):
    if not request.user.is_authenticated:
        return redirect('login')
    groceries = GroceryList.objects.filter(time=datetime.datetime.strptime(time, '%d-%m-%Y'))[0].groceries.all()
    list = []
    for grocery in groceries:
        list.append(grocery)
    context={
        'groceries' : list
    }
    return render(request, 'grocery_app/home2.html', context)

def helper1(request):
    yyyy = request.GET.get('search-text', '')
    return HttpResponseRedirect('/view-grocery/' + yyyy)

def helper(request, date):
    # date.date()
    
    temp = str(date.date()).split('-')
    # except AttributeError:
    #      messages.success(request, 'Wrong date format')
    #      return redirect("/")
    temp = reversed(temp)
    temp = "-".join(temp)
    input_value = temp
    print(input_value)
    input_value = str(input_value)
    if input_value == 'N/A':
        date = datetime.datetime.now().date()
    else:
        try:
            res = datetime.datetime.strptime(str(input_value), '%d-%m-%Y')
        except ValueError:
            context = {
            'groceries' : 'Na'
            }
            messages.success(request, 'wrong date format, try again!!!')
            return redirect("/")
        date = datetime.datetime.strptime(str(input_value), '%d-%m-%Y')
        print(date.date())
    
    
    temp = GroceryList.objects.filter(user=request.user).filter(time=datetime.datetime.strptime(input_value, '%d-%m-%Y')).first()
    print("here2")
    print(temp)
    
    if temp is  None:
        context = {
            'groceries' : None
        }
        messages.success(request, 'No list with this date create a new list')
        return redirect("/")
    groceries = GroceryList.objects.filter(user=request.user).filter(time=datetime.datetime.strptime(input_value, '%d-%m-%Y'))[0].groceries.all()
    list = []
    for grocery in groceries:
        list.append(grocery)
    context = {
        'groceries': list,
        'date' : date.date(),
    }
    return render(request, 'grocery_app/home2.html', context)
    
        
def helper_(request, date):
    messages.success(request, 'Wrong date format')
    return redirect("/")


# class PersonGroceryListView(LoginRequiredMixin, ListView):
#     model = Person
#     template_name = 'grocery_app/saved.html'
#     context_object_name = 'Data'

# def PersonSavedList(request):
#     if not User.is_authenticated():
#         return redirect('login')
#     context = {
#         'groceries': Person.objects.filter(user=request.user).order_by('-time')
#     }
#     return render(request, 'grocery_app/saved.html', context)

# def PersonSavedUpdateView(request, id):
#     if not User.is_authenticated():
#         return redirect('login')
#     if not id:
#         print("error")
#         return
#     person = Person.objects.filter(user=request.user).first()
#     grocery = Grocery.objects.filter(id=id).first()
#     person.groceries.add(grocery)
#     person.save()

#     context = {
#         'groceries': Person.objects.filter(user=request.user).order_by('-time')
#     }
#     return render(request, 'grocery_app/saved.html', context)
    

# def PersonSavedDeleteView(request, id):
#     if not User.is_authenticated():
#         return redirect('login')
#     if not id:
#         print("error")
#         return
#     person = Person.objects.filter(user=request.user).first()
#     grocery = Grocery.objects.filter(id=id).first()
#     person.groceries.remove(grocery)
#     person.save()

#     context = {
#         'groceries': Person.objects.filter(user=request.user).order_by('-time')
#     }
#     return render(request, 'grocery_app/saved.html', context)
    


def CompleteGroceryList(request):
    groceryList = GroceryList.objects.filter(user=request.user).all()
    groceries = groceryList.groceries.all()
    context = {
        'groceryList': groceryList,
        'groceries' : groceries
    }    
    return render(request, 'grocery_app/complete_list.html', context)

def SaveList(request, date):
    temp = str(date).split('-')
    temp = reversed(temp)
    temp = "-".join(temp)
    date = datetime.datetime.strptime(temp, '%d-%m-%Y')
    my_list = GroceryList.objects.filter(user=request.user).filter(time=date)[0]
    try:
        saved_list = Saved.objects.filter(user=request.user).first()
    except:
        saved_list = Saved(user=request.user)
    if saved_list is None:
        saved_list = Saved(user=request.user)
    saved_list.save()
    print(saved_list)
    print(saved_list.id)
    saved_list.groceryList.add(my_list)
    saved_list.save()
    messages.success(request, 'List Successfully saved')
    return redirect("/view-grocery/" + temp)

# class NewList(LoginRequiredMixin, CreateView):
#     model = GroceryList
#     fields = ['time']
#     success_url = '/'
#     login_url = 'login/'
#     template_name = 'create_new_list.html'

#     def post(self, request):
#         pass

def NewListTemplate(request):
    return render(request, 'grocery_app/create_new_list.html')

def CreateNewList(request):
    input_value = request.GET.get('search-text')
    print(input_value)
    result = re.match('\d{2}-\d{2}-\d{4}', input_value)
    if result is None:
        messages.success(request, 'Wrong Date format')
        return redirect('/')
    date = datetime.datetime.strptime(str(input_value), '%d-%m-%Y').date()
    print(date)
    temp = GroceryList.objects.filter(user=request.user).filter(time=date).first()
    if temp is not None:
         return redirect('/view-grocery/' + input_value)
    x = GroceryList(user=request.user, time=date)
    x.save()
    messages.success(request, 'List Successfully Created')
    return redirect('/view-grocery/' + input_value)

def DeleteList(request, date):
    temp = str(date).split('-')
    temp = reversed(temp)
    temp = "-".join(temp)
    date = datetime.datetime.strptime(temp, '%d-%m-%Y')
    my_list = GroceryList.objects.filter(user=request.user).filter(time=date)
    my_list.delete()
    messages.success(request, 'List Successfully deleted')
    return redirect('/')


def MySavedList(request):
    # login_url = 'login/'
    # model = Saved
    # template_name = 'grocery_app/saved.html'
    # context_object_name = 'SavedList'
    saved_list = Saved.objects.filter(user=request.user).first().groceryList.all()
    print(saved_list)
    time = []
    for i in saved_list:
        time.append(i.time)
    context = {
        'my_list' : saved_list,
        'time' : time,
    }
    return render(request, 'grocery_app/saved.html', context)


        


def helper2(request, date):
    return redirect('/view-grocery/' + date)

def helper3(request, pk):
    list = GroceryList.objects.filter(id=pk).first()
    saved_list = Saved.objects.filter(user=request.user).first()
    saved_list.groceryList.remove(list)
    saved_list.save()
    messages.success(request, 'List Successfully removed from saved')
    return redirect('my-saved-list')

class AllList(LoginRequiredMixin, ListView):
    model = GroceryList
    fields = ['time', 'user']
    template_name = 'grocery_app/mylists.html'
    login_url = 'login/'
    context_object_name = 'my_list'

def DeletemyList(request, pk):
    list = GroceryList.objects.filter(id=pk)
    list.delete()
    messages.success(request, 'your List Successfully deleted')
    return redirect('/all-created-list')
   

