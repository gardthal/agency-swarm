from sqlalchemy import create_engine, or_
from sqlalchemy.orm import scoped_session, sessionmaker, joinedload, make_transient
from .task import Task, States, Base
import threading

class TaskLibrary:
    """
    A class for managing a library of tasks using an SQLAlchemy database.
    """

    # Define a thread-local storage for TaskLibrary instances
    _local = threading.local()

    def __init__(self, db_url='sqlite:///task_library.db'):
        """
        Initialize a new TaskLibrary instance.

        :param db_url: str, the database URL for SQLAlchemy to connect to.
        """
        # Check if a TaskLibrary instance already exists for this thread
        if not hasattr(TaskLibrary._local, 'library'):
            # If not, create a new one and store it in thread-local storage
            TaskLibrary._local.library = self

            # Initialize database connection
            self.engine = create_engine(db_url)
            Base.metadata.create_all(self.engine)
            self.session_factory = sessionmaker(bind=self.engine)
            self.Session = scoped_session(self.session_factory)
        else:
            print("task library already created for this thread")

    @classmethod
    def get_current(cls):
        """
        Get the TaskLibrary instance associated with the current thread.

        :return: TaskLibrary instance or None if not found.
        """
        return getattr(TaskLibrary._local, 'library', None)
    
    def print_library(self):
        """
        Print all tasks in the library with their attributes in a readable format.
        """
        with self.Session() as session:
            tasks = session.query(Task).all()
            if not tasks:
                print("Task library is empty.")
                return

            for task in tasks:
                print("\nTask Details:")
                print(f"  Task ID: {task.task_id}")
                print(f"  Description: {task.description}")
                print(f"  Priority: {task.priority}")
                print(f"  State: {task.state.name}")
                print(f"  Assigned Agent: {task.assigned_agent or 'None'}")
                print(f"  Files: {', '.join(task.files) if task.files else 'None'}")
                print(f"  Tags: {', '.join(task.tags) if task.tags else 'None'}")
                print(f"  Thread ID: {task.thread_id or 'None'}")

    def add_task(self, task: Task):
        """
        Add a new task to the library or update an existing one.

        :param task: Task, the task instance to be added or updated.
        """
        with self.Session() as session:
            # Merge the task with the session
            task = session.merge(task)

            # Commit the changes to the database
            session.commit()

    def query_tasks(self, filters=None, order_by=None, limit=None):
        """
        Query tasks from the library based on provided filters, order, and limit.

        :param filters: dict, criteria for filtering tasks.
        :param order_by: str/list, attribute(s) to order the tasks by.
        :param limit: int, limit the number of tasks returned.
        :return: list of Task instances that match the query.
        """
        with self.Session() as session:
            query = session.query(Task).options(joinedload('*'))

            if filters:
                filter_conditions = []
                for key, value in filters.items():
                    if key == 'state' and isinstance(value, list):
                        # Special handling for state filters with a list of states
                        state_conditions = [getattr(Task, key) == state for state in value]
                        filter_conditions.append(or_(*state_conditions))
                    elif isinstance(value, list):
                        filter_conditions.append(getattr(Task, key).in_(value))
                    else:
                        filter_conditions.append(getattr(Task, key) == value)

                query = query.filter(*filter_conditions)

            if order_by:
                if isinstance(order_by, list):
                    query = query.order_by(*[getattr(Task, field) for field in order_by])
                else:
                    query = query.order_by(getattr(Task, order_by))

            if limit:
                query = query.limit(limit)

            return query.all()

    def next_task(self) -> Task:
        """
        Retrieve the next available task from the task library.

        :return: Task instance or None if no task is available.
        """
        with self.Session() as session:
            task = session.query(Task) \
                          .filter(Task.state.in_([States.AVAILABLE])) \
                          .order_by(Task.priority) \
                          .first()

            if task:
                # Detach the task object from the session
                make_transient(task)
                return task

        return None

    def delete_task(self, task: Task):
        """
        Delete a task from the library.

        :param task: Task, the task instance to be deleted.
        """
        with self.Session() as session:
            # Query for the task in the database by its ID
            task_to_delete = session.query(Task).filter_by(task_id=task.task_id).first()

            # If the task is found, delete it
            if task_to_delete:
                session.delete(task_to_delete)
                session.commit()
                print(f"Task ID {task.task_id} deleted.")
            else:
                print(f"Task ID {task.task_id} not found in the library.")