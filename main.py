import os
import time
from tkinter import *
from PIL import Image, ImageTk
import random

rows = 4  # number of rows
columns = 4  # and columns of tiles


def exchangeTile(clickedField, emptyField):
    """
    exchange two tilew
    :param clickedField:   2-tuple with row and column of tile clicked
    :param emptyField:        "                           empty tile
    :return:   nothing
    """
    global puzzleCv
    (clickedRow, clickedColumn) = clickedField  # extract column and row of source and destination field
    (emptyRow, emptyColumn) = emptyField
    #   get the Tk Photo images
    emptyImage = puzzleCv.itemcget(str(emptyRow) + ":" + str(emptyColumn), "image")
    clickedImage = puzzleCv.itemcget(str(clickedRow) + ":" + str(clickedColumn), "image")
    # write them back to the tiles
    puzzleCv.itemconfigure(str(emptyRow) + ":" + str(emptyColumn), image=clickedImage)
    puzzleCv.itemconfigure(str(clickedRow) + ":" + str(clickedColumn), image=emptyImage)


def clickTile(e, clickedField):
    """
    Call back when tile is clicked
    :param e:    Tk event - position
    :param clickedField:   2-tuple with row and column at which the user clicked
    :return:
    """
    global emptyField
    (er, ec) = emptyField
    (cr, cc) = clickedField
    # check wheter click was next to empty click
    if abs(er - cr) + abs(ec - cc) == 1:
        # exchange the photo tiles
        exchangeTile(clickedField, emptyField)
        emptyField = clickedField
    """
    elif er == cr:
        pass
        while ec > cc:
            exchangeTile((er, ec), (cr, cc))
            ec -= 1
        while ec < cc:
            exchangeTile((er, ec), (cr, cc))
            ec += 1
        emptyField = (cr, cc)
    """

def shufflePuzzle():
    """ shuffle the board randomly """
    for i in range(10000):
        row = random.randint(0, rows - 1)
        col = random.randint(0, columns - 1)
        Field = (row, col)
        clickTile(None, Field)


def createPuzzleWindow(master, photoid):
    """ Create the window where the puzzle is played
        :param master: is window of parent
        :param photoid:   is index pf present photo
    """
    global PhotoImagesBig, images, puzzlew, puzzleCv, photoImages, tiles, emptyField
    emptyField = (rows - 1, columns - 1)

    try:  # destroy a previous puzzle if there was already one
        puzzlew.destroy()
    except:
        pass
    puzzlew = Toplevel(master)  # new toplevel window
    puzzlew.geometry("450x450")
    puzzlew.title("Puzzle")
    puzzleCv = Canvas(puzzlew, width=420, height=420, bg="white")  # create a canvas for the tiles
    width, height = images[photoid].size
    width //= (columns)  # width and height of single tile
    height //= (rows)
    tile = dict()
    for row in range(rows):
        for col in range(columns):
            imgg = tiles[(photoid, row, col)]
            id = puzzleCv.create_image(row * (height + 1), col * (width + 1), image=imgg, anchor="nw")
            puzzleCv.tag_bind(id, "<ButtonPress-1>",
                              lambda e, arg2=(row, col): clickTile(e, arg2))
            puzzleCv.itemconfigure(id, tag=str(row) + ":" + str(col))  # tag to be used to access image

    puzzleCv.pack()
    Button(puzzlew, text="shuffle", command=shufflePuzzle).pack()


def chooseImage(cv, photoid, counter):
    """"
    Let the user choose a picture for the puzzle a call back function to the button press
    """
    global PhotoImagesBig, cw, divisions, tiles, rows, columns
    img = images[counter]
    imgg = PhotoImagesBig[counter]  # update preview
    cv.itemconfigure(photoid, image=PhotoImagesBig[counter])
    rows = divisions.get()
    columns = divisions.get()
    tiles = dict()
    for i in range(len(images)):
        width, height = images[i].size
        width //= (columns)
        height //= (rows)
        for row in range(rows):
            for col in range(columns):
                tiles[(i, row, col)] \
                    = ImageTk.PhotoImage(
                    images[i].crop((row * height, col * width, (row + 1) * height, (col + 1) * width)))
        (row, col) = (rows - 1, columns - 1)
        tiles[(i, row, col)] = ImageTk.PhotoImage('RGB', (width, height))
    print(rows, columns)
    createPuzzleWindow(cw, counter)  # create the puzzle window


def chooserWindow():
    """Create window for choosing the photo to do in the puzzle
    """
    global PhotoImagesBig, photoImages, images, cw, tiles, divisions
    #   Read all Gif files in the give subdirectory, make them into PIL files
    images = [Image.open(os.path.join("Gif", file)) for file in os.listdir("Gif")]

    #   create Tk Compatible big images and thumb nails
    cw = Tk()
    photoImages = [ImageTk.PhotoImage(img.resize((70, 70))) for img in images]
    PhotoImagesBig = [ImageTk.PhotoImage(img) for img in images]
    # create window
    divisions = IntVar()
    scale = Scale(cw, variable=divisions, from_=2, to=8, orient=HORIZONTAL, label="Difficulty")
    divisions.set(rows)
    cw.title("Choose a picture")
    cv = Canvas(width=420, height=420, bg='black')  # Canvas for the big preview image
    imgg = ImageTk.PhotoImage(images[0])  # Fill with first image found
    photoId = cv.create_image(0, 0, image=imgg, anchor="nw")  # move it to canvas
    frame = Frame()  # create a frame to hold the thumbnails
    frame.pack(side=LEFT)
    i = 0
    for img in photoImages:  # create Buttons for each available image
        b = Button(frame, text='', image=img, relief=RAISED,
                   command=lambda arg1=cv, arg2=photoId, arg3=i: chooseImage(arg1, arg2, arg3))
        b.pack(side=TOP)
        i += 1
    cv.pack(side=TOP, anchor="ne")
    scale.pack(anchor=CENTER)
    # for each photo create the small tiles in with references in the tile dictionary
    cw.mainloop()
chooserWindow()
