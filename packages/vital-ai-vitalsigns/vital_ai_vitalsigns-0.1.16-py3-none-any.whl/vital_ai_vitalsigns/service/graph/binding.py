
class Binding:
    def __init__(self, variable: str, property_uri: str, optional: bool = False, unbound_symbol: str = "UNKNOWN"):
        self.variable = variable
        self.property_uri = property_uri
        self.optional = optional
        self.unbound_symbol = unbound_symbol



