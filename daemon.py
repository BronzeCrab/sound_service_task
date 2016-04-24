from time import sleep
from daemonize import Daemonize

pid = "/tmp/test.pid"
directory = "/home/user/music"


def main():
    while True:
        sleep(5)

daemon = Daemonize(app="test_app", pid=pid, action=main)
daemon.start()
