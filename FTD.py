"""
	Part 2: Format Training Data
"""
from Tkinter import *

#SETTINGS
WIDTH, HEIGHT = 100, 100
RD_WIDTH, RD_HEIGHT = 10,10
BACKGROUND_COLOR = "#ffffff"

#set up
window = Tk()
window.configure(background=BACKGROUND_COLOR)
window.title("Format Training Data")

canvas = Canvas(window, width=WIDTH*2, height=HEIGHT, bg=BACKGROUND_COLOR, highlightthickness=0)

#text
text = Label(window, text="Test Neural Network")
text.configure(background=BACKGROUND_COLOR)
text.pack()

#set up canvas
canvas.pack()

#functions
def format_training_data():
	print "format training data"

#Buttons
format = Button(window, text="format training data", command=format_training_data)
format.pack()


img = PhotoImage(width=WIDTH, height=HEIGHT)

"""
			file and directory names
"""
#project path							###TMP*** not really###***
#path = '/home/Desktop/NN/kanji_brain/original_photos/'
#'.' = relitive ath

#training data generated file
GEN_TRAINING_FILE_NAME = "pixel_array_data.txt";	#should have to name yourself

#orginal photos directory name
ORIGINALS_DIR_NAME = "original_photos_3";

#error checking directory name
ECHECKING_DIR_NAME = "error_ckecking";

import os, sys
from PIL import Image

class Data_Photo:
    """convert photos to correct format"""

    def __init__(self, file_name, file_path):
    	""" constructor """

    	self.file_path = file_path
    	self.full_file_name = file_name

    	#extract title, page#, box#
    	title_and_page = file_name.split('_')

    	self.title = title_and_page[0]
    	self.page_num = title_and_page[-1]

    	#create formatted version: cropped, correct size, max contrast
    	image = Image.open(self.file_path)

    	box_array_test = break_up_photo(img)

    	#test crop image function
    	for i in range(0, size(box_array_test)):
    		box_array_test.get(i).show()

def break_up_photo(img):
	""" break up large orginal photo into individual boxes """

	#crop each	(9 rows, 7 cols)
	w,h,left,top = 215,220,10,15
	self.boxes = []

	for i in range(0,63):
		#left,top,right,bottom
		cropped_img = image.crop((left, top, left + w, top + h))
		self.boxes.append(cropped_img)

		top += h
		    
		if i%9 == 0:
			left += w
    
	return boxes


#loop through files in orginal dir path 
def import_originals():
	#originals
	originals = []

	#open files in directory
	path = ORIGINALS_DIR_NAME + '/'
	dir = os.listdir( path )

	#get excepted photos from original photos folder
	excepted_types = ['jpg','pdf', 'png']

	#create original file object and add to list
	for fn in dir:
		file_and_extension = fn.split('.')
		file = file_and_extension[0]
		filetype = file_and_extension[1].lower()

		if filetype in excepted_types:
			full_path = path + fn
			originals.append(Data_Photo(file, full_path))


#run import
import_originals()

#start
mainloop()