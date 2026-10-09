import sys
sys.dont_write_bytecode = True

import cv2
import os
import time
import numpy as np

# ==========================================
# NEXA AI - FACE AUTHENTICATION SETTINGS
# ==========================================

DATA_DIR = "face_data"
FACE_SIZE = (200, 200)
SAMPLES_REQUIRED = 40
MATCH_THRESHOLD = 65

WINDOW_NAME = "NEXA AI - Face Authentication"
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600


# ==========================================
# LOAD FACE DETECTION MODEL
# ==========================================

def get_face_cascade():
    cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades
        + "haarcascade_frontalface_default.xml"
    )

    if cascade.empty():
        print("Error: Could not load face detection model.")
        return None

    return cascade


# ==========================================
# DETECT FACES
# ==========================================

def detect_faces(gray, cascade):
    return cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(100, 100)
    )


# ==========================================
# REGISTER FACE
# ==========================================

def collect_face_samples(camera, cascade):
    """Register the user's face on first run."""

    os.makedirs(DATA_DIR, exist_ok=True)

    print("\n======================================")
    print("           NEXA AI FACE SETUP")
    print("======================================")
    print("No registered face was found.")
    print("Look directly at the camera.")
    print("Move your head slightly between captures.")
    print("Press Q to cancel registration.")
    print("======================================")

    samples = []
    frame_count = 0

    while len(samples) < SAMPLES_REQUIRED:
        success, frame = camera.read()

        if not success:
            print("Error: Could not read from the camera.")
            return None

        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detect_faces(gray, cascade)

        message = "Show exactly one face"

        if len(faces) == 1:
            x, y, w, h = faces[0]

            face = cv2.resize(
                gray[y:y + h, x:x + w],
                FACE_SIZE
            )

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            frame_count += 1

            # Capture periodically to reduce duplicate frames.
            if frame_count % 4 == 0:
                samples.append(face.copy())

            message = (
                f"Registering face: "
                f"{len(samples)}/{SAMPLES_REQUIRED}"
            )

        elif len(faces) > 1:
            message = "Only one person should be visible"

        cv2.putText(
            frame,
            message,
            (20, 45),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            "Press Q to cancel",
            (20, frame.shape[0] - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        cv2.imshow(WINDOW_NAME, frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            print("Face registration cancelled.")
            return None

    # Save registered face samples.
    for index, face in enumerate(samples, start=1):
        path = os.path.join(
            DATA_DIR,
            f"face_{index:03d}.jpg"
        )

        if not cv2.imwrite(path, face):
            print("Error: Could not save face samples.")
            return None

    print("\nFace registration completed successfully.")
    return samples


# ==========================================
# LOAD SAVED FACE SAMPLES
# ==========================================

def load_registered_faces():
    """Load previously registered face samples."""

    if not os.path.isdir(DATA_DIR):
        return []

    samples = []

    for filename in sorted(os.listdir(DATA_DIR)):
        if not filename.lower().endswith(
            (".jpg", ".jpeg", ".png")
        ):
            continue

        path = os.path.join(DATA_DIR, filename)

        image = cv2.imread(
            path,
            cv2.IMREAD_GRAYSCALE
        )

        if image is not None:
            samples.append(
                cv2.resize(image, FACE_SIZE)
            )

    return samples


# ==========================================
# DISPLAY AUTHENTICATION MESSAGE
# ==========================================

def show_success_screen(frame):
    """Display a larger, foreground success screen."""

    success_text = "AUTHENTICATION SUCCESSFUL"

    cv2.putText(
        frame,
        success_text,
        (20, frame.shape[0] // 2),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        3
    )

    cv2.imshow(WINDOW_NAME, frame)

    # Try to keep the camera window in the foreground.
    try:
        cv2.setWindowProperty(
            WINDOW_NAME,
            cv2.WND_PROP_TOPMOST,
            1
        )
    except cv2.error:
        pass

    # Keep the success message visible for 3 seconds.
    cv2.waitKey(3000)


# ==========================================
# AUTHENTICATE REGISTERED FACE
# ==========================================

def authenticate_face():
    """Register on first use and authenticate on later runs."""

    if not hasattr(cv2, "face"):
        print("\nError: OpenCV face-recognition module is missing.")
        print("Install opencv-contrib-python.")
        return False

    cascade = get_face_cascade()

    if cascade is None:
        return False

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("\nError: Could not access the camera.")
        return False

    try:
        # Create and enlarge the camera window.
        cv2.namedWindow(
            WINDOW_NAME,
            cv2.WINDOW_NORMAL
        )

        cv2.resizeWindow(
            WINDOW_NAME,
            WINDOW_WIDTH,
            WINDOW_HEIGHT
        )
        
        # Position the camera window near the top of the screen.
        cv2.moveWindow(WINDOW_NAME, 150, 40)

        # Attempt to bring the camera window to the front.
        try:
            cv2.setWindowProperty(
                WINDOW_NAME,
                cv2.WND_PROP_TOPMOST,
                1
            )
        except cv2.error:
            pass

        registered_samples = load_registered_faces()

        # Register a face if there are not enough saved samples.
        if len(registered_samples) < 10:
            registered_samples = collect_face_samples(
                camera,
                cascade
            )

            if not registered_samples:
                return False

        # Train the LBPH face-recognition model.
        model = cv2.face.LBPHFaceRecognizer_create()

        labels = np.zeros(
            len(registered_samples),
            dtype=np.int32
        )

        model.train(
            registered_samples,
            labels
        )

        print("\n======================================")
        print("       NEXA AI AUTHENTICATION")
        print("======================================")
        print("Checking registered face...")

        print("======================================")

        match_started = None
        start_time = time.time()
        match_duration = 2.0

        while time.time() - start_time < 60:
            success, frame = camera.read()

            if not success:
                print("Error: Could not read from camera.")
                return False

            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2GRAY
            )

            faces = detect_faces(gray, cascade)

            status = "Looking for your face..."
            color = (255, 255, 255)
            matched = False

            if len(faces) == 1:
                x, y, w, h = faces[0]

                face = cv2.resize(
                    gray[y:y + h, x:x + w],
                    FACE_SIZE
                )

                _, confidence = model.predict(face)

                matched = confidence <= MATCH_THRESHOLD

                if matched:
                    status = "REGISTERED FACE MATCHED"
                    color = (0, 255, 0)
                else:
                    status = "FACE NOT RECOGNIZED"
                    color = (0, 0, 255)

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    color,
                    3
                )

            elif len(faces) > 1:
                status = "ONLY ONE FACE ALLOWED"
                color = (0, 0, 255)

            # Require a continuous match for two seconds.
            if matched:
                if match_started is None:
                    match_started = time.time()

                if time.time() - match_started >= match_duration:
                    show_success_screen(frame)
                    return True
            else:
                match_started = None

            # Display the application name.
            cv2.putText(
                frame,
                "NEXA AI",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (255, 255, 255),
                2
            )

            # Display the authentication status.
            cv2.putText(
                frame,
                status,
                (20, 85),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,
                2
            )

            cv2.putText(
                frame,
                "Press Q to cancel",
                (20, frame.shape[0] - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )

            cv2.imshow(WINDOW_NAME, frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                print("\nAuthentication cancelled.")
                return False

        print("\nAuthentication timed out.")
        return False

    finally:
        camera.release()
        cv2.destroyAllWindows()


# ==========================================
# RUN FACE AUTHENTICATION DIRECTLY
# ==========================================

if __name__ == "__main__":
    result = authenticate_face()

    if result:
        print("Access granted.")
    else:
        print("Access denied.")

