import subprocess
import time
import threading
from datetime import datetime

from state import STATE


class AlertManager:

    def __init__(self):
        self.last_alert_time = 0
        self.cooldown = 4.0   # seconds between alerts
        self._sound_lock = threading.Lock()

    def trigger(self, track_id, evidence_path=None):

        now = time.time()

        with self._sound_lock:
            if now - self.last_alert_time < self.cooldown:
                return False
            self.last_alert_time = now

        # Non-blocking alert sound
        self._play_sound()

        # Log event
        event = {
            "type": "INTRUSION",
            "time": datetime.now().strftime("%H:%M:%S"),
            "camera": "CAM-01",
            "track_id": track_id,
            "evidence": evidence_path
        }

        with STATE.lock:
            STATE.alert_count += 1
            STATE.last_alert = event
            STATE.events.append(event)
            # Keep last 50 events
            STATE.events = STATE.events[-50:]

        print(f"[ALERT] Intrusion by Person #{track_id} at {event['time']}")

        return True

    def _play_sound(self):

        def _sound():
            try:
                # macOS system sound
                subprocess.run(
                    ["afplay", "/System/Library/Sounds/Ping.aiff"],
                    check=False,
                    timeout=3
                )
            except Exception:
                pass

        t = threading.Thread(target=_sound, daemon=True)
        t.start()


# Global instance
_ALERT_MANAGER = AlertManager()


def trigger_alert(track_id, evidence_path=None):
    """Public API called by detector."""
    return _ALERT_MANAGER.trigger(track_id, evidence_path)