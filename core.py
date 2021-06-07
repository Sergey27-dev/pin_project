import cv2
import numpy as np
import os
from numpy import array, sqrt

def click_exit():
        exit(0)

class ImageLoad:
    image = []
    grayImg = []
    s = 0.33
    v = 0
    light_b = 200
    dark_b = 150
    area_arr = []
    lengh_arr = []
    ploshad = 0

    def grab_contours(cnts):
        if len(cnts) == 2:
            return cnts[0]
        elif len(cnts) == 3:
            return cnts[1]

    def auto_canny(self, path):
        self.area_arr.clear()
        
        self.image = open(path,'rb')
        chunk = self.image.read()
        chunk_arr = np.frombuffer(chunk, dtype=np.uint8)
        self.image = cv2.imdecode(chunk_arr,cv2.IMREAD_COLOR)
        self.findCanny()

        

    def findCanny(self):
        self.ploshad = 0
        img = self.image.copy()
        img = cv2.bitwise_not(img)
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        #cv2.imshow("closed", img_hsv)

        light_black = (0, 0, self.light_b)
        dark_black = (0, self.dark_b, 255)
        mask = cv2.inRange(img_hsv, light_black, dark_black)

        result = cv2.bitwise_and(img, img, mask=mask)
        self.grayImg = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        self.v = np.median(self.grayImg)  # Ищет среднее значение серого для Canny
        ret, thresh = cv2.threshold(self.grayImg, 127, 255, 0)
        self.grayImg = cv2.medianBlur(thresh, 3)

        self.area_arr.clear()
        lower = int(max(0, self.v - self.v * 0.3))
        upper = int(min(255, (1.0 + self.s) * self.v))

        edged = cv2.Canny(self.grayImg, lower, upper)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 2))
        closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)

        cnts = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_NONE)
        cnts = ImageLoad.grab_contours(cnts)

        contour_image = closed.copy()
        area = 0
        for c in cnts:
            area = cv2.contourArea(c)
            cv2.drawContours(contour_image, [c], 0, (150, 50, 10), 1)
            if area != 0:
                cm_ar = (area * 2.14) / (96 * 40)
                self.ploshad+=cm_ar
                cm_ar = str(cm_ar)
                cm_ar += "см^2/" + str(area) + "px\n"
                self.area_arr.append(cm_ar)
                print((area * 2.14) / (96 * 40), "см^2/", area, "px")

        cv2.fillPoly(contour_image, cnts, color=((150, 50, 10)))
        #cv2.imshow("area", contour_image)
        k = cv2.waitKey(0)
        if k == 27:
            cv2.destroyAllWindows()
        cv2.imwrite(os.path.join('','tempimg.jpg'), contour_image)

    def Central_line(self):
        self.area_arr.clear()
        self.lengh_arr.clear()
        img = cv2.cvtColor(self.image.copy(), cv2.COLOR_BGR2GRAY)
        v = np.median(img)
        img = cv2.medianBlur(img,3)
        img_bw = img <= 128
        img_bw = 255*img_bw.astype("uint8")
        

        s = 0.33

        lower = int(max(0, v - v * 0.3))
        upper = int(min(255, (1.0 + s) * v))

        edge = cv2.Canny(img,lower,upper)
        #cv2.imshow("edged",edge)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,2))
        closed = cv2.morphologyEx(edge, cv2.MORPH_CLOSE, kernel)
        #cv2.imshow("closed", closed)

        cnts = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        cnts = ImageLoad.grab_contours(cnts)
    



        for c in cnts:
            #print('conturs in c', c)


            maxCoord = c[0][0]
            for i in range(len(array(c))):
                for j in range(len(array(c[i]))):
                    if any(maxCoord < c[i][j]):
                        maxCoord = c[i][j]

            print("max",maxCoord)

             

            M = cv2.moments(c)

            if M["m00"] != 0:
                cx = int(M["m10"]/M["m00"])
                cy = int(M["m01"]/M["m00"])

            

            vector = np.vectorize(np.int)

            central_line = cv2.line(img,tuple(c[0][0]),tuple(vector(maxCoord)),(255,255,255),1)
            add_len = str(len(c)) + '\n'
            self.lengh_arr.append(add_len)
            print("len",len(c))

        cv2.imwrite(os.path.join('','lines.jpg'), img)
        cv2.waitKey(0)






