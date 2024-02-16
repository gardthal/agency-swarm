from node import Node
from tasks import TaskLibrary, Task, States
from agency import Agency
import time

class AgencyNode(Node):
    def __init__(self, agency: Agency, custom_tools=None):
        self.agency = agency
        self.task_library = TaskLibrary()

        if custom_tools is not None:
            self.add_custom_tools_to_ceo(custom_tools)

        # Subscribe to topics of interest here
        self.subscribe("task_updates", self.handle_task_update)

    def run(self):
        """
        Main loop where the AgencyNode checks for new tasks and executes them.
        """
        while self._running:
            next_task = self.task_library.next_task()
            if next_task:
                self.execute_task(next_task)
        else:
            time.sleep(1)

    def handle_task_update(self, message):
        """
        Handle messages received on the 'task_updates' topic.
        This method will be called whenever a message is published to 'task_updates'.
        """
        print(f"AgencyNode {self._id} received a task update: {message}")
        # Process the task update message here
        # Example: Update task status in the task library or initiate a new task

    def execute_task(self, task: Task):
        """
        Execute the given task and update its state in the task library.
        """
        # Example task execution logic
        print(f"Executing task {task.task_id}")
        task.state = States.IN_PROGRESS
        self.task_library.add_task(task)

        # Complete Task
        self.agency.get_completion(task.format_for_ai())

        #Check Task State
        if task.state == States.IN_PROGRESS:
            self.agency.get_completion("Please change the state of the task based on your execution success")

            if task.state == States.IN_PROGRESS:
                task.state = States.ERROR

    def add_custom_tools_to_ceo(self, custom_tools):
        """
        Add custom tools to the agency's CEO.
        """
        for tool in custom_tools:
            self.agency.ceo.add_tool(tool)

    def __repr__(self):
        return f"<AgencyNode id={self._id}>"
