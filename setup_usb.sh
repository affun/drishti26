#!/bin/bash
# USB Wired Connection Setup for DRISHTI + Redmi K50i
# Run this in Terminal before starting surveillance

echo "=== DRISHTI USB Wired Setup ==="
echo ""

# Check if ADB is installed
if ! command -v adb &> /dev/null; then
    echo "ADB not found. Installing..."
    brew install android-platform-tools
fi

# Check device connection
echo "Checking for connected Android device..."
adb devices

echo ""
echo "If you see your device listed above, proceed."
echo "If not, enable USB Debugging on your Redmi K50i:"
echo "  Settings > About phone > tap MIUI version 7 times"
echo "  Settings > Additional settings > Developer options > USB Debugging ON"
echo ""

# Set up reverse port forwarding
echo "Setting up USB tunnel (port 8080)..."
adb reverse tcp:8080 tcp:8080

echo ""
echo "Done! Now:"
echo "  1. Open IP Webcam on your Redmi K50i"
echo "  2. Tap 'Start server'"
echo "  3. In DRISHTI dashboard, select 'Android IP Camera (USB Wired)'"
echo "  4. Click START SURVEILLANCE"
echo ""
echo "The stream will flow through USB-C, not Wi-Fi."