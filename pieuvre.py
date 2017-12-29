import pymumble.pymumble_py3 as pymumble
import signal
import logging
from htmlstripper import HTMLRemover
from trackplayer import TrackPlayer
from track import Track
from track import InvalidYoutubeURL
import queue

MURMUR_HOST = "localhost"
MURMUR_PASSWORD = "password"


class Pieuvre:

    log = logging.getLogger("PieuvreBot")
    mumble = None
    trackPlayer = None
    tracklist = queue.Queue()

    def __init__(self, server, user, port, password):

        self.mumble = pymumble.Mumble(server,
                                      user=user, port=port,
                                      password=password, debug=False)
        self.log.info("Created the mumble class")

        self.trackPlayer = TrackPlayer(self.mumble)

        self.mumble.callbacks.set_callback(
          pymumble.constants.PYMUMBLE_CLBK_CONNECTED,
          self._connected)

        self.mumble.callbacks.set_callback(
          pymumble.constants.PYMUMBLE_CLBK_TEXTMESSAGERECEIVED,
          self._msgReceived)
        self.mumble.set_codec_profile("audio")

        try:
            self.mumble.start()  # start the mumble thread
        except Exception:
            self.log.error("Could not start the mumble thread...")
            raise
        self.log.info("Started the mumble thread")

        print(self.mumble.is_ready())  # wait for the connection
        self.log.info("Mumble thread ready")

        self.mumble.set_bandwidth(200000)
        self.mumble.users.myself.comment("Hi I'm pieuvre")

    def stop(self):
        self.trackPlayer.stop()

    def wait(self):
        self.mumble.join()

    def _connected(self):
        self.log.info("Bot successfully connected !")

    def _parseCommand(self, line, sender):
        args = line.split(" ")
        cmd = args[0].lower()

        if cmd == "add" or cmd == "a":
            if len(args) != 2:
                sender.send_message("Invalid number of arguments.")
                return
            url = args[1]
            try:
                track = Track(sender, url)
            except InvalidYoutubeURL:
                sender.send_message("Invalid youtube link.")
                return

            self.tracklist.put(track)
            self.log.info(sender["name"] + " added "
                          + url + " to the tracklist.")
            sender.send_message("You added " + track.vid.title
                                + " to the tracklist.")
        else:
            sender.send_message("Invalid command.")

    def _msgReceived(self, msg):

        sender = self.mumble.users[msg.actor]
        senderName = sender['name']

        r = HTMLRemover()
        r.feed(msg.message)
        messageTxt = r.getMessage()

        self.log.debug("[MSG] " + senderName + ": " + messageTxt)
        self._parseCommand(messageTxt, sender)


class BotHandler:
    def __init__(self):
        self.log = logging.getLogger("BotHandler")
        self.running = True
        signal.signal(signal.SIGINT, self.killBot)

        self.bots = []

    def addPieuvreBot(self, server, user="PYeuvre", port=64738, password=""):
        try:
            self.bots += [Pieuvre(server, user, port, password)]
        except Exception:
            self.log.error("Could not create Pieuvre bot")
            raise
        self.log.info("Created a PieuvreBot...")

    def run(self):
        for bot in self.bots:
            bot.wait()
        self.log.info("Bot handler ended...")

    def killBot(self, a, b):
        for bot in self.bots:
            bot.stop()
        self.log.warning("Killing the bot...")
        quit()


if __name__ == '__main__':

    logging.basicConfig(
        format='%(asctime)s %(name)s %(levelname)s: %(message)s',
        level=logging.INFO)

    b = BotHandler()
    b.addPieuvreBot(MURMUR_HOST, "Pieuvre", 64738, MURMUR_PASSWORD)
    b.run()
