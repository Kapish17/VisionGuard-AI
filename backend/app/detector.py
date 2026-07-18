from pathlib import Path
import cv2
from ultralytics import YOLO

print("Loading YOLOv8s model...")
model = YOLO("yolov8s.pt")
print("YOLOv8s loaded successfully!")

OUTPUT_FOLDER = Path("outputs")
OUTPUT_FOLDER.mkdir(exist_ok=True)


def detect_objects(video_path: str):

    input_path = Path(video_path)

    cap = cv2.VideoCapture(str(input_path))

    if not cap.isOpened():
        raise Exception("Could not open input video.")

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps <= 0:
        fps = 30

    print(f"Width : {width}")
    print(f"Height: {height}")
    print(f"FPS   : {fps}")

    output_path = OUTPUT_FOLDER / f"{input_path.stem}_detected.mp4"

    fourcc = cv2.VideoWriter_fourcc(*"avc1")

    writer = cv2.VideoWriter(
        str(output_path),
        fourcc,
        fps,
        (width, height),
    )

    if not writer.isOpened():
        raise Exception("VideoWriter failed to open.")

    frame_count = 0

    # Dashboard
    summary = {
        "person": 0,
        "bicycle": 0,
        "car": 0,
        "motorcycle": 0,
        "bus": 0,
        "truck": 0,
        "backpack": 0,
        "handbag": 0,
        "suitcase": 0,
        "cell phone": 0,
    }

    # Store unique tracking IDs
    unique_objects = {
        "person": set(),
        "bicycle": set(),
        "car": set(),
        "motorcycle": set(),
        "bus": set(),
        "truck": set(),
        "backpack": set(),
        "handbag": set(),
        "suitcase": set(),
        "cell phone": set(),
    }

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        results = model.track(
            frame,
            persist=True,
            tracker="bytetrack.yaml",
            conf=0.60,
            iou=0.45,
            classes=[0, 1, 2, 3, 5, 7, 24, 26, 28, 67],
            verbose=False,
        )

        result = results[0]

        if result.boxes is not None:

            for box in result.boxes:

                # Skip if tracker has not assigned an ID yet
                if box.id is None:
                    continue

                cls = int(box.cls[0])
                class_name = model.names[cls]

                # Ignore unexpected classes
                if class_name not in unique_objects:
                    continue

                track_id = int(box.id[0])

                unique_objects[class_name].add(track_id)

        annotated = result.plot()

        writer.write(annotated)

        frame_count += 1

        if frame_count % 30 == 0:
            print(f"Processed {frame_count} frames")

    cap.release()
    writer.release()

    # Convert sets into counts
    for key in summary.keys():
        summary[key] = len(unique_objects[key])

    print("\n===== Detection Summary =====")

    for name, count in summary.items():
        print(f"{name}: {count}")

    print("=============================\n")

    return {
        "video_path": str(output_path),
        "summary": summary,
    }