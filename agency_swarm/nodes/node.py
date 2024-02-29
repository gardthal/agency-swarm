import threading
import uuid
from typing import Callable, Any
from .message_bus import MessageBus  # Ensure you have the MessageBus class defined as previously discussed

class Node:
    """
    A base class representing a node in a messaging system.
    """

    _instances = []  # List to keep track of all instances of Node
    _lock = threading.Lock()  # Lock for thread safety
    _message_bus = MessageBus()  # Define a class-level message bus

    def __init__(self):
        """
        Initialize a new Node instance.
        """
        with Node._lock:
            self._running = False  # Flag to track the running state of the node
            self._id = str(uuid.uuid4())  # Unique identifier for the node
            Node._instances.append(self)  # Add the instance to the list of instances

    def start(self):
        """
        Start the node.
        """
        self._running = True  # Set running flag to True
        threading.Thread(target=self._run, daemon=True).start()  # Start a new thread to run the node's logic

    def stop(self):
        """
        Stop the node.
        """
        self._running = False  # Set running flag to False

    def subscribe(self, topic: str, callback: Callable[[Any], None]):
        """
        Subscribe to a topic with a callback function.

        :param topic: str, the topic to subscribe to.
        :param callback: Callable[[Any], None], the callback function to be invoked when a message is received.
        """
        Node._message_bus.subscribe(topic, callback)

    def unsubscribe(self, topic: str, callback: Callable[[Any], None]):
        """
        Unsubscribe from a topic.

        :param topic: str, the topic to unsubscribe from.
        :param callback: Callable[[Any], None], the callback function to be removed from the topic.
        """
        Node._message_bus.unsubscribe(topic, callback)

    def publish(self, topic: str, message: Any):
        """
        Publish a message to a topic.

        :param topic: str, the topic to publish the message to.
        :param message: Any, the message to be published.
        """
        Node._message_bus.publish(topic, message)

    @classmethod
    def get_instances(cls):
        """
        Get all instances of the Node class.

        :return: List, all instances of the Node class.
        """
        return cls._instances

    def _run(self):
        """
        Main execution logic of the node.
        This method should be overridden by subclasses to implement specific logic.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def __repr__(self):
        """
        Return a string representation of the Node instance.

        :return: str, string representation of the Node instance.
        """
        return f"<{self.__class__.__name__} id={self._id}>"
