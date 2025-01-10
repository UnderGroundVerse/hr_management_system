from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from .views import *


app_name = 'hr_manage'


urlpatterns = [
    path('', DashBoardTempalateView.as_view(),name='dashboard'),
    
    path('meetings/',  MeetingListView.as_view(),name='meeting-list'),
    path('meeting/create/',  MeetingCreateView.as_view(),name='meeting-create'),
    path('meeting/update/<pk>/', MeetingUpdateView.as_view(),name='meeting-update'),
    path('meeting/delete/<pk>/',  MeetingDeleteView.as_view(),name='meeting-delete'),
    path('meeting/detail/<pk>',  MeetingDetailView.as_view(),name='meeting-detail'),
    
    path('evaluate/meeting/<pk>', MeetingEvaluationMultiCreateView.as_view(),name='evaluate-meeting-multi-create'),
    
    
    path('members/', EmployeeListView.as_view(), name='member-list'),
    
    path('warnings/', WarningListView.as_view(), name='warning-list'),
    path('warning/create/', WarningCreateView.as_view(), name='warning-create'),
    path('warning/create/<pk>', WarningCreateView.as_view(), name='warning-create'),
    path('warning/update/<pk>/', WarningUpdateView.as_view(), name='warning-update'),
    path('warning/delete/<pk>/', WarningDeleteView.as_view(), name='warning-delete'),
    path('warning/detail/<pk>/', WarningDetailView.as_view(), name='warning-detail'),

]