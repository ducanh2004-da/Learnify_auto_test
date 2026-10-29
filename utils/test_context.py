class APIContext:
    def __init__(self):
        self._variables = {}

    def set_variable(self, key: str, value):
        self._variables[key] = value

    def get_variable(self, key: str):
        return self._variables.get(key)