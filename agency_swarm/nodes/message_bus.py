import threading
from typing import Callable, Dict, List
from concurrent.futures import ThreadPoolExecutor

class MessageBus:
    def __init__(self, max_workers=10):
        self.topics: Dict[str, List[Callable]] = {}
        self.topic_info: Dict[str, Dict[str, str]] = {}  # Store topic descriptions and recommendations
        self.lock = threading.Lock()
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def subscribe(self, topic: str, subscriber: Callable):
        with self.lock:
            if topic not in self.topics:
                self.topics[topic] = []
            self.topics[topic].append(subscriber)

    def unsubscribe(self, topic: str, subscriber: Callable):
        with self.lock:
            if topic in self.topics:
                self.topics[topic].remove(subscriber)
                if not self.topics[topic]:
                    del self.topics[topic]

    def publish(self, topic: str, message: Dict):
        with self.lock:
            subscribers = self.topics.get(topic, [])
        for subscriber in subscribers:
            self.executor.submit(subscriber, message)

    def register_topic(self, topic_name, description, recommended_subscribers):
        """Register a topic with a description and recommendations for subscribers."""
        with self.lock:
            self.topic_info[topic_name] = {
                "description": description,
                "recommended_subscribers": recommended_subscribers
            }

    def get_topic_info(self, topic_name):
        """Get information about a topic, including its description and subscriber recommendations."""
        return self.topic_info.get(topic_name, None)

    def list_topics(self):
        """List all topics with their descriptions."""
        with self.lock:
            return [(topic, info["description"]) for topic, info in self.topic_info.items()]
