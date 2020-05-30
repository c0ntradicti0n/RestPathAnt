from pathant.PathSpec import PathSpec


class Api(PathSpec):
    def __init__(self, url, funs):
        self.url = url
        self.funs = funs

    def __iter__(self):
        yield from (self.url + fun for fun in self.funs)




