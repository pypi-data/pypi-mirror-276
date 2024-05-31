import json
import re
from .ExObject import ExObject
from parsel import Selector, SelectorList


class ExSelector(ExObject):
    def __init__(self, default=None):
        super().__init__(default)
        if type(default) is str:
            self.default = Selector(text=default)

    def xpath(self, query):
        return ExSelector(self.default.xpath(query))

    def extract(self):
        return ExSelector(self.default.extract())

    def FirstOrDefault(self):
        if type(self.default) is SelectorList:
            return self.extract().FirstOrDefault()
        return super().FirstOrDefault()

    def FirstOrDefaultString(self) -> str:
        if type(self.default) is SelectorList:
            return self.extract().FirstOrDefaultString()
        return super().FirstOrDefaultString()

    def LastOrDefaultString(self):
        if type(self.default) is SelectorList:
            return self.extract().LastOrDefaultString()
        return super().LastOrDefaultString()

    def FIrstCleanString(self) -> str:
        r = self.default
        if type(self.default) is SelectorList:
            r = self.default.extract()
        if type(r) is list:
            for item in r:
                if item.strip():
                    return item.strip()
            return ""

        return super().LastOrDefaultString()

    def LastCleanString(self) -> str:
        r = self.default
        if type(self.default) is SelectorList:
            r = self.default.extract()
        if type(r) is list:
            for index in range(0, len(r)):
                item = r[len(r) - index - 1]
                if item.strip():
                    return item.strip()
            return ""

        return super().LastOrDefaultString()

    def AllStringArray(self, clean=False):
        if type(self.default) is SelectorList:
            r = []
            for item in self.default.extract():
                if clean:
                    item = item.strip()
                    if item:
                        r.append(item)
                else:
                    r.append(item)
            return r
        elif type(self.default) is list:
            r = []
            for item in self.default:
                if clean:
                    item = item.strip()
                    if item:
                        r.append(item)
                else:
                    r.append(item)
            return r
        return [super().LastOrDefaultString()]

    def AllString(self):
        return "/n".join(self.AllStringArray())

    def AllCleanString(self):
        return "/n".join(self.AllStringArray(clean=True)).strip()

    def __next__(self):
        try:
            if type(self.default) is SelectorList:
                if "iter" not in dir(self):
                    self.iter = self.default.__iter__()
                # return ExScrapyObj(self.default.__next__())
                return ExSelector(next(self.iter))
            else:
                return ExSelector(self.defaultIter.__next__())
        except:
            raise StopIteration()
