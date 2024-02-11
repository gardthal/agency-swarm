# agency_node.py
from node import Node
from task_library import TaskLibrary, Task, States
from agency import Agency

class AgencyNode(Node):
    def __init__(self, message_bus, agency: Agency, task_library: TaskLibrary, custom_tools=None):
        super().__init__(message_bus)  # Pass the message_bus to the superclass
        self.agency = agency
        self.task_library = task_library

        if custom_tools is not None:
            self.add_custom_tools_to_ceo(custom_tools)

        # Subscribe to topics of interest here
        self.subscribe("task_updates", self.handle_task_update)

    def handle_task_update(self, message):
        """
        Handle messages received on the 'task_updates' topic.
        This method will be called whenever a message is published to 'task_updates'.
        """
        print(f"AgencyNode {self._id} received a task update: {message}")
        # Process the task update message here
        # Example: Update task status in the task library or initiate a new task

    def notify_task_completion(self, task_id):
        """
        Notify others that a task has been completed by publishing a message to the 'task_completion' topic.
        """
        completion_message = {"task_id": task_id, "status": "completed"}
        self.publish("task_completion", completion_message)
        print(f"AgencyNode {self._id} published task completion for task_id {task_id}")

    def get_next_task(self) -> Task:
        """
        Retrieve the next available task from the task library.
        """
        # Example logic to select the next task based on your criteria
        tasks = self.task_library.get_tasks(state=States.AVAILABLE)
        return tasks[0] if tasks else None

    def execute_task(self, task: Task):
        """
        Execute the given task and update its state in the task library.
        """
        # Example task execution logic
        print(f"Executing task {task.task_id}")
        task.state = States.IN_PROGRESS
        self.task_library.update_task(task)
        # Simulate task completion
        task.state = States.COMPLETE
        self.task_library.update_task(task)
        # Notify others about task completion
        self.notify_task_completion(task.task_id)

    def add_custom_tools_to_ceo(self, custom_tools):
        """
        Add custom tools to the agency's CEO.
        """
        for tool in custom_tools:
            self.agency.ceo.add_tool(tool)

    def run(self):
        """
        Main loop where the AgencyNode checks for new tasks and executes them.
        """
        while self._running:
            next_task = self.get_next_task()
            if next_task:
                self.execute_task(next_task)
            # Wait a bit before checking for the next task
            self.message_bus.executor.submit(self.wait_a_bit)

    @staticmethod
    def wait_a_bit():
        import time
        time.sleep(1)

    def __repr__(self):
        return f"<AgencyNode id={self._id}>"
