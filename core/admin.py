from django.contrib import admin
from .models import Task, Run

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'task_prompt', 'created', 'updated']
    readonly_fields = ['task_prompt', 'task_output', 'created', 'updated']
    
    def has_add_permission(self, request):
        return False

@admin.register(Run)
class RunAdmin(admin.ModelAdmin):
    list_display = ['id', 'task', 'created', 'execution_time']
    readonly_fields = ['task', 'created', 'execution_time']
    
    def has_add_permission(self, request):
        return False
