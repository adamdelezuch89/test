from django.db import models
from django.utils import timezone

# Create your models here.


class Task(models.Model):
    task_prompt = models.TextField(help_text="Treść zadania do wykonania przez agenta")
    task_output = models.TextField(
        blank=True, null=True, help_text="Wynik zwrócony przez agenta"
    )
    created = models.DateTimeField(
        default=timezone.now, help_text="Data utworzenia zadania"
    )
    updated = models.DateTimeField(
        auto_now=True, help_text="Data ostatniej aktualizacji"
    )

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"Task {self.id}: {self.task_prompt[:50]}..."


class Run(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="runs",
        help_text="Powiązane zadanie",
    )
    created = models.DateTimeField(default=timezone.now, help_text="Data uruchomienia")
    execution_time = models.FloatField(
        null=True, blank=True, help_text="Czas wykonania w sekundach"
    )

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"Run {self.id} for Task {self.task_id}"
