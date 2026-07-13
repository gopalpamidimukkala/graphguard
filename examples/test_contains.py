from graphguard.graph import Node
from graphguard.graph.geometry import contains, inside

person = Node(
    id=0,
    label="person",
    bbox=(100, 100, 400, 500),
    confidence=1.0,
)

helmet = Node(
    id=1,
    label="helmet",
    bbox=(180, 120, 260, 200),
    confidence=1.0,
)

print("Contains:", contains(person, helmet))
print("Inside:", inside(helmet, person))