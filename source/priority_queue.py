class PriorityQueue:
    def __init__(self):
        self.queue = []

    def put(self, item, priority):
        self.queue.append((priority, item))
        self.queue.sort(key=lambda item: item[1])

    def get(self):
        return self.queue.pop(0)[0]

    def empty(self):
        return len(self.queue) == 0
