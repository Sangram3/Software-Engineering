from app import app
import unittest

class FlaskTest(unittest.TestCase):
    def test_add_face(self):
        tester = app.test_client(self)
        response = tester.post( '/add_face', json = {'image_path':'.\\Abdel_Nasser_Assidi_0002.jpg' })
        statuscode = response.status_code
        print(response.json)
        self.assertEqual(statuscode , 200)

    def test_add_faces_in_bulk(self):
        tester = app.test_client(self)
        response = tester.post( '/add_faces_in_bulk', json = {'zip_path':'.\\sample_zip.zip' })
        statuscode = response.status_code
        print(response.json)
        self.assertEqual(statuscode , 200)

        # response = tester.post( '/add_faces_in_bulk', json = {'zip_path':'C:\\Users\\ACER\\Desktop\\FLASK\\zip_files\\lfw_1.zip' })
        # statuscode = response.status_code
        # print(response.json)
        # self.assertEqual(statuscode , 200)
        
    
    def test_search_faces(self):
        tester = app.test_client(self)
        response = tester.post( '/search_faces', json = {'input_image':'.\\Abdel_Nasser_Assidi_0002.jpg', 'k':3, 'confidence_value':0.5 })
        statuscode = response.status_code
        print(response.json)
        self.assertEqual(statuscode , 200)
    
    def test_get_image_info(self):
        tester = app.test_client(self)
        response = tester.post( '/get_face_info', json = {'api_key':3, 'face_id': 3})
        statuscode = response.status_code
        print(response.json)
        self.assertEqual(statuscode , 200)

        response = tester.post( '/get_face_info', json = {'api_key':3, 'face_id': 0})
        statuscode = response.status_code
        print(response.json)
        self.assertEqual(statuscode , 200)

        response = tester.post( '/get_face_info', json = {'api_key':2, 'face_id': 1})
        statuscode = response.status_code
        print(response.json)
        self.assertEqual(statuscode , 200)

        response = tester.post( '/get_face_info', json = {'api_key':3})
        statuscode = response.status_code
        print(response.json)
        self.assertEqual(statuscode , 200)

    def test_empty_folder(self):
        tester = app.test_client(self)
        response = tester.post( '/empty_folder', json = {'folder_path' : '.\\temp_folder'})
        statuscode = response.status_code
        print(response.json)
        self.assertEqual(statuscode , 200)
if __name__ == "__main__":
    unittest.main()