from graphguard.models import Detection

detection = Detection(
    label="person",
    confidence=0.98,
    bbox=(10, 20, 300, 500),
)

print(detection)