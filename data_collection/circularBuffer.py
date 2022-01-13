import collections

class CircularBuffer(object):
    '''
        Circular Buffer implementation using the collections library
    '''
    def __init__(self, buffer_size) -> None:
        super().__init__()
        self.content = None
        self.size = buffer_size

    def update(self, scalar) -> None:
        try:
            self.content.appendleft(scalar)
        except AttributeError:
            self.content = collections.deque([0.] * self.size, maxlen = self.size)

