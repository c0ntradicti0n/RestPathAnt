import functools

from pathant.converters import converters


class converter:
    def __init__(self,  _from, _to, *args, method=None, **kwargs):
        self._from = _from
        self._to = _to
        self.args = args
        self.kwargs = kwargs
        self.method = method

    def __call__(self, func):
        self.func = func(*self.args, **self.kwargs, path_spec=self)

        # Improve __docs__ of func
        functools.update_wrapper(self, self.func)

        converters.append((self._from, self._to, self.func))
        return self.func
