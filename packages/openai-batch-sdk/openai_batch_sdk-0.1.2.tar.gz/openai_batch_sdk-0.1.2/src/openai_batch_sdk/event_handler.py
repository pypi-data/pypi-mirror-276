class EventHandler:
    def __init__(self):
        self.events = {}

    def register_event(self, event_name, callback):
        if event_name not in self.events:
            self.events[event_name] = []
        self.events[event_name].append(callback)

    def trigger_event(self, event_name, data):
        if event_name in self.events:
            for callback in self.events[event_name]:
                callback(data)
