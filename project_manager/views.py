from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404,render,redirect
from django.urls import reverse
from django.views import generic
from django.views.decorators.csrf import csrf_protect
from django.views.generic import View
from django.urls import reverse,reverse_lazy

from .models import Project,ProjectCreateForm,Task,TaskCreateForm


class ProjectListView(generic.ListView):
    template_name = 'project_manager/index.html'
    context_object_name = 'projects_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Project.objects.order_by('-create_date')[:5]

class CreateProjectView(View):
    form_class    =  ProjectCreateForm
    success_url   =  reverse_lazy('project_manager:index')
    template_name = 'project_manager/create_project.html'

    def get(self, request, *args, **kwargs):
        form_args  = {}
        create_obj = self.form_class(**form_args)
        return render(
            request,
            self.template_name,
            {
                'CreateProjectForm': create_obj
            }
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            return redirect(self.success_url)
        else:
            # return render(request, self.template_name, {'form': form})
            form_args = {}
            create_obj = self.form_class(**form_args)
            return render(
                request,
                self.template_name,
                {
                    'CreateProjectForm': create_obj
                }
            )

class EditProjectView(View):
    operating_form   =  ProjectCreateForm
    operating_model  =  Project
    success_url      =  reverse_lazy('project_manager:index')
    template_name    = 'project_manager/create_project.html'

    def get(self, request, project_id):
        row_instance  = self.operating_model.objects.get(id=project_id)
        form_obj      = self.operating_form(instance=row_instance)
        request.session['reverse_project_id'] = project_id
        return render(
            request,
            self.template_name,
            {
                'CreateProjectForm': form_obj
            }
        )

    def post(self, request, *args, **kwargs):
        project_id    = request.session['reverse_project_id']
        row_instance  = self.operating_model.objects.get(id=project_id)
        form          = self.operating_form(request.POST, request.FILES, instance=row_instance)
        if form.is_valid():
            print(" \t - Recieved form was valid.")
            form.save(commit=True)
            del request.session['reverse_project_id']
            return redirect(self.success_url)
        else:
            row_instance  = self.operating_model.objects.get(id=project_id)
            form_obj      = self.operating_form(instance=row_instance)
            return render(
                request,
                self.template_name,
                {
                    'CreateProjectForm': form_obj
                }
            )

class DeleteProjectView(View):
    operating_model = Project
    success_url     = reverse_lazy('project_manager:index')

    def get(self, request, project_id):
        search_query = self.operating_model.objects.get(id= project_id)
        
        search_query.delete()
        return redirect(self.success_url)

class DeleteTaskView(View):
    operating_model  = Task
    success_url      =  'project_manager:project_detail'

    def get(self, request, project_id, task_id):
        search_query = self.operating_model.objects.get(id= task_id)
        search_query.delete()
        success_url  = reverse_lazy(f"{self.success_url}",kwargs={'project_id': project_id})
        return redirect(success_url)

class DetailProjectView(View):
    project_model    =  Project
    task_model       =  Task
    success_url      =  reverse_lazy('project_manager:index')
    template_name    = 'project_manager/project_detail.html'

    def get(self, request, project_id):
        project        = self.project_model.objects.get(id= project_id)
        tasks          = self.task_model.objects.filter(project=project)
        request.session['reverse_project_name'] = project.project_name
        request.session['reverse_project_id'] = project.id
        # print(project_tasks)
        return render(
                request,
                self.template_name,
                {
                    'project': project,
                    'tasks': tasks
                }
            )
        # return redirect(self.success_url)

class CreateTaskView(View):
    form_class    =  TaskCreateForm
    success_url   =  reverse_lazy('project_manager:index')
    template_name = 'project_manager/create_task.html'

    def get(self, request, *args, **kwargs):
        form_args  = {}
        create_obj = self.form_class(**form_args)
        return render(
            request,
            self.template_name,
            {
                'CreateTaskForm': create_obj
            }
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            return redirect(self.success_url)
        else:
            # return render(request, self.template_name, {'form': form})
            form_args = {}
            create_obj = self.form_class(**form_args)
            return render(
                request,
                self.template_name,
                {
                    'CreateTaskForm': create_obj
                }
            )

class EditTaskView(View):
    operating_form  =  TaskCreateForm
    operating_model =  Task
    template_name   =  'project_manager/create_task.html'
    success_url     =  'project_manager:project_detail'

    def get(self, request, project_id, task_id):
        my_record  = self.operating_model.objects.get(id=task_id)
        form_obj   = self.operating_form(instance=my_record)

        request.session['reverse_project_id'] = project_id
        request.session['reverse_task_id']    = task_id
        # create_obj = self.form_class(**form_args)
        return render(
            request,
            self.template_name,
            {
                'CreateTaskForm': form_obj
            }
        )

    def post(self, request, *args, **kwargs):
        project_id    = request.session['reverse_project_id']
        task_id       = request.session['reverse_task_id']
        row_instance  = self.operating_model.objects.get(id=task_id)
        form          = self.operating_form(request.POST, request.FILES, instance=row_instance)
        if form.is_valid():
            form.save(commit=True)
            project_id     = request.session['reverse_project_id']
            success_url    = reverse_lazy(f"{self.success_url}",kwargs={'project_id': project_id})
            del request.session['reverse_project_id'], request.session['reverse_task_id']
            return redirect(success_url)
        else:
            # return render(request, self.template_name, {'form': form})
            row_instance  = self.operating_model.objects.get(id=task_id)
            form_obj      = self.operating_form(instance=row_instance)
            return render(
                request,
                self.template_name,
                {
                    'CreateTaskForm': form_obj
                }
            )
