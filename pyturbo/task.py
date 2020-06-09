import time
from collections import namedtuple


class Task(object):
    '''
    Base task
    '''

    def __init__(self):
        self.create_time = time.time()

    def start(self):
        self.start_time = time.time()

    def finish(self):
        self.finish_time = time.time()

    def __repr__(self, info=None):
        if info is None:
            return self.__class__.__name__
        return '%s(%s)' % (self.__class__.__name__, info)


class ControlTask(Task):
    '''
    Pipeline control task
    '''

    def __init__(self, command, *, parent_task=None):
        super(ControlTask, self).__init__()
        self.command = command
        self.parent = parent_task

    def __repr__(self):
        return super(ControlTask, self).__repr__(self.command)


TaskLog = namedtuple('TaskLog', [
    'processor', 'duration', 'start_time', 'end_time'])


class RegularTask(Task):
    '''
    Regular excutable task
    '''

    def __init__(self, content, meta=None, *, parent_task=None):
        super(RegularTask, self).__init__()
        self.content = content
        self.build_meta(meta, parent_task)
        self.logs = parent_task.logs.copy() if parent_task is not None else []

    def build_meta(self, meta, parent_task):
        self.meta = {}
        if parent_task is not None:
            self.meta.update(parent_task.meta)
        if meta is not None:
            self.meta.update(meta)

    def start(self, processor):
        super(RegularTask, self).start()
        self.processor = repr(processor)

    def finish(self):
        super(RegularTask, self).finish()
        duration = self.finish_time - self.start_time
        log = TaskLog(
            self.processor, duration, self.start_time, self.finish_time)
        self.logs.append(log)

    def __repr__(self):
        return super(RegularTask, self).__repr__(repr(self.meta))
