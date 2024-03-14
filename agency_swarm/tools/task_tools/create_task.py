from agency_swarm import BaseTool
from typing import List, Dict, Optional
from agency_swarm.tasks import States, Tags, Task
from pydantic import Field

class CreateTask(BaseTool):
    """
    This tool creates a new task object
    """
    description: str = Field(
    ..., description="Description of the task to be completed. include all relevant information and requirements",
        examples=["Create a two week mealplan based on the user's preferences and schedule","Create a shopping list and catagorize it based on nearby stores","check the weather for tomorrow"]
    )

    priority: int = Field(
        ..., description="relative task priority. 1 to 10 with 1 being the highest priority",
        examples=[1,2,3,4,5]
    )

    state: States = Field(
        ..., description="Desired state of the task. either avaialable or on hold. if on hold, add a tag to the task to indicate why it is on hold",
        examples=[States.AVAILABLE, States.ON_HOLD]
    )

    tags: Optional[Dict[Tags, str]] = Field(
        ..., description="Dictionary of tags to be added to the task with the keys being the tags and the values being the additional information",
        examples={Tags.AWAITING_APPROVAL: None, Tags.EXECUTE_TIME: "2021-01-01 12:00:00"}
    )

    files: Optional[List[str]] = Field(
        ..., description="List of file paths to be added to the task",
        examples=["file1.txt", "file2.txt"]
    )

    def run(self):
        task = Task(description=self.description, priority=self.priority, state=self.state, tags=self.tags, files=self.files)

        return task