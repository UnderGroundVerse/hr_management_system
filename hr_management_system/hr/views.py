from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, View
from Employees.models import *
from Employees.models import *
from .forms import *
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.forms import BaseModelForm, formset_factory
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.mixins import AccessMixin
from django.utils import timezone
from datetime import timedelta
# Create your views here.
        





class DashBoardTempalateView(LoginRequiredMixin, TemplateView):
    template_name = 'hr/dashboard.html'
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        user_teams = Hrrole.objects.raw("""
        SELECT *
        FROM Employees_team
        INNER JOIN hrrole_teams ON (team.id = hrrole_teams.team_id);
        """)
        context['teams'] = Hrrole.objects.raw("""
        SELECT et.id, et.name, et.description 
        FROM team et
        INNER JOIN hrrole_teams hrt ON et.id = hrt.team_id;
        """)
        context['own_meetings'] = Hrrole.objects.raw("""
        SELECT *
        FROM meeting hm
        INNER JOIN meeting_teams hmt ON hm.id = hmt.meeting_id
        WHERE hmt.team_id IN (
       SELECT et.id
        FROM team et
        INNER JOIN hrrole_teams hrt ON et.id = hrt.team_id
            )
        ORDER BY hm.created_at DESC, hm.updated_at DESC
        LIMIT 3;
        """)
        context['unevaluated_meetings'] = Hrrole.objects.raw("""
        SELECT *
        FROM meeting hm
        INNER JOIN meeting_teams hmt ON hm.id = hmt.meeting_id
        WHERE hm.evaluated = FALSE
        AND hmt.team_id IN (
            SELECT et.id
            FROM team et
            INNER JOIN hrrole_teams hrt ON et.id = hrt.team_id
        )
        ORDER BY hm.created_at DESC, hm.updated_at DESC
        LIMIT 3;
        """)
        return context




    
    
class MeetingListView(LoginRequiredMixin, ListView):
    model = Meeting
    template_name = 'hr/meeting_list.html'
    context_object_name = 'meetings'
    paginate_by = 30

    def get_queryset(self):
        query = self.model.objects.raw("""
        SELECT *
        FROM meeting
        ORDER BY meeting.created_at DESC, meeting.updated_at DESC;
        """)
        return query
    
class MeetingDetailView(LoginRequiredMixin,  DetailView):
    model = Meeting
    template_name = 'hr/meeting_detail.html'
    context_object_name = 'meeting'
    
    
class MeetingCreateView(LoginRequiredMixin, CreateView):
    model = Meeting
    form_class = MeetingForm
    template_name = 'hr/meeting_form.html'
    success_url = reverse_lazy('hr_manage:meeting-list') 
    
    

    def form_valid(self, form):
       
        form.instance.created_by = self.request.user  
        
        return super().form_valid(form)
        

class MeetingUpdateView(LoginRequiredMixin, UpdateView):
    model = Meeting
    form_class = MeetingForm
    template_name = 'hr/meeting_form.html'
    success_url = reverse_lazy('hr_manage:meeting-list')
    
    
    
    
    
class MeetingDeleteView(LoginRequiredMixin,  DeleteView):
    model = Meeting
    template_name = 'hr/meeting_delete.html'
    success_url = reverse_lazy('hr_manage:meeting-list')
    
    
    
class MeetingEvaluationMultiCreateView(LoginRequiredMixin,  View):
    template_name = 'hr/meeting_evaluation_multi_form.html'
    success_url = reverse_lazy('hr_manage:meeting-list')

    def get(self, request, *args, **kwargs):
        meeting_id = kwargs.get('pk')
        meeting = get_object_or_404(Meeting, pk=meeting_id)

        members = Employee.objects.raw("""
        SELECT *
        FROM employee
        ORDER BY employee.full_name ASC;
        """)
        formset_class = formset_factory(MeetingEvaluationForm, extra=len(members))
        formset = formset_class()
        formset_form_members = []

        for i, form in enumerate(formset):
            member = Employee.objects.get(pk=members[i].id)
            form.initial = {
                'task': 0,
                'attendance': 0,
                'performance': 0,
                'behavior': 0,
                'interaction': 0,
                'bonus': 0,
                'comment': 0,
            }
            
            form.initial['member']= member
            form.initial['meeting'] = meeting
            formset_form_members.append([form, member])
    

        return render(request, self.template_name, {'formset_form_members': formset_form_members, 'meeting': meeting, 'formset': formset_class})

    def post(self, request, *args, **kwargs):
        meeting_id = kwargs.get('pk')
        meeting = get_object_or_404(Meeting, pk=meeting_id)

        members = Employee.objects.raw("""
        SELECT *
        FROM employee
        ORDER BY employee.full_name ASC;
        """)
        formset_class = formset_factory(MeetingEvaluationForm, extra=len(members))
        formset = formset_class(request.POST)
            

        if formset.is_valid():
            meeting.evaluated = True
            meeting.save()
            for form in formset:
                evaluation = form.save(commit=False)
                
                evaluation.meeting = meeting
                evaluation.created_by = request.user
                evaluation.save()
            return redirect(self.success_url)
        else:
           
            print("Formset Errors:", formset.errors)
     
        

        return render(request, self.template_name, {'formset': formset, 'meeting': meeting})
    
    

class EmployeeListView(LoginRequiredMixin, ListView):
    model = Rating
    template_name = 'hr/member_list.html' 
    context_object_name = 'ratings'  
    paginate_by = 20
    
    def get_queryset(self):
        queryset = self.model.objects.raw("""
        SELECT *
        FROM rating
        """)
        return queryset


    
        


    
    
class WarningListView(LoginRequiredMixin, ListView):
    model = Warnings
    template_name = 'hr/warning_list.html'
    context_object_name = 'warnings'
    paginate_by = 30


class WarningCreateView(LoginRequiredMixin,CreateView):
    model = Warnings
    form_class = WarningForm
    template_name = 'hr/warning_form.html'
    success_url = reverse_lazy('hr_manage:warning-list')
    
    
    def get_initial(self):
        initial = super().get_initial()
        pk = self.kwargs.get('pk')

        if pk:
            member = get_object_or_404(Employee, pk=pk)
            initial['member'] = member  # Pre-populate the 'member' field
        return initial
    
    def form_valid(self, form):
        return super().form_valid(form)


class WarningUpdateView(LoginRequiredMixin,  UpdateView):
    model = Warnings
    form_class = WarningForm
    template_name = 'hr/warning_form.html'
    success_url = reverse_lazy('hr_manage:warning-list')


class WarningDeleteView(LoginRequiredMixin, DeleteView):
    model = Warnings
    template_name = 'hr/warning_delete.html'
    success_url = reverse_lazy('hr_manage:warning-list')
    
    
class WarningDetailView(LoginRequiredMixin,   DetailView):
    model = Warnings
    template_name = 'hr/warning_detail.html'
    context_object_name = 'warning'
    
