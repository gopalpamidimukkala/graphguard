from math import sqrt

from graphguard.graph import Node


def center(node: Node) -> tuple[float, float]:
    x1, y1, x2, y2 = node.bbox
    return ((x1 + x2) / 2, (y1 + y2) / 2)


def area(node: Node) -> float:
    x1, y1, x2, y2 = node.bbox
    return max(0.0, x2 - x1) * max(0.0, y2 - y1)


def intersection_area(a: Node, b: Node) -> float:
    ax1, ay1, ax2, ay2 = a.bbox
    bx1, by1, bx2, by2 = b.bbox

    x_left = max(ax1, bx1)
    y_top = max(ay1, by1)
    x_right = min(ax2, bx2)
    y_bottom = min(ay2, by2)

    if x_right <= x_left or y_bottom <= y_top:
        return 0.0

    return (x_right - x_left) * (y_bottom - y_top)


def union_area(a: Node, b: Node) -> float:
    return area(a) + area(b) - intersection_area(a, b)


def iou(a: Node, b: Node) -> float:
    union = union_area(a, b)

    if union == 0:
        return 0.0

    return intersection_area(a, b) / union


def distance(a: Node, b: Node) -> float:
    ax, ay = center(a)
    bx, by = center(b)

    return sqrt((ax - bx) ** 2 + (ay - by) ** 2)