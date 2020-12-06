import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models

from django.db import models
from django.forms import ModelForm, ModelChoiceField
from django import forms
from django.contrib.admin import widgets  
from bootstrap_datepicker_plus import DatePickerInput, DateTimePickerInput

class Project(models.Model):
    project_name = models.CharField(max_length=200)
    description  = models.TextField()
    create_date  = models.DateTimeField('date create')
    avatar       = models.ImageField() 

    def __str__(self):
        return self.project_name

    def was_published_recently(self):
        return self.create_date >= timezone.now() - datetime.timedelta(days=1)

class Task(models.Model):
    title       = models.CharField(max_length=100)
    description = models.TextField()
    start_date  = models.DateField('date start')
    end_date    = models.DateField('date end')
    project     = models.ForeignKey(Project, on_delete=models.CASCADE)
    # assignee    = models.ForeignKey(
    #                 settings.AUTH_USER_MODEL,
    #                 on_delete=models.CASCADE,
    #             )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']

#..> forms.py

class ProjectCreateForm(ModelForm):
    project_name = forms.CharField(label='Project name',
                           max_length=100,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Project
        fields = ['project_name', 'description','create_date','avatar']  
        widgets = {
            'create_date': DatePickerInput(options={
                    "format": "MM/DD/YYYY", # moment date-time format
                    "showClose": True,
                    "showClear": True,
                    "showTodayButton": True
                })
        }

    def __init__(self, *args, **kwargs):
        super(ProjectCreateForm, self).__init__(*args, **kwargs)
        self.fields["avatar"].required = True
        

class TaskCreateForm(ModelForm):
    title = forms.CharField(label='Task name',
                           max_length=100,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.TextInput()
    class Meta:
        model  = Task
        fields = ['title', 'description', 'start_date','end_date','project']  
        widgets = {
            'start_date': DatePickerInput(options={
                    "format": "MM/DD/YYYY", # moment date-time format
                    "showClose": True,
                    "showClear": True,
                    "showTodayButton": True,
                }), # default date-format %m/%d/%Y will be used
            'end_date': DatePickerInput(options={
                    "format": "MM/DD/YYYY", # moment date-time format
                    "showClose": True,
                    "showClear": True,
                    "showTodayButton": True,
                }), # specify date-frmat
        }


    def __init__(self, *args, **kwargs):
        super(TaskCreateForm, self).__init__(*args, **kwargs)
        project = ModelChoiceField(queryset=Project.objects.all()) # Or whatever query you'd like
        
    

        
