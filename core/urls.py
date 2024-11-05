from django.urls import path
from . import views

urlpatterns = [
    path("", views.TaskListView.as_view(), name="task-list"),
    path("task/new/", views.TaskCreateView.as_view(), name="task-create"),
    path("task/<int:task_id>/run/", views.run_agent, name="run-agent"),
]
