from .typedefs import Properties


def set(self, properties: Properties):
    return SetAvailable(self.query + ' SET ' + Properties(properties).to_str("=", ", "))
