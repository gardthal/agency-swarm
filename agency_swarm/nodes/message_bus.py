import threading
from typing import Callable, Dict, List, Tuple
from concurrent.futures import ThreadPoolExecutor

class MessageBus:
    """
    A message bus implementation for managing message passing between components.
    """

    def __init__(self, max_workers: int = 10):
        """
        Initialize a new MessageBus instance.

        :param max_workers: int, the maximum number of worker threads for message processing.
        """
        self.topics: Dict[str, List[Callable]] = {}  # Dictionary to store subscribers for each topic
        self.topic_info: Dict[str, Dict[str, str]] = {}  # Dictionary to store topic descriptions and recommendations
        self.lock = threading.Lock()  # Lock for thread safety
        self.executor = ThreadPoolExecutor(max_workers=max_workers)  # ThreadPoolExecutor for concurrent message processing

    def subscribe(self, topic: str, subscriber: Callable):
        """
        Subscribe a callable function to a topic.

        :param topic: str, the topic to subscribe to.
        :param subscriber: Callable, the function to be subscribed to the topic.
        """
        with self.lock:
            if topic not in self.topics:
                self.topics[topic] = []
            self.topics[topic].append(subscriber)

    def unsubscribe(self, topic: str, subscriber: Callable):
        """
        Unsubscribe a callable function from a topic.

        :param topic: str, the topic to unsubscribe from.
        :param subscriber: Callable, the function to be unsubscribed from the topic.
        """
        with self.lock:
            if topic in self.topics:
                self.topics[topic].remove(subscriber)
                if not self.topics[topic]:
                    del self.topics[topic]

    def publish(self, topic: str, message: Dict):
        """
        Publish a message to a topic.

        :param topic: str, the topic to publish the message to.
        :param message: Dict, the message to be published.
        """
        with self.lock:
            subscribers = self.topics.get(topic, [])
        for subscriber in subscribers:
            self.executor.submit(subscriber, message)

    def register_topic(self, topic_name: str, description: str, recommended_subscribers: List[str]):
        """
        Register a topic with a description and recommendations for subscribers.

        :param topic_name: str, the name of the topic to be registered.
        :param description: str, the description of the topic.
        :param recommended_subscribers: List[str], a list of recommended subscribers for the topic.
        """
        with self.lock:
            self.topic_info[topic_name] = {
                "description": description,
                "recommended_subscribers": recommended_subscribers
            }

    def get_topic_info(self, topic_name: str) -> Dict[str, str]:
        """
        Get information about a topic, including its description and subscriber recommendations.

        :param topic_name: str, the name of the topic to retrieve information for.
        :return: Dict[str, str], information about the topic.
        """
        return self.topic_info.get(topic_name, {})

    def list_topics(self) -> List[Tuple[str, str]]:
        """
        List all topics with their descriptions.

        :return: List[Tuple[str, str]], a list of tuples containing topic names and descriptions.
        """
        with self.lock:
            return [(topic, info["description"]) for topic, info in self.topic_info.items()]
