## Use-Case-Checker
This is my Final Year Project to create a use case diagram checker in Python
<br>BSc title: **Use Case Diagram Checker**<br>

## **Prerequisites**
You would need Python3 and Visual Studio Code installed
Python3 commands have to work and with just python the code may not work
You may need to install python-openCV, PIL, torch, Pyyaml, tqdm, torchvision and seaborn Python libraries
You can install these libraries using pip and the requirements.txt file
Command: pip install -r requirements.txt
The additional external library to install is Tkinter
Command: pip install tk

##Before running commands
Ensure all files and folders are in the same directory/folder
Folders: _py_cache_ , data, models, Pictures, runs, utils
Files:.pre-commit-config.yaml, dataset.yaml, hubconf.py, setup.cfg, train.py, UseCaseProgram.py, val.py, yolov5s.pt

##Built With
PyCharm - Text Editor
Command Prompt - Compiler

##Project Directory Details
A object detection model isn't loaded by default and the user will have to choose the model
The user will have to choose a use case diagram image file in Pictures folder
The trained object detection model weights are in runs/train/
The models, utils and data folders are provided to train the YOLOv5 model

##Object Detection details
exp First trained model (Detects actors, use_case and system_boundary)
exp8 Second trained model (Detects actors, use_case, system_boundary, include and exclude)
exp9 Third, final and best trained model (Detects all elements)
Choose specific weight .pt file in the weights folder to load model
All exp folders have weights folder storing last.pt and best.pt 
best.pt best training epoch
last.pt is last training epoch

##Commands
Run the UseCaseDiagramChecker program
python3 UseCaseProgram.py

To select Model
Choose runs -> train -> choose exp folder -> weights -> best.pt

To select images
Choose a image file in the Pictures folder

Creating new training data
Use LabelImg and select the .txt save file format for YOLO
Create labels in the same order as the dataset.yaml file
Label the new image data accordingly
Save the new image files into data/images
Save the new label .txt files into data/labels

Edit the dataset.yaml file
Dataset.yaml file requires the path, train, val directories on your machine which will be different
path: Directory of the data\ folder on your machine
train: Directory to data\images on your machine
val: Directory to data\images on your machine
nc: number of labels
names: is the labels/ class names

To train the model 
-img = img size
-batch size of img
-epochs number of training loops
-data .yaml file that has the number of labels, labels, train + val img directories
-cfg model config of yolov5
-name name of folder holding results

Start from pretrained weights
python3 train.py --img 640 --batch 16 --epochs 500 --data dataset.yaml --weight yolov5s.pt 

Start from scratch
python3 train.py --img 640 --batch 16 --epochs 500 --data dataset.yaml --cfg ./models/yolov5s.yaml --weights '' 

## **Versioning**
- V1 - added detect shapes and text using terminal
- V2 - created a GUI allowing user to choose buttons
- V3 - Improved the GUI to display the chosen image, but functions display on separate windows
- V4 - Added frames to the GUI
- V5 - Restructured the code into separate classes and functions for the processing and GUI
- V6 - Added image changes from each function to display on same window
- V7 - Added save to file dialog function
   User can choose file directory and filename
- V8 - Improved images displaying on diagram frame to fill most of the frame
   Added refresh function to reset display according to window size
   Added refresh function by wiping old frames and calling GUI functiona again
   Resetting GUI without adding new menu buttons
   Added sizeGrip to bottom righthand corner to show the user the window is resizeable
   Added dynamic font sizes for text in frames and buttons according to window size
- V9 - Managed to make custom model that can be trained, but can't show or draw where the item is
   Created a custom model with pretrained model and managed to train and make it draw bounding boxes
   Improved Check text function to work with model
- V10 - Removed Check text function
   Changed UI to load model only, changed Check Text button to Save Diagram and changed Check Shapes button to Check Diagram
   Removed save from filemenu 
- V11 - Created exp model
   Successfully detects actors, uses cases and system boundaries
- V12 - Created exp8 model
   Successfully detects actors, uses cases and system boundaries like exp
   Detects extend and include with some issues
- V13 - Create exp9 model
   Successfully detects actors, uses cases and system boundaries like exp
   Detects extend and include with no issues like exp8 and detects these elements with arrows
   Successfully detects communication links with some issues
   Fixed bug that duplicates directory of model weights and requires weights to be in duplicate directory
- V14 - Fixed code to run on other machines
   'Upsample' object has no attribute 'recompute_scale_factor' attribute error was caused by newer Torch library version (1.11.0)
   Requirements.txt file was modified to ensure the Torch version 1.10.2 was installed where the object detection works properly

## **Authors**
Ethan Chong 37777025

## **Acknowledgments**
Ultralytics - Files for training yolov5 object detection model
YOLOv5 🚀 by Ultralytics under GPL-3.0 license

## **Provided Files and Folders**
Ultralytics - hubconf.py, train.py, val.py, .pre-commit-config.yaml, setup.cfg, yolov5s.pt
Ultralytics - files in utils, models, data folders
YOLOv5 repository link: https://github.com/ultralytics/yolov5

Files and Folders created by the Author
Files in data/images and data/labels
Files in Pictures Folder
dataset.yaml
modified requirements.txt
UseCaseProgram.py
README.txt
