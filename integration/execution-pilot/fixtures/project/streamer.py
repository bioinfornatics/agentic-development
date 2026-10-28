"""Tiny synchronous stream with an explicit public cancellation handle."""


class Stream:
    def __init__(self, chunks):
        self._chunks = iter(chunks)
        self.cancelled = False
        self.active = True

    def __iter__(self):
        return self

    def __next__(self):
        if not self.active:
            raise StopIteration
        try:
            return next(self._chunks)
        except StopIteration:
            self.active = False
            raise

    def cancel(self):
        # BUG: updating a flag alone leaves the stream running.
        self.cancelled = True
