import streamlit as st
import numpy as np
from PIL import Image
import cv2
import time
import os

from streamlit_drawable_canvas import st_canvas

from detector import DrishtiDetector
from state import STATE
from zone_manager import save_zone, load_zone


# ==================================================
# PAGE
# ==================================================

st.set_page_config(
    page_title="DRISHTI",
    layout="wide"
)


# ==================================================
# INITIAL STATE
# ==================================================

if "zone_loaded" not in st.session_state:

    saved_zone = load_zone()

    with STATE.lock:
        STATE.zone_type = saved_zone["type"]
        STATE.line_segments = saved_zone["lines"]
        STATE.polygon_points = saved_zone["polygon"]

    st.session_state.zone_loaded = True


if "camera_source" not in st.session_state:
    st.session_state.camera_source = "Demo Video"


# ==================================================
# DETECTOR
# ==================================================

@st.cache_resource
def get_detector():
    return DrishtiDetector()


detector = get_detector()


# ==================================================
# HEADER
# ==================================================

st.title("DRISHTI")
st.caption("AI-POWERED INTELLIGENT VIDEO SURVEILLANCE")
st.divider()


# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.header("CONTROL")

camera_source = st.sidebar.selectbox(
    "Camera Source",
    [
        "Demo Video",
        "Android IP Camera (Wi-Fi)",
        "Android IP Camera (USB Wired)"
    ]
)


# --- Source-specific URL input ---

stream_url = "test.mp4"

if camera_source == "Android IP Camera (Wi-Fi)":

    stream_url = st.sidebar.text_input(
        "Phone Stream URL",
        value="http://192.168.43.123:8080/video",
        help="IP Webcam URL. Find it in the IP Webcam app after starting the server."
    )

    st.sidebar.info(
        "\u26a0 Make sure the Redmi and Mac are on the same Wi-Fi / hotspot."
    )

elif camera_source == "Android IP Camera (USB Wired)":

    st.sidebar.markdown("""
    **USB Wired Setup:**
    1. Connect Redmi K50i to Mac via USB-C
    2. Enable **USB Debugging** on phone
       (Settings > Developer options)
    3. Install ADB: `brew install android-platform-tools`
    4. In Terminal run:
       ```
       adb reverse tcp:8080 tcp:8080
       ```
    5. Start IP Webcam on phone
    6. DRISHTI will connect via USB tunnel
    """)

    stream_url = "http://localhost:8080/video"


st.sidebar.divider()

st.sidebar.subheader("RESTRICTED ZONE")

zone_type = st.sidebar.radio(
    "Zone Type",
    ["Barrier Lines", "Polygon"]
)

st.sidebar.caption(
    "Barrier Lines: draw one or more straight virtual fences."
)
st.sidebar.caption(
    "Polygon: define an enclosed restricted area."
)


# ==================================================
# BUTTONS
# ==================================================

start = st.sidebar.button(
    "START SURVEILLANCE",
    use_container_width=True
)

stop = st.sidebar.button(
    "STOP SURVEILLANCE",
    use_container_width=True
)


if start:
    if camera_source == "Demo Video":
        source = "test.mp4"
    else:
        source = stream_url

    if not source:
        st.sidebar.error("Enter the phone stream URL.")
    else:
        try:
            detector.start(source)
            st.session_state.camera_source = camera_source
            st.sidebar.success("Surveillance started.")
        except Exception as e:
            st.sidebar.error(str(e))


if stop:
    detector.stop()
    st.sidebar.info("Surveillance stopped.")


# ==================================================
# ZONE CONTROLS
# ==================================================

st.sidebar.divider()

if st.sidebar.button("CLEAR ZONE", use_container_width=True):
    with STATE.lock:
        STATE.line_segments = []
        STATE.polygon_points = []
    save_zone("lines", [], [])
    st.rerun()


if st.sidebar.button("SAVE ZONE", use_container_width=True):
    with STATE.lock:
        save_zone(
            STATE.zone_type,
            STATE.line_segments,
            STATE.polygon_points
        )
    st.sidebar.success("Restricted zone saved.")


# ==================================================
# METRICS
# ==================================================

col1, col2, col3, col4 = st.columns(4)

with STATE.lock:
    running = STATE.running
    people = STATE.people_detected
    alerts = STATE.alert_count
    camera_status = STATE.camera_status

with col1:
    st.metric("CAMERA", "CAM-01")

with col2:
    st.metric(
        "STATUS",
        "ONLINE" if running else "STANDBY"
    )

with col3:
    st.metric("PEOPLE", people)

with col4:
    st.metric("THREATS", alerts)

st.divider()


# ==================================================
# LIVE FEED
# ==================================================

st.subheader("AI SURVEILLANCE FEED")


@st.fragment(run_every=0.08)
def live_feed():

    with STATE.lock:
        frame = STATE.frame
        running = STATE.running
        people = STATE.people_detected
        alerts = STATE.alert_count

    if frame is not None:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        st.image(rgb, use_container_width=True)
    else:
        st.info("Start surveillance to display the camera feed.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "SURVEILLANCE",
            "ACTIVE" if running else "STANDBY"
        )

    with col2:
        st.metric("PEOPLE DETECTED", people)

    with col3:
        st.metric("ALERTS", alerts)


live_feed()


# ==================================================
# ZONE DRAWING
# ==================================================

st.divider()

st.subheader("RESTRICTED ZONE CONFIGURATION")


# --- CLEAR INSTRUCTIONS ---

if zone_type == "Barrier Lines":
    st.info(
        "\U0001f4cc **How to draw barrier lines:**\n\n"
        "1. Look at the camera frame below\n"
        "2. Click **\u2018Line\u2019** in the toolbar above the canvas\n"
        "3. **Click and drag** on the frame to draw a red line across the area you want to protect\n"
        "4. Draw multiple lines if needed\n"
        "5. Click **SAVE ZONE** in the sidebar\n\n"
        "The AI will trigger an alert when a person **crosses** any of these lines."
    )
else:
    st.info(
        "\U0001f4cc **How to draw a polygon zone:**\n\n"
        "1. Look at the camera frame below\n"
        "2. Click **\u2018Polygon\u2019** in the toolbar above the canvas\n"
        "3. **Click multiple points** on the frame to outline the restricted area\n"
        "4. Double-click to close the shape\n"
        "5. Click **SAVE ZONE** in the sidebar\n\n"
        "The AI will trigger an alert when a person **enters** this area."
    )


with STATE.lock:
    drawing_frame = STATE.frame


if drawing_frame is not None:

    rgb = cv2.cvtColor(drawing_frame, cv2.COLOR_BGR2RGB)
    background = Image.fromarray(rgb)

    canvas_width = background.width
    canvas_height = background.height

    max_width = 1000
    if canvas_width > max_width:
        scale = max_width / canvas_width
        canvas_width = max_width
        canvas_height = int(canvas_height * scale)
        background = background.resize((canvas_width, canvas_height))

    if zone_type == "Barrier Lines":
        drawing_mode = "line"
    else:
        drawing_mode = "polygon"

    canvas_result = st_canvas(
        fill_color="rgba(255, 0, 0, 0.15)",
        stroke_width=4,
        stroke_color="#ff0000",
        background_image=background,
        update_streamlit=True,
        height=canvas_height,
        width=canvas_width,
        drawing_mode=drawing_mode,
        key="zone_canvas"
    )

    # ==================================================
    # EXTRACT DRAWINGS
    # ==================================================

    if canvas_result.json_data is not None:

        objects = canvas_result.json_data.get("objects", [])

        # ----------------------------------------------
        # BARRIER LINES
        # ----------------------------------------------

        if zone_type == "Barrier Lines":

            new_lines = []

            for obj in objects:
                if obj.get("type") != "line":
                    continue

                x1 = obj.get("x1", 0)
                y1 = obj.get("y1", 0)
                x2 = obj.get("x2", 0)
                y2 = obj.get("y2", 0)

                new_lines.append([
                    int(x1), int(y1),
                    int(x2), int(y2)
                ])

            scale_x = drawing_frame.shape[1] / canvas_width
            scale_y = drawing_frame.shape[0] / canvas_height

            scaled_lines = []
            for line in new_lines:
                x1, y1, x2, y2 = line
                scaled_lines.append([
                    int(x1 * scale_x),
                    int(y1 * scale_y),
                    int(x2 * scale_x),
                    int(y2 * scale_y)
                ])

            with STATE.lock:
                STATE.zone_type = "lines"
                STATE.line_segments = scaled_lines

        # ----------------------------------------------
        # POLYGON
        # ----------------------------------------------

        else:

            for obj in objects:
                if obj.get("type") != "polygon":
                    continue

                points = obj.get("points", [])
                polygon = []

                for point in points:
                    polygon.append([
                        int(point.get("x", 0)),
                        int(point.get("y", 0))
                    ])

                scale_x = drawing_frame.shape[1] / canvas_width
                scale_y = drawing_frame.shape[0] / canvas_height

                scaled_polygon = [
                    [int(x * scale_x), int(y * scale_y)]
                    for x, y in polygon
                ]

                with STATE.lock:
                    STATE.zone_type = "polygon"
                    STATE.polygon_points = scaled_polygon

else:
    st.warning(
        "Start surveillance first to see the camera frame, "
        "then draw the zone on it."
    )


# ==================================================
# SECURITY ALERTS
# ==================================================

st.divider()

st.subheader("SECURITY ALERTS")

with STATE.lock:
    events = list(STATE.events)

if events:
    for event in reversed(events[-5:]):
        st.error(
            f"INTRUSION DETECTED | "
            f"{event['camera']} | "
            f"{event['time']} | "
            f"Person #{event['track_id']}"
        )
else:
    st.success("NO ACTIVE THREATS")


# ==================================================
# INCIDENT LOG
# ==================================================

st.subheader("INCIDENT LOG")

if events:
    st.dataframe(events, use_container_width=True)
else:
    st.info("No incidents recorded.")


# ==================================================
# EVIDENCE GALLERY
# ==================================================

st.divider()

st.subheader("EVIDENCE CAPTURES")

with STATE.lock:
    evidence = list(STATE.evidence_images)

if evidence:
    cols = st.columns(min(4, len(evidence)))
    for idx, path in enumerate(reversed(evidence[-4:])):
        if os.path.exists(path):
            with cols[idx]:
                st.image(path, caption=os.path.basename(path))
else:
    st.info("No evidence captured yet.")