class PriorityQueue:
    """@brief Klasa reprezentująca kolejkę priorytetową."""

    def __init__(self):
        """@brief Inicjalizuje kolejkę priorytetową."""
        self.queue = []

    def put(self, item, f_score, g_score):
        """@brief Dodaje element do kolejki priorytetowej.
        @args:
        - item: Element do dodania.
        - f_score: Wartość funkcji f.
        - g_score: Wartość funkcji g
        """
        self.queue.append((item, f_score, g_score))

    def get(self):
        """@brief Pobiera element z kolejki priorytetowej.

        @returns: Element z kolejki priorytetowej.
        """
        self.queue.sort(key=lambda item: (item[1], item[2]))
        return self.queue.pop(0)[0]

    def empty(self):
        """@brief Sprawdza, czy kolejka priorytetowa jest pusta."""
        return len(self.queue) == 0
