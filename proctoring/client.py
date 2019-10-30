import requests
import json
file = 'street.jpg'

with open(file, 'rb') as f: 
    filename = 'filename.jpg'
    files = {'file': (filename, f)}
    
    r = requests.post('http://0.0.0.0:8000/object_detection/detect_object', files=files)
