import face_recognition

import os,shutil
import psycopg2
import zipfile
import ntpath
import time
import threading

#to convert encoding np array to string: to store into the database
def cipher(encoding):
    c_encoding = [str(i) for i in encoding]
    c_encoding = ','.join(encoding)
    return c_encoding

#to get back encoding from the string
def de_cipher(c_encoding):
    c_encoding = c_encoding.split(',')
    encoding = [float(i) for i in c_encoding]
    return encoding

#to get the name of the person from filename
def get_name(img_path):
    img_path = ntpath.basename(img_path)
    name = img_path.split('.')[0].split('_')[:-1]
    name = '_'.join(name)
    return name

#to get the version of the image from filename
def get_version(img_path):
	img_path = ntpath.basename(img_path)
	return int(img_path.split('.')[0].split('_')[-1], 10)

#class: which performs all the actions on the face database
class FaceDatabase:
    def __init__(self, user,password,host,port,db_name) -> None:
        
        self.db_conn_str = "postgresql://{}:{}@{}:{}/{}".format(user,password,host,port,db_name)
        create_table_stm = """
                    CREATE TABLE IF NOT EXISTS faces(
                        id SERIAL PRIMARY KEY,
                        name TEXT,
                        version INT,
                        encoding TEXT
                    );
                """
        #connecting to the database (POSTGRES)
        self.conn = psycopg2.connect(self.db_conn_str)
        #getting cursor
        self.curs = self.conn.cursor()
        #creating table if it is not there
        self.curs.execute(create_table_stm)
        self.conn.commit()
    
    #insert image into the database WITHOUT Encoding
    #this will save our time for encoding

    def insert_image(self,image_path):
        try:
            known_image = face_recognition.load_image_file(image_path)
            encoding = face_recognition.face_encodings(known_image)[0]
            encoding = [str(i) for i in encoding]
            c_encoding = cipher(encoding)
            name = get_name(image_path)
            version = get_version(image_path)
            self.curs.execute("INSERT INTO faces(id, name,version,encoding) VALUES (DEFAULT,%s,%s,%s) RETURNING id",\
                    (name, version , c_encoding))
            returned_id = self.curs.fetchone()[0]
            self.conn.commit()
            # print("Stored {0} into DB record {1}".format(image_path, returned_id))
            return 1
        except:
            return 0
            
    #get encoding of the image using id, if encoding is present in the database
    def get_encoding(self,id):
        try:
            self.curs.execute("SELECT encoding  FROM faces WHERE id = %s", (int(id),))
            c_encoding = self.curs.fetchone()
            c_encoding = c_encoding[0]
            if c_encoding == None:
                return None
            # print("Fetched image with id {0};".format(id))
            encoding = de_cipher(c_encoding)
            return encoding 
        except:
            return 0

    def get_image_info(self,id):
        try:
            self.curs.execute("SELECT name,version  FROM faces WHERE id = %s", (int(id),))
            (name , version) = self.curs.fetchone()
            # print("Fetched name,version with id {0} and name {1};".format(id,name))
            return {'name':name,'version':version} 
        except:
            return 0

    #insert images into the database in bulk
    #@params
    #zip_file_path : path to the zip file
    def insert_images_in_bulk(self,zip_file_path):
        try:
            # temporary folder to extract files in it
            temp_folder = 'temp_folder' 
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(temp_folder)
            # start_time = time.time()
            # for each image in the extracted folder
            threads = []
            for root, dirs, files in os.walk(temp_folder):
                for file in files:
                    
                    image_path = root + "\\" + file
                    # creating new thread
                    t = threading.Thread(target = self.insert_image,args = [image_path])
                    t.start()
                    threads.append(t)
            # end_time = time.time()
            # print('x================TIME REQUIRED FOR UPLOAD ZIP==============x')
            # print(end_time-start_time,'\n')
            
            #joining all the threads that are created
           
            for t in threads:
                t.join()
        
            return 1
        except:
            return 0
    	 
    #to get the k topmost matching images
    def get_top_k_matches(self,input_image,confidence_value = 0.5 ,k = 3):
        try:
            output = []
            #find encoding of the input image
            unknown_image = face_recognition.load_image_file(input_image)
            unknown_encoding_list = face_recognition.face_encodings(unknown_image)
            ind = 1
            final_output = dict()
            for unknown_encoding in unknown_encoding_list:
                for id in range(14000): 
                    flag = self.get_encoding(id)
                    if flag == 0:#id is not in the database
                        continue
                    known_encoding = self.get_encoding(id)
                    if known_encoding == None:
                        continue
                    result = face_recognition.face_distance([known_encoding], unknown_encoding)
                    
                    if result <= confidence_value:
                        tmp =  self.get_image_info(id)
                        name = tmp['name']
                        version = tmp['version']
                        output.append([result,id,name,version])
                output.sort()
                return_output = []
                for i in range(min(len(output),k)):
                    return_output.append({'id':output[i][1],'name':output[i][2],'version':output[i][3] })
                st = 'face{}'.format(str(ind))
                final_output[st] = return_output
                ind+=1
            return final_output
        except:
            return 0
    
    #destructor: upon termination of the program memory is cleared in the file_system
    def __del__(self):
        self.empty_the_folder(".//temp_folder")
        self.conn.close()

    # to clear the memory
    # i.e. delete the images that were generated 
    # in the temporary folders
    def empty_the_folder(self,folder_path):
        folder = folder_path
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
                return 0
        return 1