import unittest

from Parse.parse import Parse
from Scrape.scrape import Scrape
from generalape.api import Api
from generalape.TryCallApe import GeneralApe
from pathant.PathAnt import PathAnt
from pathant.Pipeline import Pipeline
from test.known_apis import apis


class testRestApe(unittest.TestCase):

    def test_get_apis(self):
        url_update: dict

        api_docs = list(Scrape("https://any-api.com/"))

    def test_read_methods_from_apis(self):
        pa = PathAnt()

        api_docs = list(list(e) for e in Scrape("https://any-api.com/"))

        apis = pa.lookup("any-api.com-page", "resturl")
        apis(api_docs)
        apes = []

        i = 0
        for html, (funs, url_update) in apis:
            url = url.format(** url_update)
            api = Api(url, funs)
            ape = GeneralApe(api=api)
            apes.append(ape)
            i += 1
            if i > 20:
                break
            print (f"scraped {i} apis, that's soon enough, because enough is enough")


        pa = PathAnt()
        pa.info()

        for edge_pipe in pa.get_all_possible_edges():
            list(edge_pipe("blub", calling_api_fun="test"))

        po = PathAnt()
        po.info()

if __name__ == '__main__':
    unittest.main()