import cv2

import fd_utils

video_stream = 0
video_capture = cv2.VideoCapture(video_stream)

# https://github.com/opencv/opencv/tree/4.x/samples/dnn/face_detector
# https://github.com/opencv/opencv/blob/4.x/samples/dnn/models.yml

network = cv2.dnn.readNetFromCaffe("deploy.prototxt", "res10_300x300_ssd_iter_140000.caffemodel")

# cv2.dnn.readNetFromONNX()

mean = [104, 117, 123]
scale = 1.0
width = 300
height = 300

font_style = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.5
font_thickness = 3

detection_confidence_threshold = 0.7
cv2.namedWindow("video stream")

while True:
    has_frame, frame = video_capture.read()
    # image_height = frame.shape[0]
    # image_width = frame.shape[1]
    blob = cv2.dnn.blobFromImage(frame, scalefactor=scale, size=(width, height), mean=mean, swapRB=False, crop=False)
    network.setInput(blob)
    face_detections = network.forward()
    for detection_id in range(face_detections.shape[2]):
        confidence = fd_utils.get_confidence(face_detections, detection_id)
        if confidence < detection_confidence_threshold:
            continue
        bounding_box = fd_utils.get_box(face_detections, detection_id)
        fd_utils.anotate(frame, bounding_box, font_style, font_scale, font_thickness, confidence)
        # fd_utils.blur_face(frame, bounding_box, ksize=(23, 23))

    cv2.imshow("video stream", frame)
    cv2.waitKey(1)
