import threading
from typing import Callable, Dict, List, Tuple
from concurrent.futures import ThreadPoolExecutor

class MessageBus:
    """
    A message bus implementation for managing message passing between components.
    """

    def __init__(self, max_workers: int = 10):
        self.topics: Dict[str, List[Callable]] = {}
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
            try:
                self.executor.submit(subscriber, message)
            except Exception as e:
                print(f"Exception in subscriber '{subscriber.__name__}': {e}")

    def list_topics(self) -> List[Tuple[str, str]]:
        with self.lock:
            return [(topic, "") for topic in self.topics.keys()]
