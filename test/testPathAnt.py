import unittest

from generalape.api import Api
from generalape.generalape import GeneralApe
from pathant.PathAnt import PathAnt
from test.known_apis import apis


class testRestApe(unittest.TestCase):

    def test_make_apis(self):
        url_update: dict
        apes = []
        for url, (funs, url_update) in apis.items():
            url = url % url_update
            api = Api(url, funs)
            ape = GeneralApe(api=api)
            apes.append(ape)


        pa = PathAnt()

        for path in pa.get_all_paths():
            path()


if __name__ == '__main__':
    unittest.main()