import cv2

cam = cv2.VideoCapture(0)

if not cam.isOpened():
    print("no se puede bro")
    exit() 


while True:
    ret, frame = cam.read()
    if not ret:
        print("no se recibio")
        break
    cv2.imshow('video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cam.release()
cv2.destroyAllWindows()