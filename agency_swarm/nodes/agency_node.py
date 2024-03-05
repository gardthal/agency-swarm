from agency_swarm.nodes.node import Node
from agency_swarm.tasks import TaskLibrary, Task, States
from agency_swarm.agency import Agency
from agency_swarm.tools.tasktools import ChangeTaskState
import time
import os
import inspect
import threading
import concurrent.futures

class AgencyNode(Node):
    """
    A class representing an agency node, inheriting from the base Node class.
    This class is responsible for managing tasks and executing them within an agency context.
    """

    def __init__(self, agency: Agency, **kwargs):
        """
        Initialize a new AgencyNode instance.

        :param agency: Agency, the agency associated with this node.
        """
        self.agency = agency
        super().__init__(**kwargs)

        # Get the directory of the calling script 
        calling_frame = inspect.stack()[1]
        calling_module = inspect.getmodule(calling_frame[0])
        calling_script_dir = os.path.dirname(calling_module.__file__)

        # Construct the path for the database file
        db_path = os.path.join(calling_script_dir, 'task_library.db')

        # Initialize the task library
        self.task_library = TaskLibrary(db_url=f'sqlite:///{db_path}')
        
        #Add ceo tools for tasks and task library
        self.agency.ceo.add_tool(ChangeTaskState)

        #Create new topic
        curr_instance = self.__class__.__name__
        self.create_topic(curr_instance, f"Publish requests to add tasks to {curr_instance} task library")

        self.subscribe(f"{curr_instance}", self.add_task)

    def add_task(self, message):
        pass

    #REEVALUATE!
    def run(self, num_workers=5):
        """
        Main loop where the AgencyNode checks for new tasks and executes them.
        
        :param num_workers: int, number of worker threads to use.
        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
            while self._running:
                # Retrieve multiple tasks if available
                next_tasks = self.task_library.next_tasks()

                # Check if there are tasks to execute
                if next_tasks:
                    # Submit tasks to the thread pool
                    future_to_task = {executor.submit(self._execute_task, task): task for task in next_tasks}
                    
                    # Wait for all tasks to complete
                    for future in concurrent.futures.as_completed(future_to_task):
                        task = future_to_task[future]
                        try:
                            future.result()  # Retrieve the result to check for any exceptions
                        except Exception as e:
                            print(f"Task execution failed: {e}")

                else:
                    time.sleep(10)

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

    def __repr__(self):
        """
        Return a string representation of the AgencyNode instance.

        :return: String representation.
        """
        return f"<AgencyNode id={self._id}>"