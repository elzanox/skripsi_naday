import cv2
import urllib.request
import numpy as np
import os
from datetime import datetime
import pathlib
dir = pathlib.Path().absolute()
print(dir)

net = cv2.dnn.readNet('yolo_conf/10022023-yolov4-tiny-custom/custom_config_pam_v4_20000.weights', 'yolo_conf/10022023-yolov4-tiny-custom/custom_config_pam_v4.cfg')

#if you use nvidia gpu
# net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
# net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

#if you use intel or amd gpu
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_OPENCL)

classes = []
with open("yolo_conf/classes.txt", "r") as f:
    classes = f.read().splitlines() 

example_url = ['https://picsum.photos/200/300.jpg']

#get source from url
# url = example_url[0]
url = 'http://192.168.137.12/640x480.jpg' #ip address local esp32

# #get surce from videos
# path_videos = 'media/gun_test5.mp4'
# cap = cv2.VideoCapture(path_videos)

 #get surce from photos
path_photos = 'media/test.jpg'

font = cv2.FONT_HERSHEY_PLAIN
colors = np.random.uniform(0, 255, size=(100, 3))

while True:
    #from url photos
    cap = urllib.request.urlopen(url)
    imgz= np.array(bytearray(cap.read()),dtype=np.uint8)
    img = cv2.imdecode(imgz,-1)
    
    #from videos
    # _, img = cap.read() 
         
    # #from photos
    # img  = cv2.imread(path_photos)
    
    height, width,_ = img.shape
    imgs = img.copy()
    blob = cv2.dnn.blobFromImage(img, 1/255, (416, 416), (0,0,0), swapRB=True, crop=False)
    net.setInput(blob)
    output_layers_names = net.getUnconnectedOutLayersNames()
    layerOutputs = net.forward(output_layers_names)

    boxes = []
    confidences = []
    class_ids = []
    
    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.1:
                center_x = int(detection[0]*width)
                center_y = int(detection[1]*height)
                w = int(detection[2]*width)
                h = int(detection[3]*height)

                x = int(center_x - w/2)
                y = int(center_y - h/2)

                boxes.append([x, y, w, h])
                confidences.append((float(confidence)))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.2, 0.4)
    daftar = []
    if len(indexes)>0:
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            confidence_round = round(confidences[i],2)*100
            confidence_print = ("%.2f" % confidence_round)
            label = str(classes[class_ids[i]])
            daftar.append(label)
            data = str(daftar)
            center_rect = (center_x,center_y)
            color = colors[i]
            cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
            cv2.putText(img,label, (x,y-40), font, 3, (0,0,255), 3)
            # cv2.putText(img,confidence_print, (x+50,y), font, 1, (0,255,0), 2)
            cv2.circle(img, center_rect, radius=1, color=(0, 0, 255), thickness=2)
    
    print(daftar)
    cv2.imshow('Image', img)
    
    key = cv2.waitKey(1)
    if key==27:
        break
    if key==32:
        ts = datetime.timestamp(datetime.now())
        IN = str(ts) + ".jpg"
        dataset_name = os.path.join(dir,'dataset',IN)
        cv2.imwrite(dataset_name, imgs)
        print('Pengambilan dataset {} berhasil'.format(IN))

cap.release()
cv2.destroyAllWindows()