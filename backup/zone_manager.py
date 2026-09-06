import json
import os


ZONE_FILE = "config/zone.json"


def save_zone(zone_type, lines=None, polygon=None):

    os.makedirs("config", exist_ok=True)

    data = {
        "type": zone_type,
        "lines": lines or [],
        "polygon": polygon or []
    }

    with open(ZONE_FILE, "w") as f:
        json.dump(data, f, indent=4)


def load_zone():

    if not os.path.exists(ZONE_FILE):
        return {
            "type": "lines",
            "lines": [],
            "polygon": []
        }

    try:

        with open(ZONE_FILE, "r") as f:
            data = json.load(f)

        # Backward compatibility with your
        # old zone.json format.
        if "points" in data:

            return {
                "type": "polygon",
                "lines": [],
                "polygon": data.get("points", [])
            }

        return {
            "type": data.get("type", "lines"),
            "lines": data.get("lines", []),
            "polygon": data.get("polygon", [])
        }

    except Exception:

        return {
            "type": "lines",
            "lines": [],
            "polygon": []
        }


def point_inside_polygon(point, polygon):

    if len(polygon) < 3:
        return False

    import cv2
    import numpy as np

    polygon_np = np.array(
        polygon,
        dtype="int32"
    )

    result = cv2.pointPolygonTest(
        polygon_np,
        point,
        False
    )

    return result >= 0


def segments_intersect(p1, p2, q1, q2):

    def orientation(a, b, c):

        value = (
            (b[1] - a[1]) * (c[0] - b[0])
            - (b[0] - a[0]) * (c[1] - b[1])
        )

        if value == 0:
            return 0

        return 1 if value > 0 else 2

    def on_segment(a, b, c):

        return (
            min(a[0], c[0]) <= b[0] <= max(a[0], c[0])
            and
            min(a[1], c[1]) <= b[1] <= max(a[1], c[1])
        )

    o1 = orientation(p1, p2, q1)
    o2 = orientation(p1, p2, q2)
    o3 = orientation(q1, q2, p1)
    o4 = orientation(q1, q2, p2)

    if o1 != o2 and o3 != o4:
        return True

    if o1 == 0 and on_segment(p1, q1, p2):
        return True

    if o2 == 0 and on_segment(p1, q2, p2):
        return True

    if o3 == 0 and on_segment(q1, p1, q2):
        return True

    if o4 == 0 and on_segment(q1, p2, q2):
        return True

    return False


def crossed_any_line(previous_point, current_point, lines):

    for line in lines:

        if len(line) != 4:
            continue

        x1, y1, x2, y2 = line

        barrier_start = (x1, y1)
        barrier_end = (x2, y2)

        if segments_intersect(
            previous_point,
            current_point,
            barrier_start,
            barrier_end
        ):
            return True

    return False