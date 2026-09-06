import cv2
import time


class CameraStream:

    def __init__(self, source):
        self.source = source
        self.cap = None

    def start(self):

        self.cap = cv2.VideoCapture(self.source)

        # Optimize for network streams
        if isinstance(self.source, str) and self.source.startswith("http"):
            # Reduce buffer for lower latency
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            # Set timeout
            self.cap.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 5000)
            self.cap.set(cv2.CAP_PROP_READ_TIMEOUT_MSEC, 5000)

        if not self.cap.isOpened():
            raise RuntimeError(
                f"Could not open camera source: {self.source}"
            )

        # Warm-up: skip first few buffered frames
        for _ in range(3):
            self.cap.read()
            time.sleep(0.05)

        return self

    def read(self):

        if self.cap is None:
            return False, None

        return self.cap.read()

    def stop(self):

        if self.cap is not None:
            self.cap.release()
            self.cap = None