from pathant.PathSpec import PathSpec


class Ape(PathSpec):
    def __init__(self, api_fun, method):
        self.method = method
        self.api_fun = api_fun

    def __iter__(self):
        yield from (self.url + fun for fun in self.funs)

    def __call__(self, *args, **kwargs):
        yield from args




