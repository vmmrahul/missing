import cv2

def get_cropped_img_if_2_eye(image_path):
    face_cascade = cv2.CascadeClassifier('opencv/haarcascades/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('opencv/haarcascades/haarcascade_eye.xml')
    print(image_path)
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        print(len(eyes))
        if len(eyes) >= 2:
            return roi_color


d = get_cropped_img_if_2_eye('/home/vmm/Pictures/Webcam/2021-03-01-110140.jpg')
print(d)