import cv2
import sys

def rescale_frame(frame, factor = 1.75):
    width = int(frame.shape[1] * factor)
    height = int(frame.shape[0] * factor)
    return cv2.resize(frame, (width, height), interpolation = cv2.INTER_AREA)

# Get user supplied values
#imagePath = sys.argv[1]
#cascPath = "haarcascade_frontalface_default.xml"
cascPath = "fml.xml"
cascPath2 = "eyesblyat.xml"

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)
eyesCascade = cv2.CascadeClassifier(cascPath2)

videoCapture = cv2.VideoCapture(0)
videoCapture.set(3, 640)
videoCapture.set(4, 480)

while True:

    # Read the frame:
    ret, frame = videoCapture.read()
    #frame = rescale_frame(frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray);

    # Detect faces in frame
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
        #flags = cv2.CV_HAAR_SCALE_IMAGE
    )

    print("Found {0} faces!".format(len(faces)))

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        #Crop faces to recognize eyes
        cropFace = frame[y:y+h, x:x+w]
        grayEyes = cv2.cvtColor(cropFace, cv2.COLOR_BGR2GRAY)
        grayEyes = cv2.equalizeHist(grayEyes);
        eyes = eyesCascade.detectMultiScale(
            grayEyes,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        for (x1, y1, w1, h1) in eyes:
            cv2.rectangle(frame, (x + x1, y + y1), (x + x1 + w1, y + y1 + h1), (255, 0, 0), 2)

    cv2.imshow("fuck shit", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
videoCapture.release()
cv2.destroyAllWindows()
