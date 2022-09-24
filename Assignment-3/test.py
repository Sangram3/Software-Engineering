import unittest
import app
import models
class FlaskTest(unittest.TestCase):
    def test(self):
        path = 'C:\\Users\\ACER\\Desktop\\FLASK\\assignment-3\\samples\\intro_to_analysis_of_algos1.png'
        R = app.Runner(path)
        response = R.runRunner()
        self.assertEqual(response , {'book1': {'Title': 'AN INTRODUCTION TO THE'}})

if __name__ == "__main__":
    unittest.main()
