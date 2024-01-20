class Action:
    def __init__(self, name, number, function, ascii):
        if not callable(function):
            raise ValueError("La funzione deve essere callable")
        self.name = name
        self.number = number
        self.function = function
        self.ascii = ascii

    def __str__(self):
        function_name = self.function.__name__ if hasattr(self.function, '__name__') else 'funzione anonima'
        return f"Action{{name: {self.name}, number: {self.number}, function: {function_name}, ascii: {self.ascii}}}"

    def __repr__(self):
        return self.__str__()
