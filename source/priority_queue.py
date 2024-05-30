class PriorityQueue:
    def __init__(self):
        self.queue = []

    def put(self, item, priority):
        self.queue.append((priority, item))

    def get(self):
        self.queue.sort(key=lambda item: item[1])
        return self.queue.pop(0)[0]

    def empty(self):
        return len(self.queue) == 0

    def check_in(self, item):
        return item in self.queue
