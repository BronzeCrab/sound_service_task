# -*- coding: utf-8 -*-
from daemonize import Daemonize
import logging
import signal
from datetime import datetime
import os
from pydub import AudioSegment
import sys

LOGGING_FILE = "/tmp/test.log"
PID = "/tmp/test.pid"
DIRECTORY = "/home/user/music"
OUTPUT_DIR = os.path.join(DIRECTORY, 'mp3')
EXTENSION = 'wav'


class ExtendedDaemonize(Daemonize):
    """New class to add signal catching to daemon"""
    def __init__(self, app, pid, action, keep_fds=None, foreground=False):
            Daemonize.__init__(
                self, app, pid, action,
                keep_fds=keep_fds,
                foreground=foreground)
            signal.signal(signal.SIGINT, self.sigterm)
            signal.signal(signal.SIGTERM, self.sigterm)

    def sigterm(self, signum, frame):
        now = datetime.now().strftime('%Y.%m.%d %H:%M')
        if signum == 15:
            logger.debug("{} - SIGTERM, завершение работы".format(now))
        if signum == 2:
            logger.debug("{} - SIGINT, завершение работы".format(now))
        Daemonize.sigterm(self, signum, frame)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False
fh = logging.FileHandler(LOGGING_FILE, "w")
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)
keep_fds = [fh.stream.fileno()]


def main():
    converted_files = []
    if not os.path.exists(OUTPUT_DIR):
        try:
            os.makedirs(OUTPUT_DIR)
        except Exception as e:
            now = datetime.now().strftime('%Y.%m.%d %H:%M')
            logger.error(
                "{} Ошибка при создании директории, текст: {}".format(now, e)
            )
            sys.exit(1)
    while True:
        files = [f for f in os.listdir(DIRECTORY) if os.path.isfile(
            os.path.join(DIRECTORY, f))]
        for f in files:
            if f.split('.')[1] == EXTENSION and f not in converted_files:
                new_name = f.split('.')[0] + '.mp3'
                now = datetime.now().strftime('%Y.%m.%d %H:%M')
                try:
                    AudioSegment.from_wav(os.path.join(DIRECTORY, f)).export(
                        os.path.join(OUTPUT_DIR, new_name), format="mp3")
                    converted_files.append(f)
                    logger.debug(
                        "{} Успешно переконвертировали файл {} ".format(now, f)
                    )
                except Exception as e:
                    logger.error(
                        "{} Ошибка при конвертации файла {}, текст: {}".
                        format(now, f, e)
                    )
                    sys.exit(1)

daemon = ExtendedDaemonize(
    app="test_app", pid=PID,
    action=main, keep_fds=keep_fds,
    foreground=True)
daemon.start()
