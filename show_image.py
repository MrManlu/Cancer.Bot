import os, sys
from glob import glob
import cv2
import numpy as np

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

mask = np.zeros((50,50,3), np.uint8)
mask[:,0:50//2] = (255,0,0)      # (B, G, R)
mask[:,50//2:50] = (0,255,0)

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
maskImg = np.zeros((imgMY+50,imgMX+50,3), np.uint8)
nameImg = str(os.path.basename(filename)).split('_')[0]

for image in imgList:
	s_img = cv2.imread(image[0], -1)
	x_offset = image[1]
	y_offset = image[2]
	try:
		baseImg[y_offset:y_offset+s_img.shape[0], x_offset:x_offset+s_img.shape[1]] = s_img
		if(image[3]==0):
			maskImg[y_offset:y_offset+s_img.shape[0], x_offset:x_offset+s_img.shape[1]] = s_img
		else:
			maskImg[y_offset:y_offset+s_img.shape[0], x_offset:x_offset+s_img.shape[1]] = mask

	except ValueError:
		print(str(os.path.basename(image[0])) + "\t\tIN: " + str(s_img.shape) + "\tEXP: "+ str(baseImg.shape))

cv2.imwrite(nameImg + ".jpg", baseImg);
cv2.imwrite(nameImg + "-masked.jpg", maskImg);
cv2.imshow('image',baseImg)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imshow('image',maskImg)
cv2.waitKey(0)

cv2.destroyAllWindows()


