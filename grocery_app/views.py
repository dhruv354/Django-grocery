from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import MyRegisterForm
from django.urls import reverse
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
        'groceries': Grocery.objects.all().order_by('-time')
    }
    return render(request, 'grocery_app/home.html', context)


class GroceryListView(LoginRequiredMixin,ListView):
    model = Grocery
    template_name = 'grocery_app/home.html'
    context_object_name = 'groceries'
    ordering = ['-time']

class GroceryCreateView(LoginRequiredMixin, CreateView):
    model = Grocery
    fields = ['name', 'price', 'quantity', 'time']
    success_url = '/'
    # template_name = 'grocery_app/home.html'

    def form_valid(self, form):
     
        return super().form_valid(form)
       

class GroceryUpdateView(LoginRequiredMixin, UpdateView):
    model = Grocery
    fields = ['name', 'price', 'quantity']
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.is_superuser:
            return True
        return False

class GroceryDeleteView(LoginRequiredMixin, DeleteView):
    model = Grocery
    success_url = "/"

class PersonGroceryListView(LoginRequiredMixin, ListView):
    model = Person
    template_name = 'grocery_app/saved.html'
    context_object_name = 'Data'

def PersonSavedList(request):
    if not User.is_authenticated():
        return redirect('login')
    context = {
        'groceries': Person.objects.filter(user=request.user).order_by('-time')
    }
    return render(request, 'grocery_app/saved.html', context)

def PersonSavedUpdateView(request, id):
    if not User.is_authenticated():
        return redirect('login')
    if not id:
        print("error")
        return
    person = Person.objects.filter(user=request.user).first()
    grocery = Grocery.objects.filter(id=id).first()
    person.groceries.add(grocery)
    person.save()

    context = {
        'groceries': Person.objects.filter(user=request.user).order_by('-time')
    }
    return render(request, 'grocery_app/saved.html', context)
    

def PersonSavedDeleteView(request, id):
    if not User.is_authenticated():
        return redirect('login')
    if not id:
        print("error")
        return
    person = Person.objects.filter(user=request.user).first()
    grocery = Grocery.objects.filter(id=id).first()
    person.groceries.remove(grocery)
    person.save()

    context = {
        'groceries': Person.objects.filter(user=request.user).order_by('-time')
    }
    return render(request, 'grocery_app/saved.html', context)
    


    

