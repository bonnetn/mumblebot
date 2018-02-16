import logging
import threading
import subprocess
import audioop
import time


class PlayingThread(threading.Thread):

    log = logging.getLogger("PlayingThread")
    lock = threading.Lock()
    eventPlaying = threading.Event()
    running = True

    def play(self, path):
        with self.lock:
            self.path = path

        self.eventPlaying.set()

    def stop(self):
        self.running = False

    def run(self):
        assert(self.mumble and self.onFinishedPlaying)

        while self.running:

            self.eventPlaying.wait()
            self.eventPlaying.clear()

            self.log.info("Started playing")
            with self.lock:
                command = ["ffmpeg", "-v", "quiet", '-nostdin', '-i',
                           self.path, '-ac', '1', '-f', 's16le', '-ar',
                           '48000', '-']
                t = subprocess.Popen(command, stdout=subprocess.PIPE,
                                     bufsize=480)
            while (t.poll() is None and
                   not self.eventPlaying.is_set() and self.running):

                while self.mumble.sound_output.get_buffer_size() > 0.5:
                    time.sleep(0.01)
                raw_music = t.stdout.read(480)
                if raw_music:
                    self.mumble.sound_output.add_sound(
                        audioop.mul(raw_music, 2, 0.1))
                else:
                    time.sleep(0.1)

            self.log.info("Stopped playing")
            self.onFinishedPlaying()
