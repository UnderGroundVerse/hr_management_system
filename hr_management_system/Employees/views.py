from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import MemberRegisterForm, MemberUpdateForm
from django.contrib.auth.models import User
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
import datetime
from django.core.exceptions import PermissionDenied
# Create your views here.



@login_required
def profileView(request):
    context = {
        'title': 'Profile'
    }
    return render(request, template_name='Employees/profile.html', context=context)

@login_required
def profileUpdateView(request):
    if request.method == 'POST':
        form = MemberUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('Employees:profile')
    else:
        form = MemberUpdateForm(instance=request.user)
    context = {
        'title': 'Edit Profile',
        'form': form
    }
    return render(request, 'Employees/profile_edit.html', context)




class EmployeeLoginView(LoginView):
    template_name = 'Employees/login.html'

    def get_context_data(self,**kwargs):
        context = super(EmployeeLoginView, self).get_context_data(**kwargs)
        context['title'] = 'Login'
        return context

class EmployeeLogoutView(LoginRequiredMixin, LogoutView):
    raise_exception = True
    template_name = 'Employee/logout.html'

    def get_context_data(self,**kwargs):
        context = super(EmployeeLogoutView, self).get_context_data(**kwargs)
        context['title'] = 'Logout'
        return context