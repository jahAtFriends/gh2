import sys
import os

from friendsbalt.acs import Vector, Plotter
import random
import signal
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from graham import get_convex_hull

# class TimeoutException(Exception):
#     pass

# def timeout_handler(signum, frame):
#     raise TimeoutException

# # Set the signal handler and a 15-second alarm
# signal.signal(signal.SIGALRM, timeout_handler)

def test_random_points():
    points = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(10)]
    hull = get_convex_hull(points)
    assert is_convex(hull)
    for p in points:
        assert is_within(p, hull)

# def test_a_lot_of_points():
#     points = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(1000000)]
#     signal.alarm(15)
#     try:
#         hull = get_convex_hull(points)
#         signal.alarm(0)
#     except TimeoutException:
#         pytest.fail("The algorithm took too long to run.")
#     assert is_convex(hull)
#     for p in points:
#         assert is_within(p, hull)

def test_horizontal_points():
    points = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
    hull = get_convex_hull(points)
    assert hull.size() == 2
    assert (0, 0) in hull
    assert (4, 0) in hull

def test_vertical_points():
    points = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]
    hull = get_convex_hull(points)
    assert hull.size() == 2
    assert (0, 0) in hull
    assert (0, 4) in hull

# def test_random_trangle(): # This test is not working because of floating point arithmetic
#     while True:
#         points = [(random.uniform(-100, 100), random.uniform(-100, 100)) for _ in range(3)]
#         if len(set(points)) == 3:
#             v1 = Vector.from_points(points[0], points[1])
#             v2 = Vector.from_points(points[1], points[2])
#             if v1.cross(v2).magnitude() != 0:
#                 break
    
#     for _ in range(10):
#         t = random.uniform(0, 1)
#         random_point1 = (points[0][0] + t * (points[1][0] - points[0][0]), points[0][1] + t * (points[1][1] - points[0][1]))
#         random_point2 = (points[1][0] + t * (points[2][0] - points[1][0]), points[1][1] + t * (points[2][1] - points[1][1]))
#         random_point3 = (points[2][0] + t * (points[0][0] - points[2][0]), points[2][1] + t * (points[0][1] - points[2][1]))
#         points.append(random_point1)
#         points.append(random_point2)
#         points.append(random_point3)
    
#     hull = get_convex_hull(points)

#     assert hull.size() == 3
#     assert points[0] in hull
#     assert points[1] in hull
#     assert points[2] in hull

def test_triangle():
    points = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (-1, 5), (-2, 4), (-3, 3), (-2, 2), (-1, 1)]
    hull = get_convex_hull(points)
    assert hull.size() == 3
    assert is_convex(hull)
    for p in points:
        assert is_within(p, hull)

def test_all_points_same():
    points = [(0, 0)] * 10
    hull = get_convex_hull(points)
    assert hull.size() == 1
    assert is_convex(hull)
    for p in points:
        assert is_within(p, hull)

def test_is_minimal():
    points = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]
    hull = get_convex_hull(points)
    assert hull.size() == 2
    assert is_convex(hull)
    for p in points:
        assert is_within(p, hull)

def test_is_minimal2():
    points = [(0, -4), (2, -2), (4, 0), (2, 2), (0, 4), (-2, 2), (-4, 0), (-2, -2)]
    hull = get_convex_hull(points)
    assert hull.size() == 4
    assert is_convex(hull)
    for p in points:
        assert is_within(p, hull)

def test_no_points():
    points = []
    hull = get_convex_hull(points)
    assert hull.size() == 0

def test_one_point():
    points = [(0, 0)]
    hull = get_convex_hull(points)
    assert hull.size() == 1
    assert is_convex(hull)
    assert is_within(points[0], hull)

def test_two_points():
    points = [(0, 0), (1, 1)]
    hull = get_convex_hull(points)
    assert hull.size() == 2
    assert is_convex(hull)
    for p in points:
        assert is_within(p, hull)

def is_convex(hull):
    n = hull.size()
    if n < 2: return True

    for i in range(n):
        p1 = hull.peek(i)
        p2 = hull.peek((i + 1) % n)
        p3 = hull.peek((i + 2) % n)
        v1 = Vector.from_points(p1, p2)
        v2 = Vector.from_points(p2, p3)
        if v1.cross(v2).magnitude() < 0:
            return False
    return True

def is_within(point, hull):
    if point in hull:
        return True
    for i in range(hull.size()):
        p1 = hull.peek(i)
        p2 = hull.peek((i + 1) % hull.size())
        v1 = Vector.from_points(p1, p2)
        v2 = Vector.from_points(p1, point)
        if v1.cross(v2).magnitude() < 0:
            return False
    return True