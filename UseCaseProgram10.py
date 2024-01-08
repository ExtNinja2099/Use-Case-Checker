import cv2 as cv
import numpy as np
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import font
from PIL import ImageTk, Image
import torch
import os

class UseCaseProgram:
    def openAIModel(self, modelPath, modelList):
        # Opens a file dialog window to let user choose model weight in .pb format
        fileDir = filedialog.askopenfilename(initialdir='/runs', title="Select A Model File", filetypes=[("pt file","*.pt"), ("All files",".*")])
        # Adds the file to the filePath list
        modelPath.append(fileDir)
        # If the ModelPath is not empty
        if len(modelPath) > 0:
            # Replaces backslash with forward slash
            newfileDir = fileDir.replace(os.sep,'/')
            # Adds formatted file directory to model list
            modelList.append(newfileDir)

    def useModel(self, modelPath, modelDir, imgPath):
        # If the modelPath is not empty
        if len(modelPath) > 0:
            # Gets current working directory
            cwd = os.getcwd()
            # Replaces backslash with forward slash
            cwd = cwd.replace(os.sep, '/')
            # Prints cwd in new format to check
            print("cwd: " + cwd)
            # Gets the specific directory of the model file
            newDir = modelDir[len(cwd)+1:len(modelDir)]
            # Prints result
            print("modelDir - cwd: " + newDir)
            # Loads the model using torch.hub.load() function
            model = torch.hub.load(cwd, 'custom', path=newDir, source='local', force_reload=True)
            # Runs the model with the chosen image using the directory of the image
            result = model(imgPath)
            # Prints result from the model
            result.print()
            # Converts result to numpy array
            img = np.squeeze(result.render())
            # Return array for image to be displayed
            return img

class GUI:
    def openFile(self, filePath, panel, winW, winH, displayedImg):
        # Opens a file dialog window to let user choose image file
        fileDir = filedialog.askopenfilename(initialdir='/Pictures', title="Select A Diagram File")
        # Adds the file to the filePath list
        filePath.append(fileDir)
        #If the filePath is not empty
        if len(filePath) > 0:
            # Display image on the panel label
            self.displayImage(filePath, panel, winW, winH, displayedImg)

    def saveToFile(self, displayedImg):
        # If the displayed images list is not empty
        if len(displayedImg) > 0:
            # Get the recent displayed image on the panel label
            tempImg = displayedImg[len(displayedImg) - 1]
            # Open a dialog window to let user choose where to save and name the file
            filename = filedialog.asksaveasfile(initialdir='/Pictures', title="Save Diagram As", defaultextension='*.png', filetypes=[("PNG file","*.png"), ("JPEG file","*.jpg"),("All files",".*")])
            # Convert _io.TextIOWrapper object to a string
            tempstr = str(filename)
            # Find the chosen directory and filename
            endOfDir = len(tempstr)-29
            fileDir = tempstr[25:endOfDir]
            print(fileDir)
            # tempImg.save(fileDir)
            # Write the file using cv.imwrite function
            cv.imwrite(fileDir, tempImg)

    def displayImage(self, directory, panel, imgW, imgH, displayedImg):
        # If the filepath is not empty
        if len(directory) > 0:
            # Get the recent chosen image
            img = Image.open(directory[len(directory) - 1])
            # Convert to Photoimage object
            tempImg = ImageTk.PhotoImage(img)
            # Get height and width of image
            h = tempImg.height()
            w = tempImg.width()
            # Resize the original image size to fit within panel label
            if h > w:
                newImg = img.resize((imgW - 50, imgH - 50), Image.ANTIALIAS)
            else:
                newImg = img.resize((imgW - 100, imgH - 50), Image.ANTIALIAS)
            # Store original image size to displayedImg list
            displayedImg.append(img)
            # Convert image with new size to photoImage
            displayImg = ImageTk.PhotoImage(newImg)
            # Display the image on the panel frame
            panel.configure(image=displayImg)
            panel.image = displayImg

    def displayProcessedImg(self, img, panel, imgW, imgH, displayedImg):
        #Convert the image file to RGB
        temp1 = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        temp2 = Image.fromarray(temp1)
        # Convert to Photoimage object
        tempImg = ImageTk.PhotoImage(temp2)
        # Get height and width of image
        h = tempImg.height()
        w = tempImg.width()
        # Resize the original image size to fit within panel label
        if h > w:
            newImg = temp2.resize((imgW - 50, imgH - 50), Image.ANTIALIAS)
        else:
            newImg = temp2.resize((imgW - 100, imgH - 50), Image.ANTIALIAS)
        # Store original image size to displayedImg list
        displayedImg.append(img)
        # Convert image with new size to photoImage
        displayImg = ImageTk.PhotoImage(newImg)
        # Display the image on the panel label
        panel.configure(image=displayImg)
        panel.image = displayImg

    def processImage(self, directory, modelPath, modelList, program, panel, image, imgW, imgH, displayedImg):
        # If the directory is not empty
        if len(directory) > 0:
            # Old code to detect shapes and text
            """
            # Get the recent chosen image
            img = cv.imread(directory[len(directory) - 1])
            # Store image to image list
            image.append(img)
            # Initialising a variable to be a copy of the image
            imgCont = img.copy()
            # Store image to imgContour list
            imgContour.append(imgCont)
            # Convert the most recent image in image list to grayscale
            grayScale = cv.cvtColor(image[len(image)-1], cv.COLOR_BGR2GRAY)
            # Blur the grayscale image
            blurred = cv.blur(grayScale, (3, 3))
            # Use canny function on blurred image
            Canny = cv.Canny(blurred, 100, 100*2)
            # Use the getContours function on the canny image and most recent image in contour list
            #program.getContours(Canny, imgContour[len(imgContour)-1])
            """
            # If the modelPath is also not empty
            if len(modelPath) > 0:
                # use Ai with the modelPath, directory of the chosen model and the directory of the image
                newimg = program.useModel(modelPath, modelList[len(modelList) - 1], directory[len(directory) - 1])
                # Add new image to image list
                image.append(newimg)
                # Display the image onto the panel
                self.displayProcessedImg(image[len(image)-1], panel, imgW, imgH, displayedImg)
            # To detect only digits not words
            # conf1 = r'--oem 3 --psm 6 outputbase digits'
            # To use the conf1
            # boxes = pytesseract.image_to_boxes(img, config=conf1)
            # Detect_Characters(newImg)

    def refreshGUI(self, window, menu, frameList, modelPath, modelList, displayedImg, filePath, image, Program, winW, winH):
        # Get new window width and height
        newWidth = window.winfo_width()
        newHeight = window.winfo_height()
        # Set window to new width and height
        window.geometry(f"{newWidth}x{newHeight}")
        # Add new width and height to lists
        winW.append(newWidth)
        winH.append(newHeight)
        # Delete frames in window
        frameList[len(frameList) - 2].destroy()
        frameList[len(frameList) - 1].destroy()
        # Create a new GUI according to the new window width and height
        self.init_GUI(window, menu, frameList, modelPath, modelList, displayedImg, filePath, image, Program, winW, winH)

    def init(self, filePath, image, Program, width, height):
        # Window variable
        window = Tk()
        # Window Title
        window.title('Use Case Diagram Checker')
        # Setting window width and height
        window.geometry(width + "x" + height)
        # Make the window resizeable
        window.resizable(True, True)
        # Menu initialisation
        menu = Menu(window)
        window.config(menu=menu)
        # Storage for holding the images displayed on the panel label
        displayedImg = list(())
        frameList = list(())
        # Storage for holding AI Models
        modelPath = list(())
        modelList = list(())
        # Window width and height values as integers
        winW = list(())
        winH = list(())
        winW.append(int(width))
        winH.append(int(height))
        self.init_GUI(window, menu, frameList, modelPath, modelList,  displayedImg, filePath, image, Program, winW, winH)
        # Making a size grip at the right bottom corner of the window
        # Showing the user the window is resizeable
        sizeGrip = ttk.Sizegrip(window)
        sizeGrip.pack(side="right", anchor=SE)
        window.mainloop()

    def init_GUI(self, window, menu, frameList, modelPath, modelList, displayedImg, filePath, image, Program, winW, winH):
        # Maximum font size for frames and larger elements
        # Font value depends on window width
        maxFontSize = (winW[len(winW) - 1])//30
        # Basic font size for buttons and smaller elements
        normalFont = font.Font(family='Helvetica', size=10)
        # If the maximum font size reaches a large value
        if maxFontSize > 40:
            maxFont = font.Font(family='Helvetica', size=25)
        else:
            maxFont = font.Font(family='Helvetica', size=maxFontSize)
        # Width and height of frames
        frameWidth = (winW[len(winW) - 1])-50
        frameHeight = (winH[len(winH) - 1])-100
        # Width of buttons
        buttonWidth = frameWidth//30
        # Diagram frame
        frame = LabelFrame(window, text="Diagram", font= maxFont, width=frameWidth, height=frameHeight, padx=10, pady=10)
        frame.pack()
        frame.pack_propagate(0)
        # Panel label to hold and display images
        panel = Label(frame)
        panel.pack()
        # Button frame
        frame2 = LabelFrame(window, text="Functions", font= maxFont, width=frameWidth, height=frameHeight//90, padx=10, pady=10)
        frame2.pack()
        frame2.pack_propagate(0)
        # Open File button
        button0 = Button(frame2, text='Open File', font= normalFont, width=buttonWidth, command= lambda: self.openFile(filePath, panel, (winW[len(winW) - 1]) - 50, (winH[len(winH) - 1]) - 80, displayedImg))
        button0.grid(row=0, column=0, sticky="nsew")
        # Check Diagram button
        button1 = Button(frame2, text='Check Diagram', font= normalFont, width=buttonWidth, command=lambda: self.processImage(filePath, modelPath, modelList, Program, panel, image, (winW[len(winW) - 1]) - 50, (winH[len(winH) - 1]) - 80, displayedImg))
        button1.grid(row=0,column=1, sticky="nsew")
        # Save Diagram button
        button2 = Button(frame2, text='Save Diagram', font= normalFont, width=buttonWidth, command=lambda: self.saveToFile(displayedImg))
        button2.grid(row=0,column=2, sticky="nsew")
        # If the GUI started from first initialisation
        if len(frameList) == 0:
            # File menu
            filemenu = Menu(menu)
            menu.add_cascade(label='File', menu=filemenu)
            # Save button in File Menu
            #filemenu.add_command(label='Save', command= lambda: self.saveToFile(displayedImg))
            # Exit button in File Menu
            filemenu.add_command(label='Exit', command=window.quit)
            #View menu
            viewmenu = Menu(menu)
            menu.add_cascade(label='View', menu=viewmenu)
            # Refresh button in View Menu
            viewmenu.add_command(label='Refresh', command=lambda: self.refreshGUI(window, menu, frameList, modelPath, modelList, displayedImg, filePath, image,
                                                                                  Program, winW, winH))
            # Model menu
            modelmenu = Menu(menu)
            menu.add_cascade(label='Model', menu=modelmenu)
            # Load Model button in Model Menu
            modelmenu.add_command(label='Load Model',
                                  command=lambda: Program.openAIModel(modelPath, modelList))
            # Add menus to frameList
            frameList.append(filemenu)
            frameList.append(viewmenu)
            frameList.append(modelmenu)

        # Add frames to frameList to be deleted when user chooses refresh function
        frameList.append(frame)
        frameList.append(frame2)

# Program variable to use functions in UseCaseProgram class
Program = UseCaseProgram()
# List variables to hold objects
filePath = list((""))
image = list(())
# Initial width and height values
width = "500"
height = "500"
# Gui variable to use functions in GUI class
newGui = GUI()
# Initialise GUI function using initialised lists and variables
newGui.init(filePath, image, Program, width, height)


