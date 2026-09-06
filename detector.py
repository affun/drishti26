import cv2
import threading
import time
import os
from datetime import datetime

from ultralytics import YOLO

from state import STATE
from stream import CameraStream
from zone import draw_zone
from zone_manager import crossed_any_line
from alert_manager import trigger_alert


class DrishtiDetector:

    def __init__(self):
        self.stream = None
        self.model = YOLO("yolo11n.pt")
        self.thread = None
        self._stop_flag = False

        os.makedirs("evidence", exist_ok=True)

    # --------------------------------------------------
    # START
    # --------------------------------------------------

    def start(self, source):

        if self.thread is not None and self.thread.is_alive():
            self.stop()
            time.sleep(0.3)

        self._stop_flag = False

        with STATE.lock:
            STATE.running = True
            STATE.camera_source = source
            STATE.camera_status = "CONNECTING..."
            STATE.people_detected = 0
            STATE.people_in_zone = 0
            STATE.alert_count = 0
            STATE.events = []
            STATE.previous_positions = {}
            STATE.evidence_images = []

        self.thread = threading.Thread(
            target=self._run,
            args=(source,),
            daemon=True
        )

        self.thread.start()

    # --------------------------------------------------
    # STOP
    # --------------------------------------------------

    def stop(self):

        self._stop_flag = True

        with STATE.lock:
            STATE.running = False
            STATE.camera_status = "OFFLINE"

        if self.stream is not None:
            self.stream.stop()
            self.stream = None

        if self.thread is not None:
            self.thread.join(timeout=3)
            self.thread = None

    # --------------------------------------------------
    # MAIN AI LOOP
    # --------------------------------------------------

    def _run(self, source):

        # --- Open stream with retries ---
        for attempt in range(3):
            try:
                self.stream = CameraStream(source)
                self.stream.start()
                break
            except Exception as e:
                with STATE.lock:
                    STATE.camera_status = f"CONNECTING ({attempt+1}/3)..."
                time.sleep(1.5)
        else:
            with STATE.lock:
                STATE.camera_status = f"ERROR: Could not open {source}"
                STATE.running = False
            return

        with STATE.lock:
            STATE.camera_status = "ONLINE"

        frame_count = 0
        last_fps_time = time.time()
        fps_counter = 0
        current_fps = 0

        while not self._stop_flag:

            ret, frame = self.stream.read()

            if not ret or frame is None:
                time.sleep(0.02)
                continue

            frame_count += 1
            fps_counter += 1

            # FPS calculation
            now = time.time()
            if now - last_fps_time >= 1.0:
                current_fps = fps_counter
                fps_counter = 0
                last_fps_time = now

            # Process every 3rd frame for performance
            process_this_frame = (frame_count % 3 == 0)

            annotated = frame.copy()

            # ------------------------------------------
            # GET CURRENT ZONE
            # ------------------------------------------

            with STATE.lock:
                zone_type = STATE.zone_type
                line_segments = list(STATE.line_segments)
                polygon_points = list(STATE.polygon_points)

            # Draw zone on frame
            if zone_type == "lines" and line_segments:
                for line in line_segments:
                    if len(line) == 4:
                        x1, y1, x2, y2 = line
                        cv2.line(
                            annotated,
                            (int(x1), int(y1)),
                            (int(x2), int(y2)),
                            (0, 0, 255),
                            3
                        )
            elif zone_type == "polygon" and len(polygon_points) >= 3:
                annotated = draw_zone(
                    annotated,
                    polygon_points
                )

            # ------------------------------------------
            # YOLO PERSON TRACKING
            # ------------------------------------------

            people = 0
            people_inside = 0

            if process_this_frame:

                # Resize for faster inference
                small_frame = cv2.resize(frame, (640, 480))

                results = self.model.track(
                    small_frame,
                    persist=True,
                    classes=[0],
                    conf=0.35,
                    imgsz=320,
                    verbose=False
                )

                current_positions = {}

                if results and results[0].boxes is not None:

                    boxes = results[0].boxes
                    h_scale = frame.shape[0] / 480
                    w_scale = frame.shape[1] / 640

                    for box in boxes:

                        if box.id is None:
                            continue

                        track_id = int(box.id[0])

                        # Scale coordinates back to original frame size
                        sx1, sy1, sx2, sy2 = map(float, box.xyxy[0])
                        x1 = int(sx1 * w_scale)
                        y1 = int(sy1 * h_scale)
                        x2 = int(sx2 * w_scale)
                        y2 = int(sy2 * h_scale)

                        people += 1

                        # Bottom-center of bounding box
                        center_x = int((x1 + x2) / 2)
                        center_y = int(y2)

                        current_positions[track_id] = (
                            center_x, center_y
                        )

                        # ----------------------------
                        # INTRUSION DETECTION
                        # ----------------------------

                        intrusion = False

                        with STATE.lock:
                            prev_pos = STATE.previous_positions.get(
                                track_id
                            )

                        if zone_type == "lines" and line_segments:

                            if prev_pos is not None:
                                intrusion = crossed_any_line(
                                    prev_pos,
                                    (center_x, center_y),
                                    line_segments
                                )

                        elif zone_type == "polygon" and len(polygon_points) >= 3:

                            from zone import point_inside_zone
                            intrusion = point_inside_zone(
                                (center_x, center_y),
                                polygon_points
                            )

                        if intrusion:
                            people_inside += 1

                        # ----------------------------
                        # DRAW PERSON
                        # ----------------------------

                        color = (0, 0, 255) if intrusion else (0, 255, 0)

                        cv2.rectangle(
                            annotated,
                            (x1, y1),
                            (x2, y2),
                            color,
                            2
                        )

                        cv2.circle(
                            annotated,
                            (center_x, center_y),
                            5,
                            (0, 0, 255),
                            -1
                        )

                        label = f"ID:{track_id}"
                        if intrusion:
                            label += " ALERT"

                        cv2.putText(
                            annotated,
                            label,
                            (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6,
                            color,
                            2
                        )

                        # ----------------------------
                        # TRIGGER ALERT
                        # ----------------------------

                        if intrusion:

                            cv2.putText(
                                annotated,
                                "INTRUSION DETECTED",
                                (x1, y2 + 25),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.7,
                                (0, 0, 255),
                                2
                            )

                            evidence_path = self._save_evidence(
                                annotated,
                                track_id
                            )

                            trigger_alert(
                                track_id=track_id,
                                evidence_path=evidence_path
                            )

                # Update positions for next frame
                with STATE.lock:
                    STATE.previous_positions = current_positions

            # ------------------------------------------
            # DRAW FPS
            # ------------------------------------------

            cv2.putText(
                annotated,
                f"FPS: {current_fps}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            # ------------------------------------------
            # UPDATE SHARED STATE
            # ------------------------------------------

            with STATE.lock:
                STATE.frame = annotated
                STATE.people_detected = people
                STATE.people_in_zone = people_inside
                STATE.last_update = time.time()

        print("[Detector] Loop ended.")

    # --------------------------------------------------
    # EVIDENCE CAPTURE
    # --------------------------------------------------

    def _save_evidence(self, frame, track_id):

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S_%f"
        )[:-3]

        filename = f"evidence/alert_{timestamp}_id{track_id}.jpg"

        cv2.imwrite(filename, frame)

        with STATE.lock:
            STATE.evidence_images.append(filename)
            STATE.evidence_images = (
                STATE.evidence_images[-20:]
            )

        return filename


# ------------------------------------------------------
# DIRECT TEST
# ------------------------------------------------------

if __name__ == "__main__":

    detector = DrishtiDetector()
    detector.start("test.mp4")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        detector.stop()