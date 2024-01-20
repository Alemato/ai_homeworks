class State:
    def __init__(self, number, position):
        self.number = number
        self.position = position

    def __str__(self):
        return f"State{{number: {self.number}, position: {self.position}}}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        return self.number == other.number and self.position == other.position
