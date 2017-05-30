import os, os.path

KAFKA_HOST= os.environ['KAFKA_HOST'] + ':9092'
CLASSIFIER_FILE="haarcascade_frontalface_default.xml"
SCALE_FACTOR=1.1
MIN_NEIGHBORS=5
MIN_WIDTH=140
MIN_HEIGHT=180
HEIGHT=112
WIDTH=92
IMG_RES=WIDTH * HEIGHT
RATIO=WIDTH/HEIGHT
TEST_DIR='../media/test_faces/'
TRAIN_DIR='../media/train_faces/'
TEST_FACES='../media/test_faces/*'
TRAIN_FACES='../media/train_faces/*'
THRESHOLD=1.5

teammates=[name for name in os.listdir(TRAIN_DIR) if os.path.isdir(TRAIN_DIR + name)]
NUM_TEAMMATES=len(teammates)

counts = []
for name in teammates:
	path=TRAIN_DIR+name+"/"
	counts.append(len(os.listdir(path)))

MIN_IMAGES_PER_TEAMMATE=min(counts)

NUM_EIGENFACES=MIN_IMAGES_PER_TEAMMATE
NUM_TRAINIMAGES=MIN_IMAGES_PER_TEAMMATE * NUM_TEAMMATES