from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import MyRegisterForm
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import *

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
    return render(request, 'blog/home.html', context)


class GroceryListView(LoginRequiredMixin,ListView):
    model = Grocery
    template_name = 'grocery_app/home.html'
    context_object_name = 'groceries'
    ordering = ['-time']
    paginate_by = 4

