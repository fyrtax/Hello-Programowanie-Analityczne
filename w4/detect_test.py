import os as os
import time

import matplotlib.pyplot as plt
from ultralytics import YOLO

# yolo26l 0.79s
yolo_model_name = 'yolo26l'
model = YOLO(os.path.join(yolo_model_name + '.pt'))

path_image_file = "./images/000008.jpg"
path_detection_visualization_file = os.path.splitext(path_image_file)[0] + "_yolo.jpg"
conficence_threshold = 0.5

time_start = time.perf_counter()
detection_results = model.predict(source=path_image_file, save=False, verbose=False, conf=conficence_threshold)
time_end = time.perf_counter()
print(f"Inference took: {time_end - time_start:.6f} seconds")
result = detection_results[0]
has_detections = result.boxes.shape[0] > 0

if has_detections:
    visualization = result.plot()
    # cv2.imwrite(path_detection_visualization_file, visualization)
    plt.figure(1)
    plt.imshow(visualization[:, :, ::-1])

    class_names = [result.names[int(cls_id)] for cls_id in result.boxes.cls]
    print("Detected classes:", class_names)

    conficence_thresholds = result.boxes.conf.detach().cpu().numpy()
    # conficence_thresholds = result.boxes.conf.numpy()
    print("Confidence scores:", conficence_thresholds)

    boxes_array = result.boxes.xyxy.detach().cpu().numpy()
    # boxes_array = result.boxes.xyxy.numpy()  # Bounding box coordinates
    print("Bounding box coordinates (x1, y1, x2, y2):")
    for box in boxes_array:
        print(box)

    plt.show()
