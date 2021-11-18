import os
import time
from tkinter import *
from PIL import Image, ImageTk

rows=8      # number of rows
columns=8   # and columns of tiles

def createPuzzle (master,photoid):
    """ Create the window where the puzzle is played
    """
    global PhotoImagesBig, images, puzzlew, puzzleCv,photoImages, tiles
    try:               # destroy a previous puzzle if there was already one
        puzzlew.destroy()
    except:
        pass
    puzzlew = Toplevel(master)     # new toplevel window
    puzzlew.geometry("450x450")
    puzzlew.title("Puzzle")
    puzzleCv= Canvas(puzzlew,width=420,height=420, bg="white")  # create a canvas for the tiles
    width, height = images[photoid].size
    width //= (columns)
    height //= (rows)

    for row in range(rows):
        for col in range(columns):
#           tile = img.crop((col*width,row*height, (col+1)*width,(row+1)*height))
#            tile.show()
            imgg = tiles[(photoid,row,col)]
 #           id2 = puzzleCv.create_rectangle(row * (height + 3), col * (width + 3),row * (height + 3)+100, col * (width + 3)+100)

            id = puzzleCv.create_image(row * (height + 3), col * (width + 3),anchor="nw")
            puzzleCv.itemconfigure(id, image=imgg)
            print(id, row*(height+3),col*(width+3) )
    puzzleCv.pack()

def chooseImage(cv, photoid,counter):
    """"
    Let the user choose a picture for the puzzle a call back function to the button press
    """
    global PhotoImagesBig, cw
    img=images[counter]
    imgg = PhotoImagesBig[counter]   # update preview
    cv.itemconfigure(photoid, image=imgg)
    createPuzzle(cw,counter)         # create the puzzle window

def chooserWindow():
    """Create window for choosing the photo to do in the puzzle
    """
    global PhotoImagesBig, photoImages, images, cw, tiles

#   Read all Gif files in the give subdirectory, make them into PIL files
    images = [Image.open(os.path.join("Gif", file)) for file in os.listdir("Gif")]

#   create Tk Compatible big images and thumb nails
    cw = Tk()

    photoImages = [ImageTk.PhotoImage(img.resize((70, 70) )) for img in images]
    PhotoImagesBig = [ImageTk.PhotoImage(img) for img in images]
# create window

    cw.title("Choose a picture")
    cv = Canvas(width=400, height=400, bg='black')  # Canvas for the big preview image
    imgg = ImageTk.PhotoImage(images[0])            # Fill with first image found
    photoId = cv.create_image(0, 0, image=imgg, anchor="nw") # move it to canvas
    frame = Frame()                                 # create a frame to hold the thumbnails
    frame.pack(side=LEFT)
    i = 0
    for img in photoImages:                         # create Buttons for each available image
        b = Button(frame, text='', image=img,relief=RAISED,
                   command=lambda arg1=cv, arg2=photoId, arg3= i: chooseImage(arg1, arg2,arg3))
        b.pack(side=TOP)
        i += 1
    cv.pack(side=LEFT, anchor="ne")
    tiles = dict()
    for i in range (len(images)):
        width, height = images[i].size
        width //= (columns)
        height //= (rows)
        for row in range(rows):
            for col in range(columns):
                tiles[(i,row,col)] \
                    = ImageTk.PhotoImage(images[i].crop((row*height,col*width, (row+1)*height,(col+1)*width)))

#    cw.after(1000, lambda arg1=cw, arg2=photoId: createPuzzle(cw,0))
    cw.mainloop()

chooserWindow()
