from plotter import Plotter

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_to(self, that):
        if that is None:
            return float('inf')
        dx = self.x - that.x
        dy = self.y - that.y
        return (dx**2 + dy**2) ** 0.5

    def draw(self, plotter):
        plotter.plot_point(self.x, self.y)

    def draw_to(self, that, plotter):
        plotter.plot_line(self.x, self.y, that.x, that.y)
    

    @staticmethod
    def ccw(a, b, c):
        area2 = (b.x - a.x) * (c.y - a.y) - (c.x - a.x) * (b.y - a.y)
        if area2 < 0:
            return -1
        elif area2 > 0:
            return 1
        else:
            return 0

    @staticmethod
    def collinear(a, b, c):
        return Point.ccw(a, b, c) == 0

    @staticmethod
    def between(a, b, c):
        if Point.ccw(a, b, c) != 0:
            return False
        if a.x == b.x and a.y == b.y:
            return a.x == c.x and a.y == c.y
        elif a.x != b.x:
            return (a.x <= c.x <= b.x) or (a.x >= c.x >= b.x)
        else:
            return (a.y <= c.y <= b.y) or (a.y >= c.y >= b.y)

    def __str__(self):
        return f"({self.x}, {self.y})"

# Example usage:
if __name__ == "__main__":
    plotter = Plotter()
    plotter.set_color('blue')
    p = Point(5, 6)
    q = Point(2, 2)
    print(f"p = {p}")
    print(f"q = {q}")
    print(f"dist(p, q) = {p.distance_to(q)} = {q.distance_to(p)}")
    p.draw(plotter)
    q.draw(plotter)
    p.draw_to(q, plotter)
    plotter.show()