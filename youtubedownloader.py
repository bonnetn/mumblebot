import pafy
import logging
import os

from api_key import YOUTUBE_API_KEY


class YoutubeDownloader:

    log = logging.getLogger("YoutubeDownloader")

    def __init__(self):
        pass

    def download(self, track):

        if track.beingDownloaded:
            self.log.warning("This video is already being downloaded.")
            # downloaded.wait()
            return

        track.beingDownloaded = True
        pafy.set_api_key(YOUTUBE_API_KEY)

        vid = track.vid
        path = "cache/video_" + vid.videoid

        if os.path.isfile(path):
            self.log.info("This video has already been downloaded...")
            track.path = path
            return

        self.log.info("Downloading the video to " + path)
        best = vid.getbestaudio()
        best.download(quiet=True, filepath=path)

        track.path = path
        track.downloaded.set()
        track.beingDownloaded = False
