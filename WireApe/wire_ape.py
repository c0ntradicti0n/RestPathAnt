import unittest
import numpy
import spacy
from Package2Rest.package2rest import Import2Rest
from pathant.Converter import converter
from pathant.PathSpec import PathSpec


@converter("resturl", "ape")
class WireApe(PathSpec):
    """
    Runs functions from library as falcon rest services
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nlp = spacy.load('en_core_web_md')

        self.dep_lookup = {l:i for i, l in enumerate (self.nlp.get_pipe("parser").labels)}

    def __iter__(self, package):
        yield from self(package)

    params = {}
    returns = {}
    route_descriptions = {}

    def __call__(self, package):
        package = list(package)
        for url, route_description in package:
            print(url)
            self.params[url] = route_description['params']
            self.returns[url] = route_description['returns']
            self.route_descriptions[url] = route_description

        self.nlp_return_descriptions = [self.nlpize(x.description) if x and x.description else None for x in self.returns.values() ]
        self.nlp_param_descriptions = {url:[self.nlpize(y.description) if y and y.description else None for y in x] for url, x in self.params.items()}

        for url, route_description in package:
            yield from self.match(url)

    def match(self, url):
        matches = [self.match_param(index, url) for index, param in enumerate(self.params[url])]
        #matches = Parallel(n_jobs=1)(delayed(self.match_param)(index, url) for index, arg in enumerate(self.params[url]))
        return matches

    def nlpize(self, text):
        doc = self.nlp(text)
        #for word in doc:
        #    word.vector[0:] = self.dep_lookup[word.dep_] * word.vector
        return doc

    def match_param(self, param_index, url):
        param = self.params[url][param_index]
        nlp_param = self.nlp_param_descriptions[url][param_index]
        calc = [nlp_param.similarity(
                    nd) if nlp_param and nd else 0 for nd in self.nlp_return_descriptions]
        match_indices = numpy.argsort(calc)[-2:]
        returns = list(self.returns.items())
        matches = [(returns[i][0], self.route_descriptions[returns[i][0]], returns[i][1]) for i in match_indices]
        print((url, param.arg_name, param.description, matches))
        target_plug = param
        return (url, self.route_descriptions[url], target_plug), matches


class TEST(unittest.TestCase):

    def test_import(self):
        list(WireApe(Import2Rest(numpy)))


if __name__ == '__main__':
    pass
