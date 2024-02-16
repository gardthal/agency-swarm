from sqlalchemy import Column, Integer, String, Enum, JSON
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PyEnum
from typing import List

Base = declarative_base()

class States(PyEnum):
    """
    Enum representing the possible states of a task.
    """
    IN_PROGRESS = "In progress"
    AVAILABLE = "Available"
    COMPLETE = "Complete"
    ON_HOLD = "On hold"
    CANCELLED = "Cancelled"
    ERROR = "Error"

class Task(Base):
    """
    Represents a task in the task library.
    """

    __tablename__ = 'task_library'

    task_id = Column(Integer, primary_key=True)  # Primary key
    state = Column(Enum(States), default=States.AVAILABLE)
    priority = Column(Integer)
    description = Column(String)
    assigned_agent = Column(String)
    files = Column(JSON)  # Storing files as JSON
    tags = Column(JSON)  # Storing tags as JSON
    thread_id = Column(String)

    def __init__(self, description: str, priority: int, thread_id: str = None, assigned_agent: str = None,
                 files: List[str] = None, tags: List[str] = None, state: States = States.AVAILABLE):
        """
        Initialize a new Task instance.

        :param description: str, description of the task
        :param priority: int, priority of the task
        :param thread_id: str, ID of the associated thread (optional)
        :param assigned_agent: str, agent assigned to the task (optional)
        :param files: List[str], list of files associated with the task (optional)
        :param tags: List[str], list of tags associated with the task (optional)
        :param state: States, state of the task (default: AVAILABLE)
        :raises ValueError: If priority is not a positive integer
        :raises TypeError: If files or tags are not lists
        """
        if not isinstance(priority, int) or priority < 0:
            raise ValueError("Priority must be a positive integer.")

        if files is not None and not isinstance(files, list):
            raise TypeError("Files must be a list.")

        if tags is not None and not isinstance(tags, list):
            raise TypeError("Tags must be a list.")

        self.description = description
        self.priority = priority
        self.thread_id = thread_id
        self.assigned_agent = assigned_agent
        self.files = files or []
        self.tags = tags or []
        self.state = state if isinstance(state, States) else States.AVAILABLE

    def format_for_ai(self) -> str:
        """
        Format the task information into a string suitable for an AI prompt.

        :return: str, formatted string for AI prompt
        """
        prompt_parts = [
            f"Task ID: {self.task_id}",
            f"Description: {self.description}",
            f"Priority: {self.priority}",
            f"State: {self.state}",
            f"Files: {', '.join(self.files) if self.files else 'None'}"
        ]

        return ' | '.join(prompt_parts)
