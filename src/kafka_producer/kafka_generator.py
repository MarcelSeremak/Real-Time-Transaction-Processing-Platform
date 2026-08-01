class KafkaGenerator:

    def __init__(self, bootstrap_server, topic):
        self.bootstrap_server = bootstrap_server
        self.topic = topic

    def send(self, message):
        pass