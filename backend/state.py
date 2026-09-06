import threading
import time


class SharedState:

    def __init__(self):

        self.lock = threading.Lock()

        # Latest annotated frame
        self.frame = None

        # Detector status
        self.running = False
        self.camera_source = None
        self.camera_status = "OFFLINE"

        # -----------------------------
        # ZONE
        # -----------------------------

        self.zone_type = "lines"
        self.line_segments = []
        self.polygon_points = []

        # -----------------------------
        # DETECTION
        # -----------------------------

        self.people_detected = 0
        self.people_in_zone = 0
        self.fps = 0

        # -----------------------------
        # ALERTS
        # -----------------------------

        self.last_alert = None
        self.alert_count = 0

        # -----------------------------
        # EVENTS
        # -----------------------------

        self.events = []

        # -----------------------------
        # EVIDENCE
        # -----------------------------

        self.evidence_images = []

        # -----------------------------
        # TRACKING
        # -----------------------------

        self.previous_positions = {}

        self.last_update = time.time()


STATE = SharedState()