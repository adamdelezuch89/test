from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Task
from .tasks import run_agent_task

# Create your views here.


class TaskListView(ListView):
    model = Task
    template_name = "core/task_list.html"
    context_object_name = "tasks"
    paginate_by = 20


class TaskCreateView(CreateView):
    model = Task
    template_name = "core/task_form.html"
    fields = ["task_prompt"]
    success_url = reverse_lazy("task-list")


def run_agent(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    # Uruchomienie taska Celery
    run_agent_task.delay(task_id)
    messages.success(request, "Agent został uruchomiony w tle.")
    return redirect("task-list")
