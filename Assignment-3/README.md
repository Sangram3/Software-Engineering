# Assignment-2

NAME: Sangram Rajendra Jagadale <br>
E.NO: 2019CSB1091 <br>
Course: Software Engineering (CS305) <br>
=========================================

## What does this program do

The program consists of an implementation of a Python based API for efficienty storing images into the database along with the metadata and comparing them with the any input image. User can call the API functions to by providing appropriate arguments. User will send this arguments in the format of POST requests, for which I have used FLASK framework.

## A description of how this program works (i.e. its logic)

This is a Python based API, using POSTGRESQL database that provides the following functionality:
  1. store a single image into the database
  2. store a bulk of images into the database (through zip file)
  3. fetch the image information from the database using image_id
  4. find the ```k topmost matching``` images in the database with the input image
  5. uses multithreading to make the process of inserting images to the database FAST
     Detailed desription of the functions and classes is given in the comments

## How to compile and run this program

-Download the folder and extract it.
-There are 3 .py files namely,
 1.app.py : Contains implementation of the server side part, where 5 major functionsa are implemented.
 2.models.py : Contains the FaceDatabase class and all the functions which are required to run the program efficiently
 3.test.py : Contains sufficient number of testcases for each of the API function

## For Testing

-Testing is done using ```Unittest``` library in Python
-For testing the program run, ```python -u test.py```
-To get the code coverage, run
    ```coverage run -m pytest test.py```
    ```coverage report -m```

It will run 5 tests (various scenarios are handled inside the single testcase), and all should pass if everything works well. The code coverage should be around 90%.

## Requirements

1. Python 3.x 
2. PILLOW 
3. Pytest
4. Flask
5. face_recognition 

<br>

