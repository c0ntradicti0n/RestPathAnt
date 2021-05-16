import unittest
from collections import Callable
from json import dumps
from pprint import pprint
from wsgiref.simple_server import make_server

import falcon as falcon
import numpy

from pathant.Converter import converter
from pathant.PathSpec import PathSpec
from docstring_parser import parse

import json_tricks

app = falcon.App()



@converter("import", "resturl")
class Import2Rest(PathSpec):
    """
    Runs functions from library as falcon rest services
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def __iter__(self, package):
        yield from self(package)

    classes = []
    functions = {}


    def __call__(self, package):
        for namme, thing in package.__dict__.items():

            typ = type(thing)
            doc_string = thing.__doc__
            doc_parse = parse(doc_string)

            if isinstance(thing, Callable) and doc_parse and (doc_parse.params or doc_parse.returns):
                fname = str(thing)

                class T:
                    fname = str(thing)
                    doc = doc_parse

                    def on_post(self, req, resp):
                        input = req.media
                        try:
                            input = {k: eval(v) for k, v in input.items()}
                        except Exception as e:
                            input = json_tricks.loads(input)

                        print (self.doc.__repr__())
                        result = Import2Rest.functions[self.fname](**input)

                        try:
                            resp.body = dumps(result)
                        except Exception as e:
                            resp.body = json_tricks.dumps(result)

                T.__qualname__ = str(fname)
                self.functions[fname] = thing
                t = T()

                path = f"/{namme}"
                app.add_route(path, t)
                self.classes.append(T)



                yield f"localhost:8000{path}", {"method":"post", "params": doc_parse.params, "returns": doc_parse.returns}



class TEST(unittest.TestCase):

    def test_import(self):

        Import2Rest(numpy)


if __name__ == '__main__':
    app = falcon.App()

    with make_server('', 8000, app) as httpd:
            print('Serving on port 8000...')

            # Serve until process is killed
            ir = list(Import2Rest(numpy))
            app = app

            httpd.serve_forever()

