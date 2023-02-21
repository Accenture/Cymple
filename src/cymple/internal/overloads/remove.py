
def remove(properties):
    if type(properties) != list:
        properties = [properties]
    ret = f" REMOVE {', '.join(properties)}"
    return RemoveAvailable(self.query + ret)
