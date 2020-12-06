from django.urls import path

from . import views

app_name = 'project_manager'
urlpatterns = [
    path('', views.ProjectListView.as_view(), name='index'),
    path('new_entry', views.CreateProjectView.as_view(), name='create_project'),
    path('<int:project_id>/project_detail',views.DetailProjectView.as_view(), name='project_detail'),
    path('<int:project_id>/edit',views.EditProjectView.as_view(), name='edit_project'),
    path('<int:project_id>/delete',views.DeleteProjectView.as_view(), name='delete_project'),
    path('new_task', views.CreateTaskView.as_view(), name='create_task'),
    path('<int:project_id>/<int:task_id>/edit_task',views.EditTaskView.as_view(), name='edit_task'),
    path('<int:project_id>/<int:task_id>/delete_task',views.DeleteTaskView.as_view(), name='delete_task'),
]