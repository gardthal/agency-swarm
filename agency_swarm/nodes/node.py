import threading
import uuid
from typing import Callable, Any
from message_bus import MessageBus  # Ensure you have the MessageBus class defined as previously discussed

class Node:
    _instances = []
    _lock = threading.Lock()

    def __init__(self, message_bus: MessageBus):
        with Node._lock:
            self._running = False
            self._id = str(uuid.uuid4())
            self.message_bus = message_bus
            Node._instances.append(self)

    def start(self):
        self._running = True
        threading.Thread(target=self.run, daemon=True).start()

    def stop(self):
        self._running = False

    def subscribe(self, topic: str, callback: Callable[[Any], None]):
        """Subscribe to a topic with a callback function."""
        self.message_bus.subscribe(topic, callback)

    def unsubscribe(self, topic: str, callback: Callable[[Any], None]):
        """Unsubscribe from a topic."""
        self.message_bus.unsubscribe(topic, callback)

    def publish(self, topic: str, message: Any):
        """Publish a message to a topic."""
        self.message_bus.publish(topic, message)

    @classmethod
    def get_instances(cls):
        return cls._instances

    def run(self):
        """Override this method in subclasses to implement specific logic."""
        raise NotImplementedError("Subclasses must implement this method.")

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self._id}>"
