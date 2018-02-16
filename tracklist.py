import queue


class Tracklist:
    def __init__(self):
        self.q = queue.Queue()

    def addTrack(self, track):
        self.q.put(track)
