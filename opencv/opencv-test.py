import cv2 

img = cv2.imread('loathe01.jpg')
cv2.imshow('loathe', img)

#imgres = cv2.resize(img, ())

"""imgred = img[:,:,2]
cv2.imshow('rojo', imgred)
imggreen = img[:,:,1]
cv2.imshow('verde', imggreen)
imgblue = img[:,:,0]
cv2.imshow('azul', imgblue)"""


blur = cv2.GaussianBlur(img, (5,5), 0)
cv2.imshow('blur', blur)

bordes = cv2.Canny(img, 100, 200)
cv2.imshow('canny', bordes)

contornos = cv2.findContours(bordes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for i in contornos:
    area = cv2.contourArea(contornos)
    print(f"area: {area}")

cv2.waitKey(0)
cv2.destroyAllWindows()
