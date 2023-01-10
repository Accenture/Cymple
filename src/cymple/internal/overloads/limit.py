from typing import Union


def limit(self, limitation: Union[int, str]):
    ret = f" LIMIT {limitation}"
    return LimitAvailable(self.query + ret)