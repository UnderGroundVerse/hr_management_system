from django import forms
from Employees.models import *
from django.core.validators import MaxValueValidator, MinValueValidator


class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = [
            'title',
            'description',
            'location',
            'scheduled_at',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Meeting Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter Meeting Description'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Meeting Location'}),
            'scheduled_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
     
        }




class MeetingEvaluationForm(forms.ModelForm):
    class Meta:
        model = Meetingevaluation
        fields = [
            'member', 
            'meeting', 
            'attendance', 
            'task', 
            'performance', 
            'interaction', 
            'behavior', 
            'bonus', 
            'comment'
        ]
        
        widgets = {
            'meeting': forms.HiddenInput(),
            'member': forms.HiddenInput(),
    
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Add any comments (optional)'}),
        }



        
class WarningForm(forms.ModelForm):
    class Meta:
        model = Warnings
        fields = ['employee', 'warning_type', 'notes', 'is_official']
        
        
