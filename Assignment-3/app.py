from models import *
import os,sys
path = 'C:\\Users\\ACER\\Desktop\\FLASK\\assignment-3\\samples\\intro_to_analysis_of_algos.png'

class Runner:
    def __init__(self,path,bol = True):
        self.bol = bol
        self.path = path
        self.IL = ImagesLoader(path)
        self.images = self.IL.getImages()
        
    def runRunner(self):
        out = {}
        ind = 1
        for image in self.images:
            IP = ImageParser()
            output = IP.getImageInfo(image,bol = self.bol)
            out['book'+str(ind)] = output
            ind+=1
        return out
if __name__ == "__main__":
    R = Runner(path)
    print(R.runRunner())


