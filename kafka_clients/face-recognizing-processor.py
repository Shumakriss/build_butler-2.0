from kafka import KafkaConsumer, KafkaProducer
import cv2
import numpy as np
import time
import constants
from sklearn.decomposition import RandomizedPCA
import glob
import math

def prepare_image(filename):
    img_color = cv2.imread(filename)
    img_gray = cv2.cvtColor(img_color, cv2.COLOR_RGB2GRAY)
    img_gray = cv2.equalizeHist(img_gray)
    return img_gray.flat

def ID_from_filename(filename):
    if(filename == None):
        raise "Must specify filename"
    part = filename.split('/')
    return part[1]

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

consumer = KafkaConsumer('formatted-faces', bootstrap_servers=constants.KAFKA_HOST)
producer = KafkaProducer(bootstrap_servers=constants.KAFKA_HOST)

for msg in consumer:
	nparr = np.fromstring(msg.value, np.uint8)
	img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

	test_faces = glob.glob(constants.TEST_FACES)

	X = np.zeros([len(test_faces), constants.IMG_RES], dtype='int8')

	for i, face in enumerate(test_faces):
		img_gray = cv2.equalizeHist(img)
		X[i,:] = img_gray.flat

	for j, ref_pca in enumerate(pca.transform(X)):
		distances = []

		for i, test_pca in enumerate(X_pca):
			dist = math.sqrt(sum([diff**2 for diff in (ref_pca - test_pca)]))
			distances.append((dist, Y[i]))

		eigenDistance = min(distances)[0]
		found_ID = min(distances)[1]
	if(eigenDistance < 1.5):
		producer.send('names', bytes(found_ID, 'utf-8'))