from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .views import profileView, profileUpdateView, EmployeeLoginView, EmployeeLogoutView
app_name = 'members'

urlpatterns = [
    path('profile/', profileView, name='profile'),
    path('profile/update/', profileUpdateView, name='profile_update'),
    path('login/', EmployeeLoginView.as_view(), name='login'),
    path('logout/', EmployeeLogoutView.as_view(), name='logout'),
    
]