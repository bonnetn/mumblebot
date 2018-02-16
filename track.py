import threading
import pafy

from api_key import YOUTUBE_API_KEY


class InvalidYoutubeURL(Exception):
    pass


class Track:
    url = ""
    user = 0
    downloaded = threading.Event()
    beingDownloaded = False
    vid = None

    def __init__(self, user, url):
        self.url = url
        self.user = user

        try:
            pafy.set_api_key(YOUTUBE_API_KEY)
            self.vid = pafy.new(url)

        except Exception:
            raise InvalidYoutubeURL("The URL could not be opened.")
