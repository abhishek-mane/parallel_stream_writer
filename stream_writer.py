
import sys
from threading import Lock


class ParallelStreamWriter():

    lock = Lock()

    def __init__(self, task_type):
        self.stream = sys.stdout
        self.task_type = task_type
        self.tasks = []
        self.width = 0

    def add_task(self, task_name):
        task = self.task_type + ' ' + task_name  # Downloading FILENAME
        self.tasks.append(task)
        if self.width < len(task):
            self.width = len(task)

    def init_task(self, task_name, initial_status=''):
        msg = "{:<{width}} ... {}\r\n".format(self.task_type + ' ' + task_name, initial_status, width=self.width)
        self.stream.write(msg)
        self.stream.flush()

    def update_status(self, task_name, status):
        self.lock.acquire()

        task = self.task_type + ' ' + task_name

        # identify line number to be updated
        index = self.tasks.index(task)
        diff = len(self.tasks) - index

        # jump to the indexth line
        self.stream.write("%c[%dA" % (27, diff))

        # erase this line
        self.stream.write("%c[2K\r" % 27)

        # write line with new status
        msg = "{:<{width}} ... {}\r".format(self.task_type + ' ' + task_name, status, width=self.width)
        self.stream.write(msg)
        self.stream.flush()

        # reset the pointer
        self.stream.write("%c[%dB" % (27, diff))

        self.lock.release()
