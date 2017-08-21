from Tkinter import *
import math
import random

"""
    note:
                -display output
                -incoorporate cropping and error checking process
                -display nueral network sucess rate on data set
                -display stats and configs

    process:

        off program:
            -print out template and upload folder storing with correct name after cropping
        run program:
            -program crops, ups contrast, and reduces scale to specified value
                -displays all cropped images
            -delete unwanted photos in error checking folder then press continue to generate training data off data set
            -fiddle with training settings (what portion is test data, how many iterations, how many hidden layers, how many nuerons)
            -train
            -score of accuracy
            -test nueral network with ink
                -percentages of likleness

            (save nerual netork?)

            PART 1: BUILD DATASET       (crop, upload in correct format/folder)
            PART 2: BUILD TRAINING DATA (crops, binary values, reduce scale of images)
                    PART 2b: please delete all unusable data from error checking folder
                    click => BUILD TRAINING DATA
            PART 3: TEST NEURAL NETWORK

"""



#SETTINGS
WIDTH, HEIGHT = 100, 100
RD_WIDTH, RD_HEIGHT = 10,10
BACKGROUND_COLOR = "#ffffff"
CANVAS_IMG_COLOR = "#000000"
#CANVAS_IMG_BORDER_COLOR  = "#000000"
MACHINE_IMG_CANVAS_COLOR = "#000077"
MACHINE_IMG_BRUSH_COLOR = "#770000"
BRUSH_COLOR = "#ffffff"
BRUSH_SIZE = 8
BRUSH_WEIGHT = 1
BRUSH_DENSITY = 2                       #must be low

#set up
window = Tk()
window.configure(background=BACKGROUND_COLOR)
window.title("Kanji Brain")

#canvas = Canvas(window, width=CANVAS_WIDTH*2, height=CANVAS_HEIGHT, bg=BACKGROUND_COLOR)
canvas = Canvas(window, width=WIDTH*2, height=HEIGHT, bg=BACKGROUND_COLOR, highlightthickness=0)

#text
text = Label(window, text="Test Neural Network")
text.configure(background=BACKGROUND_COLOR)
text.pack()

#canvas image display box
canvas_img = PhotoImage(width=WIDTH, height=HEIGHT)
canvas.create_image((WIDTH/2, HEIGHT/2), image=canvas_img, state="normal")
#canvas.config(highlightbackground=CANVAS_IMG_BORDER_COLOR)

#machine image display box
#machine_img = PhotoImage(width=WIDTH, height=HEIGHT)
#canvas.create_image((CANVAS_WIDTH + CANVAS_WIDTH/2, CANVAS_HEIGHT/2), image=machine_img, state="normal")
machine_img = PhotoImage(width=WIDTH, height=HEIGHT)
canvas.create_image( (WIDTH + WIDTH/2, HEIGHT/2), image=machine_img, state="normal")

#set up canvas
canvas.pack()

#text body
var = StringVar()
label = Label( window, textvariable=var, relief=RAISED)
var.set("Network Config:\n\n1 hidden layer\n100 neurons\n1000000 tirals")
label.pack()


#for smearing effect and clean brush strokes
x_buffer = -1
y_buffer = -1



"""
    note:
            create canvas state obj and chuck global variables.

                                                                """



"""
                        Functions
"""

def reset_image():
    """ Clear Entire Canvas """

    #reset canvas
    for i in range(0,WIDTH):
        for j in range(0,HEIGHT):
            canvas_img.put(CANVAS_IMG_COLOR, (i,j))

    #reset machine_img
    for i in range(0,WIDTH):
        for j in range(0,HEIGHT):
            machine_img.put(MACHINE_IMG_CANVAS_COLOR, (i,j))

def brush_up():
    """ Brush Up """

    #reset buffers
    global x_buffer
    global y_buffer

    x_buffer = -1
    y_buffer = -1

def brush_stroke(event):
    """ Draw Continuos Brush Stroke """

    global x_buffer
    global y_buffer

    x2 = event.x
    y2 = event.y

    #for brush down case
    if (x_buffer != -1) and (y_buffer != -1):

        #get coordinates
        x1 = x_buffer
        y1 = y_buffer

        #distance between points
        spacing = BRUSH_DENSITY

        """                                   
                 (x1,y1)          
                    |       .            
                    |__            .        
                    |__|__________theta_(x2,y2)
                                                         """

        #side lengths
        opp = x2-x1
        adj = y2-y1                                     
        hyp = math.sqrt( math.pow(opp,2) + math.pow(adj,2) )

        #opp/hyp = sin(theta)
        theta = math.asin(opp/hyp)

        #number of intermidate points
        num = int(hyp / spacing)
        for i in range(0,num):
            #next intermidiate point coordinates
            x = x1 + math.sin(theta) * (i) * spacing 
            y = y1 + math.cos(theta) * (i) * spacing 

            #decrease brush thickness based on speed
            radius = BRUSH_SIZE
            if i != 0:
                radius = BRUSH_SIZE - int(math.log(i))

            draw_point(x,y,radius)

    else:
        draw_point(x2,y2,BRUSH_SIZE)

    x_buffer = x2
    y_buffer = y2

def draw_point(x,y,radius):
    """ draw_brush_point """

    for i in range (0, radius):
        draw_circle(i,x,y)

def draw_circle(radius, center_x, center_y):
    """ draw circle with given points and radius """

    #increase thickness with radius
    circumference = int(2 * math.pi * radius)
    #thickness
    points = BRUSH_WEIGHT * circumference

    #don't increase thickness with weight
    #points = BRUSH_WEIGHT

    theta = 0.0
    for i in range(0,points):
        x_off = math.cos(theta) * radius
        y_off = math.sin(theta) * radius

        x = int(center_x + x_off)
        y = int(center_y + y_off)

        canvas_img.put(BRUSH_COLOR, (x,y))

        x = int(center_x - x_off)
        y = int(center_y + y_off)

        canvas_img.put(BRUSH_COLOR, (x,y))

        x = int(center_x - x_off)
        y = int(center_y - y_off)

        canvas_img.put(BRUSH_COLOR, (x,y))

        x = int(center_x + x_off)
        y = int(center_y - y_off)

        canvas_img.put(BRUSH_COLOR, (x,y))

        theta += (math.pi/2)/points

def get_pixel_array():
    """ Get Pixel Array """

    """
            when redoing:

            three parts, three functions:

                1. convert pixel matrix to binary pixel map -> value map // try own library or pythons map function
                2. reduce matrix
                3. scale matrix

                ->return image to display to canvas
    """

    """
            Retrieve pixel matrix (bitmap) from canvas_img.
            Store in 2d array canvas_img_matrix [row,col]
    """

    global canvas_img

    canvas_img_matrix = [[0 for row in range(HEIGHT)] for col in range(WIDTH)]

    for row in range(0, HEIGHT):
        for col in range(0, WIDTH):
            #pixel value
            pixel_color = canvas_img.get(col,row)   #must reverse for no transformation

            #convert to 1 or 0
            if int(pixel_color[0]) == 0:
                pixel_color = 1
            else:
                pixel_color = 0

            #add to 2d array
            canvas_img_matrix[row][col] = pixel_color


    """
        Reduce bitmap to specified dimesnions by earasing data.
        -> RD_WIDTH, RD_HEIGHT
        Store in 2d array reduced_canvas_img_matrix [row,col]
    """

    skip_width = int(WIDTH/RD_WIDTH)
    skip_height = int(HEIGHT/RD_HEIGHT)

    #reduced_canvas_img_matrix = [[0 for row in range(RD_HEIGHT)] for col in range(RD_WIDTH)]
    reduced_canvas_img_matrix = []

    for row in range(0,HEIGHT):
        if row % skip_height == 0:
            reduced_canvas_img_matrix.append(canvas_img_matrix[row][0:WIDTH:skip_width])

    """
        Scale reduced bitmap.
        Store on 2d array machine_img [row,col]             #should all rename to relevant name
        Display on machine_img_canvas.

        RD_WIDTH, RD_HEIGHT = 2,2   WIDTH, HEIGHT = 4,4
        reduced bitmap unscaled:    reduced bitmap scaled:

                |  1 0  |               |  11  00 |
                                        |  11  00 |
                |  0 1  |
                                        |  00  11 |
                                        |  00  11 |

            { WIDTH/RD_WIDTH , HEIGHT/RD_HEIGHT }
    """

    width_scale_coeffient = WIDTH/RD_WIDTH
    height_scale_coeffient = HEIGHT/RD_HEIGHT

    global machine_img

    machine_img_canvas = []

    for reduced_row in range(0,RD_HEIGHT):
        for dup_row in range(0,height_scale_coeffient):
            #make row
            new_row = []
            for reduced_col in range(0,RD_WIDTH):
                for dup_col in range(0,width_scale_coeffient):
                    new_row.append(reduced_canvas_img_matrix[reduced_row][reduced_col])
            #add row to matrix
            machine_img_canvas.append(new_row)

    #display on machine img
    for row in range(0,HEIGHT):
        for col in range(0,WIDTH):
            if machine_img_canvas[row][col] == 1:
                machine_img.put(MACHINE_IMG_CANVAS_COLOR, (col, row))        #reverse for no transformation
            else:
                machine_img.put(MACHINE_IMG_BRUSH_COLOR, (col, row))

def analyze_image():
    get_pixel_array()

""" 
                       >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>   

            >>>>>>>>>>>     Event Controller Functions      >>>>>>>>>>>

                       >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  
"""
def click_event(event):
    draw_point(event.x,event.y,BRUSH_SIZE)

def release_event(event):
    brush_up()

def hold_event(event):
    brush_stroke(event)


""" 
                            Mouse Events 
                                                                                             
                                                                            ()() 
                                                                            ('')   _
                                                                            /\/\  ( '                   
"""
#clcik
canvas.bind("<Button-1>", click_event)
#hold
canvas.bind("<B1-Motion>", hold_event)
#release
canvas.bind("<ButtonRelease-1>", release_event)


""" 
                            Buttons 
"""

#analyze
#analyze = Button(window, text="analyze", command=analyze_image, highlightthickness=0,bg="blue")
#analyze.configure(background=BACKGROUND_COLOR) #highlightthickness=0 removes border
#analyze.configure(bg = '#FF00FF')
#analyze.grid(row = 0, column = 0)
analyze = Button(window, text="analyze", command=analyze_image)
analyze.pack()

#clear
clear = Button(window, text="clear", command=reset_image)
#clear.configure(background=BACKGROUND_COLOR)
clear.pack()

""" 
////////////////////////// Start //////////////////////////
"""
#set pixels
reset_image()

mainloop()

