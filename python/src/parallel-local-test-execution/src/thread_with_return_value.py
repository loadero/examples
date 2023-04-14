from threading import Thread

class ThreadWithReturnValue(Thread):
    """
    A subclass of `Thread` that returns a value when it is joined.

    This class works by overriding the `run` method of the `Thread` class
    to store the return value of the target function in a `_return` attribute.
    When the `join` method is called, it returns the stored return value.

    Args:
        group: The thread group (unused).
        target: The target function to be run in the thread.
        name: The name of the thread.
        args: The positional arguments to be passed to the target function.
        kwargs: The keyword arguments to be passed to the target function.
    """

    def __init__(self, group=None, target=None, name=None,
                    args=(), kwargs=None):
        if kwargs is None:
            kwargs = {}
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                        **self._kwargs)

    def join(self, *args):
        Thread.join(self, *args)
        return self._return
