from pydantic import Field

from agency_swarm import BaseTool

from agency_swarm.tasks.task import States
from agency_swarm.tasks.task_library import TaskLibrary

class ChangeTaskState(BaseTool):
    """
    This tool changes state of a task to one of the following: IN_PROGRESS, AVAILABLE, COMPLETE, ON_HOLD, CANCELLED, or ERROR.
    """
    state: States = Field(
       ..., description="Desired state of the task.",
        examples=[States.IN_PROGRESS, States.AVAILABLE, States.COMPLETE, States.ON_HOLD, States.CANCELLED, States.ERROR]
    )

    task_id: int = Field(
        ..., description="ID of the task.",
        examples=[1,2,3,4,5]
    )

    def run(self):
        task_library = TaskLibrary.get_current()

        if task_library:
            # Use the task_library object as needed
            task = task_library.query_tasks(filters={'task_id': self.task_id})[0]
            
            if task:
                task.state = self.state
                task_library.add_task(task)
            else:
                return "Task id not correct. Task not not found"

        else:
            return "No task library has been initialized on this thread. Halt Execution"

        return f"Task state has been changed to {self.state}."
