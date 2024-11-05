from celery import shared_task
from django.utils import timezone
from crewai import Agent, Task as CrewTask, Crew, LLM
from crewai_tools import SerperDevTool


@shared_task
def run_agent_task(task_id):
    from .models import Task, Run

    start_time = timezone.now()
    try:
        task = Task.objects.get(id=task_id)
        llm = LLM(model="gpt-3.5-turbo", temperature=0.7)

        search_tool = SerperDevTool()

        researcher = Agent(
            role="Researcher",
            goal="Find accurate and up-to-date information from the internet",
            backstory="""You are an expert researcher with a knack for finding
            accurate information online and summarizing it concisely.""",
            allow_delegation=False,
            llm=llm,
            tools=[search_tool],
        )

        # Tworzymy zadanie dla agenta
        research_task = CrewTask(
            description=f"Search the internet for: {task.task_prompt}. "
            f"Provide a clear and concise answer based on the search results.",
            expected_output="A clear and concise answer to the query, based on current information found online.",
            agent=researcher,
        )

        # Tworzymy crew i uruchamiamy zadanie
        crew = Crew(agents=[researcher], tasks=[research_task])

        # Uruchamiamy crew i otrzymujemy wynik
        result = crew.kickoff()

        # Zapisujemy wynik
        task.task_output = result
        task.save()

        # Zapisujemy informacje o uruchomieniu
        execution_time = (timezone.now() - start_time).total_seconds()
        Run.objects.create(task=task, execution_time=execution_time)

        return f"Task {task_id} completed successfully"

    except Task.DoesNotExist:
        return f"Task {task_id} not found"
    except Exception as e:
        return f"Error processing task {task_id}: {str(e)}"
