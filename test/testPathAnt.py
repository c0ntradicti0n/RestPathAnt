import unittest

from Scrape.scrape import Scrape
from generalape.api import Api
from generalape.generalape import GeneralApe
from pathant.PathAnt import PathAnt
from pathant.Pipeline import Pipeline
from test.known_apis import apis


class testRestApe(unittest.TestCase):

    def test_make_apis(self):
        url_update: dict
        apes = []

        apis = list(Parse(Scrape("https://any-api.com/")))

        for url, (funs, url_update) in apis.items():
            url = url.format(** url_update)
            api = Api(url, funs)
            ape = GeneralApe(api=api)
            apes.append(ape)


        pa = PathAnt()
        pa.info()

        for edge_pipe in pa.get_all_possible_edges():
            list(edge_pipe("blub", calling_api_fun="test"))

        po = PathAnt()
        po.info()

if __name__ == '__main__':
    unittest.main()