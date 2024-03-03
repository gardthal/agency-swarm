import threading
import uuid
from typing import Callable, Any, List, Tuple
from message_bus import MessageBus

class Node:
    """
    A base class representing a node in a messaging system.
    """

    _instances = []
    _lock = threading.Lock()
    _message_bus = MessageBus()

    def __init__(self):
        with Node._lock:
            self._running = False
            self._id = str(uuid.uuid4())
            self._subscribed_topics = set()
            Node._instances.append(self)

    def start(self):
        self._running = True
        threading.Thread(target=self._run, daemon=True).start()

    def stop(self):
        self._running = False

    def subscribe(self, topic: str, callback: Callable[[Any], None]):
        Node._message_bus.subscribe(topic, callback)
        self._subscribed_topics.add(topic)

    def unsubscribe(self, topic: str, callback: Callable[[Any], None]):
        Node._message_bus.unsubscribe(topic, callback)
        self._subscribed_topics.discard(topic)

    def publish(self, topic: str, message: Any):
        Node._message_bus.publish(topic, message)

    @classmethod
    def get_instances(cls) -> List[Tuple[str, str, bool, List[str]]]:
        instances_info = []
        for instance in cls._instances:
            name = cls._get_node_name(instance)
            node_type = cls._get_node_type(instance)
            running = instance._running
            subscribed_topics = list(instance._subscribed_topics)
            instances_info.append((name, node_type, running, subscribed_topics))
        return instances_info

    @staticmethod
    def _get_node_name(instance) -> str:
        current_cls = instance.__class__
        return f'{current_cls.__name__}'

    @staticmethod
    def _get_node_type(instance) -> str:
        current_cls = instance.__class__
        return current_cls.__bases__[0].__name__

    @classmethod
    def get_topics(cls):
        topics = cls._message_bus.list_topics()
        return [(topic, "") for topic in topics]

    def _run(self):
        """
        Subclasses must override this method to define their specific behavior.
        """
        while self._running:  # Check if running flag is set
            try:
                self.run()
            except Exception as e:
                print(f"Exception in node {self._id}: {e}")
                # Optionally handle the exception here

    def run(self):
        """
        Subclasses must override this method to define their specific behavior.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self._id}>"
