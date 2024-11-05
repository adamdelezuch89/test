from celery import shared_task
from django.utils import timezone
from langchain_core.prompts import PromptTemplate
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
import os

search = DuckDuckGoSearchRun()

# Definiujemy template dla prompta
PROMPT_TEMPLATE = """
Znajdź odpowiedź w sieci na pytanie użytkownika  {task_prompt}
"""


@shared_task
def run_agent_task(task_id):
    from .models import Task, Run

    start_time = timezone.now()

    try:
        task = Task.objects.get(id=task_id)

        # Inicjalizacja modelu językowego
        llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

        # Inicjalizacja agenta
        agent = initialize_agent(
            tools=[search],
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
        )

        # Przygotowanie prompta
        prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)
        final_prompt = prompt.format(task_prompt=task.task_prompt)

        # Uruchomienie agenta i otrzymanie odpowiedzi
        response = agent.run(final_prompt)

        # Zapisanie odpowiedzi
        task.task_output = response
        task.save()

        # Zapisanie informacji o uruchomieniu
        execution_time = (timezone.now() - start_time).total_seconds()
        Run.objects.create(task=task, execution_time=execution_time)

        return f"Task {task_id} completed successfully"

    except Task.DoesNotExist:
        return f"Task {task_id} not found"
    except Exception as e:
        return f"Error processing task {task_id}: {str(e)}"
