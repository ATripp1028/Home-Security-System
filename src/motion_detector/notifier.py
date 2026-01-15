"""Notification system for motion detection alerts."""
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from typing import Optional
import cv2
import numpy as np

from .config import Config


class NotificationManager:
    """Manages notifications when motion is detected."""

    def __init__(self):
        self.last_notification_time: Optional[datetime] = None

    def _is_cooldown_active(self) -> bool:
        """Check if we're in the cooldown period to prevent spam."""
        if not self.last_notification_time:
            return False
        
        elapsed = (datetime.now() - self.last_notification_time).total_seconds()
        return elapsed < Config.NOTIFICATION_COOLDOWN_SECONDS

    def send_email_notification(self, frame: Optional[np.ndarray] = None) -> bool:
        """
        Send email notification about motion detection.
        
        Args:
            frame: Optional frame image to attach to email
            
        Returns:
            True if notification was sent successfully, False otherwise
        """
        if not Config.EMAIL_ENABLED or not Config.NOTIFICATION_ENABLED:
            return False

        if self._is_cooldown_active():
            return False

        try:
            # Create message
            msg = MIMEMultipart()
            msg["From"] = Config.EMAIL_FROM
            msg["To"] = Config.EMAIL_TO
            msg["Subject"] = f"Motion Detected - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

            # Create email body
            body = f"""
Motion has been detected by your security camera!

Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Camera Index: {Config.CAMERA_INDEX}

Please check your camera feed for details.
            """
            msg.attach(MIMEText(body, "plain"))

            # Attach frame if provided
            if frame is not None:
                try:
                    # Encode frame as JPEG
                    _, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
                    image_bytes = buffer.tobytes()
                    
                    image_attachment = MIMEImage(image_bytes)
                    image_attachment.add_header(
                        "Content-Disposition",
                        "attachment",
                        filename=f"motion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg",
                    )
                    msg.attach(image_attachment)
                except Exception as e:
                    print(f"Warning: Could not attach image to email: {e}")

            # Send email
            server = smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT)
            server.starttls()
            server.login(Config.EMAIL_FROM, Config.EMAIL_PASSWORD)
            server.send_message(msg)
            server.quit()

            self.last_notification_time = datetime.now()
            return True

        except Exception as e:
            print(f"Error sending email notification: {e}")
            return False

    def notify(self, frame: Optional[np.ndarray] = None) -> bool:
        """
        Send notification about motion detection.
        
        Args:
            frame: Optional frame image to include in notification
            
        Returns:
            True if notification was sent successfully, False otherwise
        """
        if not Config.NOTIFICATION_ENABLED:
            return False

        success = False
        if Config.EMAIL_ENABLED:
            success = self.send_email_notification(frame) or success

        return success
