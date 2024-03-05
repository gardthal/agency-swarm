import threading
import uuid
from typing import Callable, Any, List, Tuple
from .message_bus import MessageBus

class Node:
    """
    A base class representing a node in a messaging system.
    """

    # Class variables
    _instances = []
    _lock = threading.Lock()
    _message_bus = MessageBus()

    # Class methods for creating and removing topics
    @classmethod
    def create_topic(cls, topic: str, description: str):
        """
        Create a new topic with the given name and description.
        """
        cls._message_bus.create_topic(topic, description)

    @classmethod
    def remove_topic(cls, topic: str):
        """
        Remove the specified topic.
        """
        cls._message_bus.remove_topic(topic)

    # Constructor
    def __init__(self):
        """
        Initialize a new Node instance.
        """
        with Node._lock:
            self._running = False
            self._id = str(uuid.uuid4())
            self._subscribed_topics = set()
            Node._instances.append(self)

    # Start and stop methods
    def start(self):
        """
        Start the node.
        """
        self._running = True
        threading.Thread(target=self._run, daemon=True).start()

    def stop(self):
        """
        Stop the node.
        """
        self._running = False

    # Subscription methods
    def subscribe(self, topic: str, callback: Callable[[Any], None]):
        """
        Subscribe to a topic with a callback function.
        """
        Node._message_bus.subscribe(topic, callback)
        self._subscribed_topics.add(topic)

    def unsubscribe(self, topic: str, callback: Callable[[Any], None]):
        """
        Unsubscribe from a topic.
        """
        Node._message_bus.unsubscribe(topic, callback)
        self._subscribed_topics.discard(topic)

    # Publish method
    def publish(self, topic: str, message: Any):
        """
        Publish a message to a topic.
        """
        Node._message_bus.publish(topic, message)

    # Class methods for getting instances and topics
    @classmethod
    def get_instances(cls) -> List[Tuple[str, str, bool, List[str]]]:
        """
        Get information about all instances of the Node class.
        """
        instances_info = []
        for instance in cls._instances:
            name = cls._get_node_name(instance)
            node_type = cls._get_node_type(instance)
            running = instance._running
            subscribed_topics = list(instance._subscribed_topics)
            instances_info.append((name, node_type, running, subscribed_topics))
        return instances_info

    @classmethod
    def get_topics(cls):
        """
        Get the list of available topics.
        """
        return cls._message_bus.list_topics()

    # Internal methods
    @staticmethod
    def _get_node_name(instance) -> str:
        """
        Get the name of the node.
        """
        current_cls = instance.__class__
        return f'{current_cls.__name__}'

    @staticmethod
    def _get_node_type(instance) -> str:
        """
        Get the type of the node.
        """
        current_cls = instance.__class__
        return current_cls.__bases__[0].__name__

    # Main loop method
    def _run(self):
        """
        Main loop for the node's execution.
        """
        while self._running:  # Check if running flag is set
            try:
                self.run()
            except Exception as e:
                print(f"Exception in node {self._id}: {e}")
                # Optionally handle the exception here

    # Method to be implemented by subclasses
    def run(self):
        """
        Subclasses must override this method to define their specific behavior.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    # Representation method
    def __repr__(self):
        """
        String representation of the Node instance.
        """
        return f"<{self.__class__.__name__} id={self._id}>"
