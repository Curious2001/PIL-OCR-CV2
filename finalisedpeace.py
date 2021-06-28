def main():
	from zipfile import ZipFile
	wanted_name = "Mark"
	import PIL
	#import os
	#os.chdir('readme')
	from PIL import Image
	zipname = "readonly/images.zip"		#------Here you can place any zipfile you want.------#
	ZipFile(zipname,"r").extractall()
	zipcontentlist = ZipFile(zipname,"r").namelist() #realnamelist(zipname)
	#print(zipcontentlist)
	for i in range(len(zipcontentlist)):
		imgnow = Image.open(zipcontentlist[i])
		imgray = imgnow.convert("L")
		imcolr = imgnow.convert("RGB")
		wordcheck = wordsearch(imgray, wanted_name)
		if wordcheck != 0:
			print("Results found in file "+zipcontentlist[i])
			imglist = facefind(zipcontentlist[i])
			if len(imglist) == 0:
				print("But there were no faces in that file!")
			else:
				contactsheet = contactsheetmaker(imglist)
				display(contactsheet)   
            
#```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````#
#This function might be required in some environments.
#...........................................................................................................................#
def realnamelist(zipname):
	from zipfile import ZipFile
	current_list = ZipFile(zipname,"r").namelist()
	newnamelist = []
	for i in range(len(current_list)):
		namep = current_list[i][len(zipname)-3:]
		newnamelist.append(namep)
	return newnamelist
#```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````#
#The function facefindarray() takes image(as numpy array) as input and gives face location(co-ordinates as a list) as output.
#...........................................................................................................................#
def facefindarray(img_file):
	import cv2 as cv
	img        = cv.imread(img_file)
	face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')
	eye_cascade = cv.CascadeClassifier('readonly/haarcascade_eye.xml')
	img_array_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	#img_array_gray=cv.threshold(img_array_gray,120,255,cv.THRESH_BINARY)[1]
	faces   = face_cascade.detectMultiScale(img_array_gray,scaleFactor=1.35,minNeighbors=4, minSize=(30,30))
	#faces = face_cascade.detectMultiScale(img_array_gray, 1.35)#1.46 > value > 1.45; 1.455,
	faces = list(faces)
	return faces
########################################################################################################################
#The function wordsearch() takes in a PIL image and the wanted word(as a string) an input & searches whether the wanted
#word is in it or not.
#If the word is found, it returns 1 else 0.
########################################################################################################################
def wordsearch(gray_img, word):
	from pytesseract import image_to_string
	txt = image_to_string(gray_img)
	wordlist = txt.split()
	if word.isupper():
		word = word.swapcase()
	word_diff_case_init = word[0].swapcase()+word[2:]
	word_diff_case_whole = word.swapcase()
	word_apo_s = word+'\'s'
	case = wordlist.__contains__(word) or wordlist.__contains__(word_diff_case_init) or wordlist.__contains__(word_diff_case_whole)
	case = case or wordlist.__contains__(word_dcase_in_apos) or wordlist.__contains__(word_dcase_wh_apos)
	case = case or wordlist.__contains__(word_apo_s)
	return int(case)
########################################################################################################################
#The function facefind() takes image(PIL format) of pages as input & gives a list of PIL images of found "faces" as O/P.
########################################################################################################################
def facefind(img_file_name):
	from PIL import Image
	import numpy as np
	pageimg = Image.open(img_file_name)
	pageimg = pageimg.convert("RGB")					#converting the image into RGB format
	pageimg_gray = pageimg.convert("L")
	photolocationlist = facefindarray(img_file_name)			#getting the list of faces' locations
	imglist = []
	for i in range(len(photolocationlist)):
		faceloc = photolocationlist[i]
		theface = pageimg.crop((faceloc[0], faceloc[1], faceloc[0]+faceloc[2], faceloc[1]+faceloc[3]))
		#r = Image.fromarray(theface)				#converting
		imglist.append(theface)
	return imglist
########################################################################################################################
#The function contactsheetmaker() takes image(s) as input and returns a contact sheet made of them as output.
#Here each photo is alloted 100*100 pixels. If it doesn't cover that area rest remains blank.
#I did this to get similar output as our beloved instructor.
########################################################################################################################
def contactsheetmaker(imgfaces):
	import PIL
	import math
	from PIL import Image
	no_of_rows = math.ceil(len(imgfaces)/5)
	contact_sheet=PIL.Image.new(imgfaces[0].mode, (100*5,100*no_of_rows))
	x=0
	y=0
	for i in range(len(imgfaces)):
		dimension = imgfaces[i].size
		#if height/width of any selected face image is higher than 100px, it will be resized to 100*100
		if dimension[0]>100 or dimension[1]>100:
			imgfaces[i] = imgfaces[i].resize((100,100))
		contact_sheet.paste(imgfaces[i],(x,y))
		# Now we update our X position. If it is going to be the width of the image, then we set it to 0
		# and update Y as well to point to the next "line" of the contact sheet.
		if x+100 == 500:
			x=0
			y=y+100
		else:
			x = x+100
	return contact_sheet
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
let's start
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
main()

