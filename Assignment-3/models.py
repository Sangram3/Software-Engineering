# import psycopg2
# from PIL import Image
import easyocr
import cv2
import os
import spacy

# class Database:
#     def __init__(self, user,password,host,port,db_name) -> None:
        
#         self.db_conn_str = "postgresql://{}:{}@{}:{}/{}".format(user,password,host,port,db_name)
#         create_table_stm = """
#                     CREATE TABLE IF NOT EXISTS books(
#                         id SERIAL PRIMARY KEY,
#                         encoding TEXT,
#                         title TEXT,
#                         isbn TEXT,
#                         publishers TEXT,
#                         authors TEXT
#                     );
#                 """
#         #connecting to the database (POSTGRES)
#         self.conn = psycopg2.connect(self.db_conn_str)
#         #getting cursor
#         self.curs = self.conn.cursor()
#         #creating table if it is not there
#         self.curs.execute(create_table_stm)
#         self.conn.commit()
#     # def insert(self,)

class ImageParser:
    keywords_author = ['author' , 'authored by', 'writer' , 'editor' ]
    keywords_isbn = [str(i) for i in range(10)] + ['-']
    
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    def __init__(self):
        self.authors = []
        self.isbn = ''
        self.publisher = ''
        self.title = ''
    def getImageInfo(self,image_path,languages = ['en'],bol = True):
        if self.allowed_file(image_path) == False:
            return {"Error":"File extension is not correct!"}
        img = cv2.imread(image_path)
        # img = self.getGrayScale(img)
        info = {}
        reader = easyocr.Reader(languages) # this needs to run only once to load the model into memory
        result = reader.readtext(img,paragraph=bol)
        # for r in result:print(*r)
        title = self.getTitle(result)
        # authors = self.getAuthor(result)
        # isbn = self.getISBN(result)
        # publisher = self.getPublisher(result)
        # info['Author'] = authors
        # info['Publisher'] = publisher
        info['Title'] = title
        # info['ISBN'] = isbn
        return info
    
    # def removeNoise(self,img):
    #     return cv2.medianBlur(img,5)

    # def getGrayScale(self,img):
    #     return cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    def getArea(self,p):
        return (p[2][1] - p[0][1])*(p[2][0] - p[0][0])

    # def getThreshold(self,img):
    #     return cv2.threshold(img,0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    def getTitle(self,result):
        area = []
        for val in result:
            area.append([self.getArea(val[0])/len(val[1]),val[1]])
        area.sort(reverse=True)
        return area[0][1]
    
    def getAuthor(self,result):
        authors = []
        for i in result:
            NLP = spacy.load('en_core_web_md')
            DOC = NLP(i[1])
            output = [name for name in DOC.ents if name.label_ == "PERSON"]
            authors+=output
        return authors
    
    def validateISBN(self,text):
        if len(text)!=10 and len(text)!=13:
            return False
        for i in text:
            if i not in self.keywords_isbn:
                return False
        tmp = list(text)
        return True
    def getISBN(self,result):
        isbn = ''
        for i in result:
            cur = i[1]
            for j in range (len(cur)):
                text = cur[j:j+13]
                if self.validateISBN(text):
                    isbn = text
                    break
                text = cur[j: j+10]
                if self.validateISBN(text):
                    isbn = text
                    # break
            if len(isbn):
                break
        return isbn

    def getPublisher(self,result):
        prev = ''
        publisher = ''
        for i in result:
            NLP = spacy.load('en_core_web_md')
            DOC = NLP(i[1])
            for name in DOC.ents:
                if name.label_ == 'ORG':
                    if publisher == '':
                        publisher = str(name)
                    else:
                        if prev == 'PERSON':
                            publisher = str(name)
                            break
                prev = name.label_
        return publisher
        
    def allowed_file(self,filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS    
class ImagesLoader:
    def __init__(self,path):
        self.path = path
    def isDir(self):
        return os.path.isdir(self.path)
    def isFile(self):
        return os.path.isfile(self.path)
    
    def getImages(self):
        images = []  
        if self.isDir():
            for filename in os.listdir(self.path):
                try: images.append(os.path.join(self.path,filename))
                except: continue
        elif self.isFile():
            images = [self.path]
        return images
