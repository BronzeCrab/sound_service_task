# -*- coding: utf-8 -*-
from daemonize import Daemonize
import logging
import signal
from datetime import datetime

LOGGING_FOLDER = "/tmp/test.log"
PID = "/tmp/test.pid"
DIRECTORY = "/home/user/music"


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
fh = logging.FileHandler(LOGGING_FOLDER, "w")
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)
keep_fds = [fh.stream.fileno()]


def main():
    logger.debug("Test")
    while True:
        print('hello')

daemon = ExtendedDaemonize(
    app="test_app", pid=PID,
    action=main, keep_fds=keep_fds,
    foreground=True)
daemon.start()
