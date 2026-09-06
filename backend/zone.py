import cv2
import numpy as np


def point_inside_zone(point, zone):
    """
    Check whether a point is inside a restricted zone.

    zone can contain:
    - 2 points -> a straight line
    - 3+ points -> polygon / connected line boundary
    """

    if zone is None or len(zone) < 2:
        return False

    x, y = point

    # If exactly 2 points, treat it as a line.
    # A point is considered inside when it is very close to the line.
    if len(zone) == 2:
        p1 = np.array(zone[0], dtype=float)
        p2 = np.array(zone[1], dtype=float)
        p = np.array([x, y], dtype=float)

        line = p2 - p1
        length = np.linalg.norm(line)

        if length == 0:
            return False

        distance = abs(np.cross(line, p - p1)) / length

        # tolerance in pixels
        return distance < 15

    # 3+ points = polygon
    polygon = np.array(zone, dtype=np.int32)

    result = cv2.pointPolygonTest(
        polygon,
        (float(x), float(y)),
        False
    )

    return result >= 0


def draw_zone(frame, zone, color=(0, 0, 255), thickness=2):
    """
    Draw the restricted zone on the video frame.

    2 points:
        Draw a straight line.

    3+ points:
        Draw connected lines and close the polygon.
    """

    if zone is None or len(zone) < 2:
        return frame

    points = np.array(zone, dtype=np.int32)

    if len(zone) == 2:
        cv2.line(
            frame,
            tuple(points[0]),
            tuple(points[1]),
            color,
            thickness
        )

    else:
        cv2.polylines(
            frame,
            [points],
            True,
            color,
            thickness
        )

    return frame