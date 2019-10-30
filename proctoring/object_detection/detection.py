import requests
import tensorflow as tf
from collections import Counter
import os


SERVER_URL = 'http://localhost:8501/v1/models/yolo:predict'
class_names = [c.strip() for c in open('object_detection/bin/coco.names').readlines()]


def object_detect(file_url):

    image = tf.keras.preprocessing.image.load_img(file_url, target_size=(416, 416))
    image_arr = tf.keras.preprocessing.image.img_to_array(image) / 255.

    predict_request = {
        "instances": [{'input_1': image_arr.tolist()}]
    }

    # Sending the API request and getting the response

    response = requests.post(SERVER_URL, json=predict_request)
    prediction = response.json()['predictions'][0]

    boxes = [prediction['yolo_nms_0']]
    scores = [prediction['yolo_nms_1_1']]
    classes = [prediction['yolo_nms_2_2']]
    nums = [prediction['yolo_nms_3_3']]

    object_no_list = Counter(classes[0][:prediction['yolo_nms_3_3']]).most_common()  # Gets object classes and count

    object_dict = {}

    for i in object_no_list:  # Gets Object Class names from coco
        label = class_names[int(i[0])]
        object_dict[label] = i[1]

    image_response = {'labeled_classes': object_dict,
                      'metadata': {'boxes': boxes, 'scores': scores, 'classes': classes, 'nums': nums}}

    object_list = list(object_dict.keys())

    if 'person' in object_list:
        if object_dict['person'] > 1:
            image_response['anomaly_detected'] = 1
        else:
            image_response['anomaly_detected'] = 0
    if 'person' not in object_list:
        image_response['anomaly_detected'] = 1
    elif 'cell phone' in object_list:
        image_response['anomaly_detected'] = 1
    elif 'laptop' in object_list:
        image_response['anomaly_detected'] = 1
    else:
        image_response['anomaly_detected'] = 0

    os.remove(file_url)  # Deletes saved image file

    return image_response
