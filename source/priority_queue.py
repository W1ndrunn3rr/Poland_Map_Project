class PriorityQueue:
    def __init__(self):
        self.queue = []

    def put(self, item, f_score, g_score):
        self.queue.append((item, f_score, g_score))

    def get(self):
        self.queue.sort(key=lambda item: (item[1], item[2]))

        if len(self.queue) > 1 and abs(self.queue[0][1] - self.queue[1][1]) < 1:
            if self.queue[0][2] < self.queue[1][2]:
                return self.queue.pop(0)[0]
            else:
                return self.queue.pop(1)[0]
        else:
            return self.queue.pop(0)[0]

    def empty(self):
        return len(self.queue) == 0
