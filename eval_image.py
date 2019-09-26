#from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import img_to_array
from keras.callbacks import LearningRateScheduler
from keras.optimizers import Adagrad
from keras.utils import np_utils
from keras.models import load_model
from keras.preprocessing.image import load_img
from pyimagesearch.cancernet import CancerNet
from pyimagesearch import config
from imutils import paths
import matplotlib.pyplot as plt
import numpy as np
import argparse
import os, sys
from glob import glob
import cv2
import numpy as np

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

BS = 32
threshold = 0.85

model = load_model("./models/CancerNet.38-0.86.hdf5")

if (len(sys.argv) != 2):
	print("Directory name is required!")
	sys.exit()

inputFolder = str(sys.argv[1])

if os.path.exists(inputFolder) and os.path.isfile(inputFolder):
	print("Directory is required! Got file, but directory was expected.")
	sys.exit()

print("Directory exist! Processing... ")

images=glob(inputFolder + '**/*.png',recursive=True)
imgList = []
imgMX = 0
imgMY = 0

trueMask = np.zeros((50,50,3), np.uint8)
trueMask[:,0:50//2] = (255,0,0)      # (B, G, R)
trueMask[:,50//2:50] = (0,255,0)

predMask = np.zeros((50,50,3), np.uint8)
predMask[:,0:50//2] = (142,9,75)      # (B, G, R)
predMask[:,50//2:50] = (0,255,0)


for fileindex,filename in enumerate(images):
	#if fileindex==10:
	#    break
	x = int(str(os.path.basename(filename)).split('_')[2][1:])
	y = int(str(os.path.basename(filename)).split('_')[3][1:])
	c = int(str(os.path.basename(filename)).split('_')[4][5])
	#print(filename + '\t' + str(x) + '\t' + str(y) + '\t' + str(c))
	if (x>imgMX): imgMX = x
	if (y>imgMY): imgMY = y
	imgList.append([filename,x,y,c])

#print("Max X= " + str(imgMX) + "\tMax Y= " + str(imgMY))
baseImg = np.zeros((imgMY+50,imgMX+50,3), np.uint8)
trueImg = np.zeros((imgMY+50,imgMX+50,3), np.uint8)
predImg = np.zeros((imgMY+50,imgMX+50,3), np.uint8)
prthImg = np.zeros((imgMY+50,imgMX+50,3), np.uint8)

baseImg[:,:] = (225,215,227)
trueImg[:,:] = (225,215,227)
predImg[:,:] = (225,215,227)
prthImg[:,:] = (225,215,227)

nameImg = str(os.path.basename(filename)).split('_')[0]

for image in imgList:
	s_img = cv2.imread(image[0], -1)
	pred_img = cv2.cvtColor(s_img, cv2.COLOR_BGR2RGB)
	pred_img = cv2.resize(pred_img, (48, 48))
	pred_img = pred_img.astype("float") / 255.0
	pred_img = img_to_array(pred_img)
	pred_img = np.expand_dims(pred_img, axis=0)
	#pred_img = np.expand_dims(s_img[2:,2:], 0)
	x_o = image[1]
	y_o = image[2]
	prediction = model.predict(np.array(pred_img),batch_size = BS)

	#print(image[0] + '\t\t' + str(prediction[0][1]))
	try:
		baseImg[y_o:y_o+s_img.shape[0], x_o:x_o+s_img.shape[1]] = s_img
		if(image[3]==0):
			trueImg[y_o:y_o+s_img.shape[0], x_o:x_o+s_img.shape[1]] = s_img
		else:
			trueImg[y_o:y_o+s_img.shape[0], x_o:x_o+s_img.shape[1]] = trueMask

		predImg[y_o:y_o+s_img.shape[0], x_o:x_o+s_img.shape[1]] = prediction[0][0] * s_img + prediction[0][1] * predMask

		if(prediction[0][1] > threshold):
			prthImg[y_o:y_o+s_img.shape[0], x_o:x_o+s_img.shape[1]] = prediction[0][0] * s_img + prediction[0][1] * predMask
		else:
			prthImg[y_o:y_o+s_img.shape[0], x_o:x_o+s_img.shape[1]] = s_img

	except ValueError:
		print(str(os.path.basename(image[0])) + "\t\tIN: " + str(s_img.shape) + "\tEXP: "+ str(baseImg.shape))

cv2.imwrite(nameImg + "-orig.jpg", baseImg);
cv2.imwrite(nameImg + "-true.jpg", trueImg);
cv2.imwrite(nameImg + "-pred.jpg", predImg);
cv2.imwrite(nameImg + "-prth.jpg", prthImg);
#cv2.imshow('image',baseImg)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
#cv2.imshow('image',maskImg)
#cv2.waitKey(0)

cv2.destroyAllWindows()
