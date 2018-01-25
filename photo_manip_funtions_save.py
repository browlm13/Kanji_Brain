	def binary_contrast(img):
		""" make image black and white and remove red """

	    rgb_im = img.convert('RGB')
	    height, width = img.size()

	    for row in range(0, height):
	    	for col in range(0, width):
				r, g, b = rgb_im.getpixel((row, col))
								    """
			    current_color = picture.getpixel( (x,y) )
		        ####################################################################
		        # Do your logic here and create a new (R,G,B) tuple called new_color
		        ####################################################################
		        picture.putpixel( (x,y), new_color)
		        """

				if (r + g + b) > (255*1.5):
				    print r, g, b