import wifi
import socketpool
import time
import pwmio
from microcontroller import Pin

# WiFi Configuration
WIFI_SSID = "Redmi Note 8 Pro"
WIFI_PASSWORD = "stavros2"

# Connect to WiFi
print("Connecting to WiFi...")
wifi.radio.connect(WIFI_SSID, WIFI_PASSWORD)
print("Connected to WiFi!")
print("IP address:", wifi.radio.ipv4_address)

# Create Socket
pool = socketpool.SocketPool(wifi.radio)
server = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
server.bind((str(wifi.radio.ipv4_address), 80))
server.listen(1)
server.settimeout(None)



current_mode = "manual"

# Functions

# HTML Page
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Pico W Control</title>
</head>
<body>
    <h1>Raspberry Pi Pico W Control</h1>
    <h3>Steering</h3>
    <input type="range" id="steering" min="-90" max="90" value="0" oninput="sendSlider()">
    <h3>Motor Speed</h3>
    <button onclick="sendButton('forward')">Forward</button>
    <button onclick="sendButton('stop')">Stop</button>
    <button onclick="sendButton('backward')">Backward</button>
    <h3>Mode Selection</h3>
    <button onclick="toggleMode()">Toggle Mode</button>
    <p>Current Mode: <span id="mode-display">Manual</span></p>

    <script>
        let currentMode = "manual";

        function sendSlider() {
            if (currentMode === "manual") {
                const value = document.getElementById('steering').value;
                fetch(`/steering?value=${value}`);
            }
        }

        function sendButton(action) {
            if (currentMode === "manual") {
                fetch(`/motor?action=${action}`);
            }
        }

        function toggleMode() {
            currentMode = currentMode === "manual" ? "autonomous" : "manual";
            document.getElementById("mode-display").innerText = currentMode.charAt(0).toUpperCase() + currentMode.slice(1);
            fetch(`/mode?state=${currentMode}`);
        }
    </script>
</body>
</html>
"""

# Server Loop
print("Starting server...")
while True:
    print("Waiting for a connection...")
    conn, addr = server.accept()
    print(f"Connection from {addr}")
    
    try:
        request = conn.recv(1024)  # Don't decode yet
        print("Raw request received:", request)
        
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nHello, World!"
        conn.send(response.encode("utf-8"))
        conn.close()
    except Exception as e:
        print("Error:", e)
        conn.close()