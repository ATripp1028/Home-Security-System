# Motion Detector

A Python-based security camera system that detects motion and sends email notifications to the owner.

## Features

- Real-time motion detection using computer vision
- Email notifications with attached motion snapshots
- Configurable detection sensitivity and notification settings
- Cooldown period to prevent notification spam
- Simple command-line interface

## Requirements

- Python 3.12 or higher
- `uv` package manager
- A camera/webcam connected to your system
- Email account for sending notifications (Gmail recommended)

## Installation

1. Clone or navigate to this repository:
   ```bash
   cd "Home Security System"
   ```

2. Install dependencies using `uv`:
   ```bash
   uv sync
   ```

3. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

4. Edit `.env` and configure your settings:
   - `EMAIL_FROM`: Your email address (sender)
   - `EMAIL_TO`: Recipient email address
   - `EMAIL_PASSWORD`: Your email app password (see Gmail setup below)
   - `CAMERA_INDEX`: Camera device index (usually 0 for first camera)

## Gmail Setup (Recommended)

If using Gmail, you'll need to create an App Password:

1. Go to your Google Account settings
2. Enable 2-Step Verification
3. Go to Security → App passwords
4. Generate an app password for "Mail"
5. Use this app password in your `.env` file (not your regular password)

## Usage

Run the motion detector:

```bash
uv run motion-detector
```

Or using Python directly:

```bash
uv run python -m motion_detector
```

The application will:
- Open a window showing the camera feed
- Display "Monitoring..." when no motion is detected
- Display "Motion Detected!" and send an email notification when motion is detected
- Press 'q' to quit

## Configuration

Edit the `.env` file to customize settings:

- `CAMERA_INDEX`: Camera device index (default: 0)
- `MIN_CONTOUR_AREA`: Minimum area for motion detection (default: 500, increase for less sensitivity)
- `NOTIFICATION_ENABLED`: Enable/disable notifications (default: true)
- `NOTIFICATION_COOLDOWN_SECONDS`: Seconds between notifications (default: 60)
- `EMAIL_ENABLED`: Enable/disable email notifications (default: true)
- `SMTP_SERVER`: SMTP server address (default: smtp.gmail.com)
- `SMTP_PORT`: SMTP server port (default: 587)

## How It Works

1. The camera captures frames in real-time
2. A background subtraction algorithm detects changes between frames
3. Motion contours are identified and filtered by size
4. When motion is detected, an email notification is sent with a snapshot
5. A cooldown period prevents excessive notifications

## Troubleshooting

**Camera not opening:**
- Check that a camera is connected
- Try different `CAMERA_INDEX` values (0, 1, 2, etc.)
- On Linux, ensure you have video capture permissions

**Email not sending:**
- Verify your email credentials in `.env`
- For Gmail, use an App Password (not your regular password)
- Check that `NOTIFICATION_ENABLED=true` and `EMAIL_ENABLED=true`
- Verify your network connection

**Too many false positives:**
- Increase `MIN_CONTOUR_AREA` to reduce sensitivity
- Ensure the camera has stable lighting
- Wait for the background model to initialize (first 30 frames)

## License

This project is provided as-is for personal use.
