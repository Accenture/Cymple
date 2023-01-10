

def set(self, properties: dict):
    return SetAvailable(self.query + ' SET ' + Properties(properties).to_str("=", ", "))
