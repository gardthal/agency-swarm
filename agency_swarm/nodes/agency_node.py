from .node import Node
from agency_swarm.tasks import TaskLibrary, Task, States
from agency_swarm.agency import Agency
from agency_swarm.tools.tasktools import ChangeTaskState
import time

class AgencyNode(Node):
    """
    A class representing an agency node, inheriting from the base Node class.
    This class is responsible for managing tasks and executing them within an agency context.
    """

    def __init__(self, agency: Agency, custom_tools=None):
        """
        Initialize a new AgencyNode instance.

        :param agency: Agency, the agency associated with this node.
        :param custom_tools: List, optional custom tools to be added to the agency's CEO.
        """
        self.agency = agency
        self.task_library = TaskLibrary(db_url='sqlite:///task_library.db')
        self.agency.ceo.add_tool(ChangeTaskState)

        if custom_tools is not None:
            self._add_custom_tools_to_ceo(custom_tools)

    def _run(self):
        """
        Main loop where the AgencyNode checks for new tasks and executes them.
        """
        while self._running:
            next_task = self.task_library.next_task()
            if next_task:
                self._execute_task(next_task)
            else:
                time.sleep(1)

    def _execute_task(self, task: Task):
        """
        Execute the given task and update its state in the task library.

        :param task: Task, the task to be executed.
        """
        # Example task execution logic
        print(f"Executing task {task.task_id}")
        task.state = States.IN_PROGRESS
        self.task_library.add_task(task)

        # Complete Task
        print(self.agency.get_completion(task.format_for_ai()))

        # Check Task State
        if task.state == States.IN_PROGRESS:
            print("Failed to change state")

            if task.state == States.IN_PROGRESS:
                task.state = States.ERROR
                self.task_library.add_task(task)

    def _add_custom_tools_to_ceo(self, custom_tools):
        """
        Add custom tools to the agency's CEO.

        :param custom_tools: List, custom tools to be added.
        """
        for tool in custom_tools:
            self.agency.ceo.add_tool(tool)

    def __repr__(self):
        """
        Return a string representation of the AgencyNode instance.

        :return: String representation.
        """
        return f"<AgencyNode id={self._id}>"