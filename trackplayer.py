from youtubedownloader import YoutubeDownloader
from playingthread import PlayingThread


class TrackPlayer:

    def onFinishedPlaying(self):
        pass

    downloader = YoutubeDownloader()
    playingThread = PlayingThread()

    def __init__(self, mumble):
        self.mumble = mumble

        pt = self.playingThread
        pt.mumble = self.mumble
        pt.onFinishedPlaying = self.onFinishedPlaying
        pt.start()

    def stop(self):
        self.playingThread.stop()

    def play(self, track):
        try:
            self.downloader.download(track)
        except Exception:
            raise

        self.playingThread.play(track.path)
