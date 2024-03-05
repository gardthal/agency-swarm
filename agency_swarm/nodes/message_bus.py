import threading
from typing import Callable, Dict, List, Tuple
from concurrent.futures import ThreadPoolExecutor

class MessageBus:
    """
    A message bus implementation for managing message passing between components.
    """

    def __init__(self, max_workers: int = 10):
        self.topics: Dict[str, Tuple[str, List[Callable]]] = {}
        self.lock = threading.Lock()
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def subscribe(self, topic: str, subscriber: Callable):
        with self.lock:
            if topic not in self.topics:
                raise ValueError(f"Topic '{topic}' does not exist. Please create the topic first.")
            self.topics[topic][1].append(subscriber)

    def unsubscribe(self, topic: str, subscriber: Callable):
        with self.lock:
            if topic in self.topics:
                self.topics[topic][1].remove(subscriber)
                if not self.topics[topic][1]:
                    del self.topics[topic]

    def publish(self, topic: str, message: Dict):
        with self.lock:
            topic_info = self.topics.get(topic)
            if topic_info:
                subscribers = topic_info[1]
            else:
                subscribers = []
        for subscriber in subscribers:
            try:
                self.executor.submit(subscriber, message)
            except Exception as e:
                print(f"Exception in subscriber '{subscriber.__name__}': {e}")

    def create_topic(self, topic: str, description: str):
        with self.lock:
            if topic in self.topics:
                raise ValueError(f"Topic '{topic}' already exists.")
            self.topics[topic] = (description, [])

    def remove_topic(self, topic: str):
        with self.lock:
            if topic in self.topics:
                del self.topics[topic]

    def list_topics(self) -> List[Tuple[str, str]]:
        with self.lock:
            return [(topic, info[0]) for topic, info in self.topics.items()]
