from sqlalchemy import create_engine, or_
from sqlalchemy.orm import scoped_session, sessionmaker, joinedload, make_transient
from task import Task, Base, States

class TaskLibrary:
    """
    A class for managing a library of tasks using an SQLAlchemy database.
    """

    def __init__(self, db_url='sqlite:///task_library.db'):
        """
        Initialize a new TaskLibrary instance.

        :param db_url: String, the database URL for SQLAlchemy to connect to.
        """
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(self.session_factory)

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

                
    def add_task(self, task):
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

        :param filters: Dictionary, criteria for filtering tasks. Each key is an attribute name,
                        and the value can be a single value or a list of values. If a list is
                        provided, tasks matching any of the values in the list will be included.
        :param order_by: String/List, attribute(s) to order the tasks by.
        :param limit: Integer, limit the number of tasks returned.
        :return: List of Task instances that match the query.
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

    def next_task(self):
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
