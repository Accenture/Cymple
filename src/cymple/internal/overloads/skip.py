from typing import Union


def skip(self, skip_count: Union[int, str]):
    ret = f" SKIP {skip_count}"
    return SkipAvailable(self.query + ret)
