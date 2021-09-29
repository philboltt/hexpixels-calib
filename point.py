class Point(object):

    tolerance = 2

    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    @classmethod
    def from_str(cls, input):
        x,y = input.strip().strip("(").strip(")").split(",")
        pt = cls(x.strip(), y.strip())
        return pt

    def matches(self, other):
        if abs(other.x - self.x) <= self.tolerance and abs(other.y - self.y) <= self.tolerance:
            return True
        return False

    def __repr__(self):
        return "({0}, {1})".format(self.y, self.y)
