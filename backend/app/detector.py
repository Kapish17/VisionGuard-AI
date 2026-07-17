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

    # Maximum simultaneous detections
    max_counts = {}

    # Dashboard always shows these classes
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

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        results = model(
            frame,
            conf=0.60,
            iou=0.45,
            classes=[0, 1, 2, 3, 5, 7, 24, 26, 28, 67],
            verbose=False,
        )

        result = results[0]

        current_counts = {}

        if result.boxes is not None:
            for box in result.boxes:
                cls = int(box.cls[0])
                class_name = model.names[cls]

                current_counts[class_name] = current_counts.get(class_name, 0) + 1

        # Keep maximum simultaneous count
        for cls_name, count in current_counts.items():
            if count > max_counts.get(cls_name, 0):
                max_counts[cls_name] = count

        annotated = result.plot()

        writer.write(annotated)

        frame_count += 1

        if frame_count % 30 == 0:
            print(f"Processed {frame_count} frames")

    cap.release()
    writer.release()

    # Update dashboard values
    for key in summary.keys():
        summary[key] = max_counts.get(key, 0)

    print("\n===== Detection Summary =====")
    for name, count in summary.items():
        print(f"{name}: {count}")
    print("=============================\n")

    return {
        "video_path": str(output_path),
        "summary": summary,
    }