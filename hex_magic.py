
import cv2 as cv
import json
from point import Point

f = open("calibration.dat","r")
lines = f.readlines()
f.close()

points = []
for line in lines:
    idx, val = line.split(":")
    pt = Point.from_str(val)
    points.append(pt)

template_image = cv.imread("HexPixels_template2.tif", 1)
radius = 3
font                   = cv.FONT_HERSHEY_SIMPLEX
fontScale              = 0.5
fontColor              = (255,255,255)
lineType               = 1

def draw_points(col=(255,0,0)):
    for i, pt in enumerate(points):
        cv.circle(template_image, (pt.x, pt.y), radius, col, 3)
        
def draw_labels():
    for i, pt in enumerate(points):
        text = str(i%30)
        text_width, text_height = cv.getTextSize(text, font, fontScale, lineType)[0]
        adj_x  = int(text_width/2)
        adj_y = int(text_height/2)
        cv.putText(template_image,text, 
                    (pt.x-adj_x, pt.y+adj_y), 
                    font, 
                    fontScale,
                    fontColor,
                    lineType)                  


source = "Water_Drops_and_Waves_on_Lake_Water_9.mov"
cap = cv.VideoCapture(source)

while True:
    ret, frame = cap.read()
    
    if ret == True:
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        for i, pt in enumerate(points):
            col = frame[pt.y, pt.x]
            color = (int(col[0]), int(col[1]), int(col[2]))
            print(type(col[0]))
            cv.circle(template_image, (pt.x, pt.y), radius, color, 3)

        cv.imshow("Result", template_image)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    else:
        break

cap.release()

cv.waitKey(0)
cv.destroyAllWindows()    
