import cv2 as cv

class Point(object):

    tolerance = 2

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def matches(self, other):
        if abs(other.x - self.x) <= self.tolerance and abs(other.y - self.y) <= self.tolerance:
            return True
        return False

    def __repr__(self):
        return "({0},{1})".format(self.x, self.y)

source = "hexpixels_slow_oriented.mp4"
cap = cv.VideoCapture(source)

radius = 3

points = []

while True:
    ret, frame = cap.read()
    if ret == True:

        orig = frame.copy()
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # apply a Gaussian blur to the image then find the brightest
        # region
        gray = cv.GaussianBlur(gray, (radius, radius), 0)
        (minVal, maxVal, minLoc, maxLoc) = cv.minMaxLoc(gray)
        image = orig.copy()
        cv.circle(image, maxLoc, radius, (255, 0, 0), 2)

        points.append(Point(maxLoc[0], maxLoc[1]))

        # display the results of our newly improved method
        cv.imshow("Robust", image)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    else:
        break

cap.release()
#cv.destroyAllWindows()

max_diff = 2
similar_points = []
for point in points:
    if len(similar_points) > 0:
        last_point = similar_points[-1][-1]
        if point.matches(last_point):
            similar_points[-1].append(point)
        else:
            similar_points.append([point])
    else:
        similar_points.append([point])

filtered_points = []
for i, pts in enumerate(similar_points):
    if len(pts) > 9:
        filtered_points.append(pts)

template_image = cv.imread("HexPixels_template3.tif", 1)

font                   = cv.FONT_HERSHEY_SIMPLEX
fontScale              = 0.5
fontColor              = (255,255,255)
lineType               = 1
for i, pts in enumerate(filtered_points):
    pt = pts[0]
    cv.circle(template_image, (pt.x, pt.y), radius, (255, 255, 255), 3)

    # text = str(i%30)
    # text_width, text_height = cv.getTextSize(text, font, fontScale, lineType)[0]
    # adj_x  = int(text_width/2)
    # adj_y = int(text_height/2)
    # cv.putText(template_image,text, 
    #             (pt.x-adj_x, pt.y+adj_y), 
    #             font, 
    #             fontScale,
    #             fontColor,
    #             lineType)

cv.imshow("Result", template_image)
cv.imwrite("HexPixels_blueprint.png", template_image)

cv.waitKey(0)
cv.destroyAllWindows()

for i, pts in enumerate(filtered_points):
    print("{0}: {1}".format(i, len(pts)))

f = open("calibration.dat", "w")
for i, pts in enumerate(filtered_points):
    f.write("{0}:{1}\n".format(i, pts[0]))
f.close()
