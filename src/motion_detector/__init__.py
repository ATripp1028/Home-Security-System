"""Motion detector application - camera-based motion detection with notifications."""
import sys

from .camera import MotionDetector
from .notifier import NotificationManager
from .config import Config


def main():
    """Main entry point for the motion detector application."""
    # Validate configuration
    errors = Config.validate()
    if errors:
        print("Configuration errors:")
        for error in errors:
            print(f"  - {error}")
        print("\nPlease check your .env file configuration.")
        sys.exit(1)

    # Create notification manager
    notifier = NotificationManager()

    # Define callback for motion detection
    def on_motion_detected(frame):
        """Callback function called when motion is detected."""
        notifier.notify(frame)

    # Create and start motion detector
    detector = MotionDetector(on_motion_detected=on_motion_detected)

    try:
        if not detector.start():
            print("Failed to start camera. Exiting.")
            sys.exit(1)

        detector.run()
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        detector.stop()


if __name__ == "__main__":
    main()
