from flask import Flask,request,redirect
import requests
import ntpath

from models import *
app = Flask(__name__)

USER = 'postgres'
PASSWORD = 'admin'
HOST = 'localhost'
PORT = 5432
DB = 'sampledb'
API_KEY = 3

FD = FaceDatabase(USER,PASSWORD,HOST,PORT,DB)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file( filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Done!
""" Takes the input image and returns the dictionary containing information related to the """
@app.route("/search_faces",methods = ['GET','POST'])
def search_faces(): #image file containing one/more faces
    if 'input_image' not in request.json :
        return {'status':'ERROR','body':'Input image not found in //search_faces!'}
    
    k = 3
    confidence_value = 0.5
    if 'k' in request.json:
        k = request.json['k']
    if 'confidence_value' in request.json:
        confidence_value = request.json['confidence_value']
    
    status = FD.get_top_k_matches(input_image= request.json['input_image'], k=k,confidence_value= confidence_value)
    if status == 0:
        return {'status':'ERROR','body':'Error while searching the database in //search_faces!'}
    return {"status": "OK", "body": {"matches": status}}

#Done!
@app.route("/add_face", methods = ["GET","POST"])
def add_face(): #save the UploadFile in the database
    if request.method == 'POST':
        if 'image_path' not in request.json:
            redirect(request.url)
        file_path = request.json['image_path']
        filename = ntpath.basename(file_path)
        if file_path and allowed_file(filename):
            status = FD.insert_image(file_path)
            if status:
                return {"status":"OK", "body":"Image uploaded successfully, to the database in //add_face!"}
            return {"status": "ERROR", "body":"Error occured, while uploading image to the database in //add_face!"}
    if request.method == 'GET':
        return {"status":"INVALID REQUEST", 'Body':'POST request expected, GET found in //add_face!'}

#Done!
@app.route("/add_faces_in_bulk",methods = ["GET","POST"])
def add_faces_in_bulk(): #zip file containing multiple images

    if request.method == 'POST':
        if 'zip_path' not in request.json:
            redirect(request.url)
        zip_path = request.json['zip_path']
        if zip_path :
            status = FD.insert_images_in_bulk(zip_path)
            
            if status:
                return {"status":"OK", "body":"Images uploaded successfully, to the database in //add_faces_in_bulk!"}
            return {"status": "ERROR", "body":"Error occured, while uploading images to the database in //add_face_in_bulk!"}
        
    if request.method == 'GET':
        return {"status":"INVALID REQUEST", 'Body':'POST request expected, GET found in //add_faces_in_bulk!'}

#Done!
@app.route("/get_face_info",methods = ["GET","POST"])
def get_face_info():
    
    if 'api_key' not in request.json or 'face_id' not in request.json:
        return {"status":"ERROR" , 'body':'Insufficient information in //get_face_info!'}
    api_key = request.json['api_key']
    face_id = request.json['face_id']
    if api_key != API_KEY:
        return {"status":"API KEY ERROR" , 'body':'Invalid API Key provided in //get_face_info'}
    status = FD.get_image_info(face_id)
    if status == 0:
        return {"status":"ERROR" ,'body':'Error while retrieving image from database in //get_face_info!'}
    if status:
        return {'status':'OK' , 'body': status} 

#Done!
@app.route("/empty_folder",methods = ["GET","POST"])
def empty_folder():
    folder = request.json['folder_path']
    status = FD.empty_the_folder(folder)
    if status == 0:
        return {"status":"ERROR" ,'body':'Error while clearing the folder in //empty_folder!'}
    if status:
        return {'status':'OK' , 'body': 'Folder {} cleared successfully in //empty_folder!'.format(folder)} 
# if __name__ == '__main__':
#     app.secret1_key='secret123'
#     app.run(port = 5000 , host = 'localhost' , debug=True)



        