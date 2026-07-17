from pathlib import Path
import cv2
from ultralytics import YOLO

print("Loading YOLOv8 model...")
model = YOLO("yolov8n.pt")
print("YOLOv8 loaded successfully!")

OUTPUT_FOLDER = Path("outputs")
OUTPUT_FOLDER.mkdir(exist_ok=True)


def detect_objects(video_path: str) -> str:

    input_path = Path(video_path)

    cap = cv2.VideoCapture(str(input_path))

    if not cap.isOpened():
        raise Exception("Could not open input video.")

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps <= 0:
        fps = 30

    print(f"Width: {width}")
    print(f"Height: {height}")
    print(f"FPS: {fps}")

    output_path = OUTPUT_FOLDER / f"{input_path.stem}_detected.mp4"

    # Better codec
    fourcc = cv2.VideoWriter_fourcc(*"avc1")

    writer = cv2.VideoWriter(
        str(output_path),
        fourcc,
        fps,
        (width, height)
    )

    if not writer.isOpened():
        raise Exception("VideoWriter failed to open.")

    frame_count = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        results = model(frame, verbose=False)

        annotated = results[0].plot()

        writer.write(annotated)

        frame_count += 1

        if frame_count % 30 == 0:
            print(f"Processed {frame_count} frames")

    cap.release()
    writer.release()

    print(f"Total Frames Written: {frame_count}")

    return str(output_path)