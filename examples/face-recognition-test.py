import cv2
import numpy as np
import time
import constants
from sklearn.decomposition import RandomizedPCA
import glob
import math

def crop(x, y, w, h):
    # If it's wider
    if( w/h > constants.RATIO):
        # Expand width
        extra_width = (92 * h / 112) - w
        w = w + extra_width
        x = x - (extra_width / 2)
    # If it's narrower
    else:
        # Expand height
        extra_height = (112 * w / 92) - h
        h = h + extra_height
        y = y - (extra_height / 2)
    return int(x), int(y), int(w), int(h)

def ID_from_filename(filename):
    if(filename == None):
        raise "Must specify filename"
    part = filename.split('/')
    return part[1]
 
def prepare_image(filename):
    img_color = cv2.imread(filename)
    img_gray = cv2.cvtColor(img_color, cv2.COLOR_RGB2GRAY)
    img_gray = cv2.equalizeHist(img_gray)
    return img_gray.flat

def find_person(Y, pca, X_pca):
    test_faces = glob.glob(constants.TEST_FACES)

    X = np.zeros([len(test_faces), constants.IMG_RES], dtype='int8')

    for i, face in enumerate(test_faces):
        X[i,:] = prepare_image(face)

    for j, ref_pca in enumerate(pca.transform(X)):
        distances = []

        for i, test_pca in enumerate(X_pca):
            dist = math.sqrt(sum([diff**2 for diff in (ref_pca - test_pca)]))
            print(dist, Y[i])
            distances.append((dist, Y[i]))

        eigenDistance = min(distances)[0]
        found_ID = min(distances)[1]
        print(found_ID)

        if(eigenDistance < constants.THRESHOLD):
            return str(found_ID)
        else:
            return None

cascPath = constants.CLASSIFIER_FILE
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)

X = np.zeros([constants.NUM_TRAINIMAGES, constants.IMG_RES], dtype='int8')
Y = []

folders = glob.glob(constants.TRAIN_FACES)

c = 0
for x, folder in enumerate(folders):
    train_faces = glob.glob(folder + '/*')[0:constants.NUM_EIGENFACES]
    for i, face in enumerate(train_faces):
        X[c,:] = prepare_image(face)
        Y.append(ID_from_filename(face))
        c = c + 1

pca = RandomizedPCA(n_components=constants.NUM_EIGENFACES, whiten=True).fit(X)
X_pca = pca.transform(X)

person = None
while person == None:

    faces = []
    while len(faces) < 1:
    	ret, frame = video_capture.read()
    	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    	faces = faceCascade.detectMultiScale(
    		gray,
    		scaleFactor=constants.SCALE_FACTOR,
    		minNeighbors=constants.MIN_NEIGHBORS,
    		minSize=(constants.MIN_WIDTH, constants.MIN_HEIGHT),
    		flags=cv2.CASCADE_SCALE_IMAGE
    	)

    for (x, y, w, h) in faces:
        x, y, w, h = crop(x, y, w, h)
        face = frame[y:y+h, x:x+w]
        resized = cv2.resize(face, (92, 112))
        grayscale = cv2.cvtColor(resized, cv2.COLOR_RGB2GRAY)
        cv2.imwrite('test_faces/last_grayscale.png', grayscale)
        person = find_person(Y, pca, X_pca)
        print(person)

video_capture.release()
