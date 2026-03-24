import cv2
import numpy as np


def get_confidence(detections, id):
    return detections[0, 0, id, 2]


def get_box(detections, id):
    return detections[0, 0, id, 3:7]


def anotate(frame, box, font_style, font_scale, font_thickness, confidence):
    image_height = frame.shape[0]
    image_width = frame.shape[1]
    bounding_box = box * np.array([image_width, image_height, image_width, image_height])
    (x1, y1, x2, y2) = bounding_box.astype('int')
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    label = 'Confidence: %.4f' % confidence
    label_size, base_line = cv2.getTextSize(label, font_style, font_scale, font_thickness)
    cv2.rectangle(frame, (x1, y1 - label_size[1]), (x1 + label_size[0], y1 + base_line), (255, 255, 255), cv2.FILLED)
    cv2.putText(frame, label, (x1, y1), font_style, font_scale, (0, 0, 0))


def blur_face(frame, box, ksize=(23, 23)):
    image_height = frame.shape[0]
    image_width = frame.shape[1]
    bounding_box = box * np.array([image_width, image_height, image_width, image_height])
    (x1, y1, x2, y2) = bounding_box.astype('int')
    face_region = frame[y1:y2, x1:x2]
    blurred_face = cv2.GaussianBlur(face_region, ksize, 30)
    frame[y1:y2, x1:x2] = blurred_face

# class PlotDrawer:
#    def __init__(self, imsize=200):
#        self.data = deque([0]*imsize, maxlen=imsize)
#        self.imsize = imsize
#    
#    def add(self, value):
#        self.data.popleft()
#        self.data.append(value)
#
#    def plot(self, window_name):
#        image = np.zeros((self.imsize, self.imsize, 3), dtype=np.uint8)
#        for i in range(1, len(self.data)):
#            cv2.line(image,
#                     (i-1, self.imsize - int(self.data[i-1]*self.imsize)),
#                     (i, self.imsize - int(self.data[i]*self.imsize)),
#                     (255, 255, 255), 2)
#        cv2.imshow(window_name, image)
#        cv2.waitKey(1)
