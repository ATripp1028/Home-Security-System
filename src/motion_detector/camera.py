"""Camera and motion detection functionality."""
import cv2
import numpy as np
from datetime import datetime
from typing import Optional, Callable

from .config import Config


class MotionDetector:
    """Detects motion using camera feed."""

    def __init__(self, camera_index: int = None, on_motion_detected: Optional[Callable] = None):
        """
        Initialize motion detector.
        
        Args:
            camera_index: Camera index (defaults to Config.CAMERA_INDEX)
            on_motion_detected: Callback function called when motion is detected
        """
        self.camera_index = camera_index or Config.CAMERA_INDEX
        self.on_motion_detected = on_motion_detected
        self.cap: Optional[cv2.VideoCapture] = None
        self.background_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=500, varThreshold=50, detectShadows=True
        )
        self.frame_count = 0
        self.running = False

    def start(self) -> bool:
        """Start the camera and begin motion detection."""
        self.cap = cv2.VideoCapture(self.camera_index)
        
        if not self.cap.isOpened():
            print(f"Error: Could not open camera {self.camera_index}")
            return False

        # Set camera properties for better performance
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)

        self.running = True
        return True

    def stop(self):
        """Stop the camera and cleanup resources."""
        self.running = False
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()

    def _detect_motion(self, frame: np.ndarray) -> tuple[bool, np.ndarray]:
        """
        Detect motion in a frame.
        
        Args:
            frame: Input frame from camera
            
        Returns:
            Tuple of (motion_detected, processed_frame)
        """
        # Apply background subtraction
        fg_mask = self.background_subtractor.apply(frame)
        
        # Apply morphological operations to reduce noise
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
        
        # Apply Gaussian blur
        fg_mask = cv2.GaussianBlur(fg_mask, (5, 5), 0)
        
        # Find contours
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        motion_detected = False
        motion_areas = []
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > Config.MIN_CONTOUR_AREA:
                motion_detected = True
                motion_areas.append(contour)
                # Draw bounding box
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Draw motion overlay
        overlay = frame.copy()
        cv2.drawContours(overlay, motion_areas, -1, (0, 255, 0), -1)
        frame = cv2.addWeighted(frame, 0.7, overlay, 0.3, 0)
        
        return motion_detected, frame

    def run(self):
        """Run the motion detection loop."""
        if not self.cap or not self.cap.isOpened():
            print("Error: Camera not started. Call start() first.")
            return


        while self.running:
            ret, frame = self.cap.read()
            
            if not ret:
                print("Error: Failed to read frame from camera")
                break

            self.frame_count += 1
            
            # Skip first few frames to let background subtractor initialize
            if self.frame_count < 30:
                cv2.imshow("Motion Detector", frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                continue

            # Detect motion
            motion_detected, processed_frame = self._detect_motion(frame)
            
            # Add status text
            status_text = "Motion Detected!" if motion_detected else "Monitoring..."
            color = (0, 0, 255) if motion_detected else (0, 255, 0)
            cv2.putText(
                processed_frame,
                status_text,
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                color,
                2,
            )
            cv2.putText(
                processed_frame,
                f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1,
            )

            cv2.imshow("Motion Detector", processed_frame)

            # Trigger callback if motion detected
            if motion_detected and self.on_motion_detected:
                self.on_motion_detected(frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

        self.stop()
