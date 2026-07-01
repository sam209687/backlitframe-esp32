# Smart Showroom AI

Commercial multi-shop showroom automation system.

- **python_app/** — PySide6 dashboard + AI brain (voice, LED control, scheduling, licensing)
- **esp32_firmware/** — PlatformIO project for the ESP32 (LED, WiFi, HTTP API)
- **database/** — SQLite database (`smartshowroom.db`) + init script
- **config/** — JSON configuration (app, voice, led, display, device)
- **media/** — Per-product images/videos
- **logs/** — Runtime logs
- **installers/** — PyInstaller build output goes here later

## Quick start (Ubuntu)

```bash
# 1. Set up Python environment
./setup.sh

# 2. Activate venv
source venv/bin/activate

# 3. Initialize the database
python database/init_db.py

# 4. Run the dashboard
python main.py
```

## ESP32 firmware (PlatformIO)

Open `esp32_firmware/` as a PlatformIO project in VS Code (requires the
PlatformIO IDE extension), then:

```bash
cd esp32_firmware
pio run              # build
pio run -t upload    # flash to ESP32
pio device monitor    # serial monitor
```

## Architecture

```
Python (dashboard + brain)
   |
SQLite (customers, features, products, devices, schedules)
   |
JSON config (voice.json, led.json, app.json, display.json, device.json)
   |
ESP32 firmware (LED / WiFi / HTTP API)
```

Features (voice, display, LED, signboard) are toggled per customer via
`customer_features` in SQLite, so the same codebase serves every
subscription tier without forking the code.
